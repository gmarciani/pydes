from core.simulation.model.cloudlet import SimpleCloudlet as Cloudlet
from core.simulation.model.cloud import SimpleCloud as Cloud
from core.simulation.model.event import SimpleEvent as Event, EventType, Action, Scope
from core.simulation.model.server_selection_rule import SelectionRule
from core.simulation.model.task import Task
import logging

# Configure logger
logger = logging.getLogger(__name__)


class SimpleCloudletCloudSystem:
    """
    A simple system, made of a Cloudlet and a Cloud.
    """

    def __init__(self, rndgen, config_cloudlet, config_cloud, statistics):
        """
        Create a new system.
        :param rndgen: (object) the multi-stream random number generator.
        :param config_cloudlet: (dictionary) the configuration for the Cloudlet.
        :param config_cloud: (dictionary) the configuration for the Cloud.
        :param statistics: (SimulationStatistics) the simulation statistics.
        """
        self.cloudlet = Cloudlet(
            rndgen,
            config_cloudlet["n_servers"],
            config_cloudlet["service_rate_1"],
            config_cloudlet["service_rate_2"],
            config_cloudlet["threshold"],
            SelectionRule[config_cloudlet["server_selection"]]
        )

        self.cloud = Cloud(
            rndgen,
            config_cloud["service_rate_1"],
            config_cloud["service_rate_2"],
            config_cloud["t_setup_mean"]
        )

        # State
        self.n = {task: 0 for task in Task}  # current number of tasks, by task type

        # Statistics
        self.arrived = {task: 0 for task in Task}  # total number of arrived tasks, by task type
        self.completed = {task: 0 for task in Task}  # total number of completed tasks, by task type
        self.restarted = {task: 0 for task in Task}  # total number of restarted tasks, by task type
        self.service = {task: 0 for task in Task}  # total service time, by task type

        # Simulation statistics
        self.statistics = statistics

    # ==================================================================================================================
    # EVENT SUBMISSION
    #   * ARRIVAL_TASK_1
    #   * ARRIVAL_TASK_2
    #   * COMPLETION_CLOUDLET_TASK_1
    #   * COMPLETION_CLOUDLET_TASK_2
    #   * COMPLETION_CLOUD_TASK_1
    #   * COMPLETION_CLOUD_TASK_2
    # ==================================================================================================================
    def submit(self, event):
        """
        Submit an event to th system.
        :param event: (SimpleEvent) the event
        :return: ([s],[u]) where
        *s* is a list of events to schedule;
        *u* is a list of events to unschedule.
        """
        response_events_to_schedule = []
        response_events_to_unschedule = []

        if event.type.action is Action.ARRIVAL:
            # Submit the arrival
            e_completions_to_schedule, e_completions_to_unschedule = self.submit_arrival(event.type.task, event.time)

            # Add completions to schedule
            response_events_to_schedule.extend(e_completions_to_schedule)

            # Add completions to unschedule
            response_events_to_unschedule.extend(e_completions_to_unschedule)

        elif event.type.action is Action.COMPLETION:

            if event.type.scope is Scope.CLOUDLET:
                # Submit the completion in Cloudlet
                self.submit_completion_cloudlet(event.type.task, event.time, event.t_service)

            elif event.type.scope is Scope.CLOUD:
                # Submit the completion in Cloud
                self.submit_completion_cloud(event.type.task, event.time, event.t_service)

            else:
                raise ValueError("Unrecognized event: {}".format(event))

        else:
            raise ValueError("Unrecognized event: {}".format(event))

        return response_events_to_schedule, response_events_to_unschedule

    def submit_arrival(self, task_type, t_arrival):
        """
        Submit the arrival of a task.
        :param task_type: (TaskType) the type of task.
        :param t_arrival: (float) the arrival time.
        :return: (s,u) where
        *s* is a list of events to schedule;
        *u* is a list of events to unschedule;
        """
        e_to_schedule = []
        e_to_unschedule = []

        # Update state
        self.n[task_type] += 1

        # Update statistics
        self.arrived[task_type] += 1

        # Process event
        if task_type is Task.TASK_1:

            if self.cloudlet.n[Task.TASK_1] == self.cloudlet.n_servers:
                logger.debug("{} sent to CLOUD at {}".format(task_type, t_arrival))
                t_completion, t_service = self.cloud.submit_arrival(task_type, t_arrival)
                e_completion = Event(EventType.of(Action.COMPLETION, Scope.CLOUD, task_type), t_completion, t_service=t_service)
                e_to_schedule.append(e_completion)

            elif self.cloudlet.n[Task.TASK_1] + self.cloudlet.n[Task.TASK_2] < self.cloudlet.threshold:
                logger.debug("{} sent to CLOUDLET at {}".format(task_type, t_arrival))
                t_completion, t_service = self.cloudlet.submit_arrival(task_type, t_arrival)
                e_completion = Event(EventType.of(Action.COMPLETION, Scope.CLOUDLET, task_type), t_completion, t_service=t_service)
                e_to_schedule.append(e_completion)

            elif self.cloudlet.n[Task.TASK_2] > 0:
                task_to_interrupt = Task.TASK_2
                logger.debug("{} interrupted in CLOUDLET at {}".format(task_to_interrupt, t_arrival))
                t_completion, t_arrival, t_served, r_remaining = self.cloudlet.submit_interruption(task_to_interrupt, t_arrival)
                e_completion_to_ignore = Event(EventType.of(Action.COMPLETION, Scope.CLOUDLET, task_to_interrupt), t_completion)
                e_to_unschedule.append(e_completion_to_ignore)

                logger.debug("{} restarted in CLOUD at {}".format(task_to_interrupt, t_arrival))
                t_completion, t_service = self.cloud.submit_restart(task_to_interrupt, t_arrival, r_remaining)
                e_completion = Event(EventType.of(Action.COMPLETION, Scope.CLOUD, task_to_interrupt), t_completion, t_service=t_service+t_served)  # IMPORTANT
                e_to_schedule.append(e_completion)

                logger.debug("{} sent to CLOUDLET at {}".format(task_type, t_arrival))
                t_completion, t_service = self.cloudlet.submit_arrival(task_type, t_arrival)
                e_completion = Event(EventType.of(Action.COMPLETION, Scope.CLOUDLET, task_type), t_completion, t_service=t_service)
                e_to_schedule.append(e_completion)

            else:
                logger.debug("{} sent to CLOUDLET at {}".format(task_type, t_arrival))
                t_completion, t_service = self.cloudlet.submit_arrival(task_type, t_arrival)
                e_completion = Event(EventType.of(Action.COMPLETION, Scope.CLOUDLET, task_type), t_completion, t_service=t_service)
                e_to_schedule.append(e_completion)

        elif task_type is Task.TASK_2:
            if self.cloudlet.n[Task.TASK_1] + self.cloudlet.n[Task.TASK_2] >= self.cloudlet.threshold:
                logger.debug("{} sent to CLOUD at {}".format(task_type, t_arrival))
                t_completion, t_service = self.cloud.submit_arrival(task_type, t_arrival)
                e_completion = Event(EventType.of(Action.COMPLETION, Scope.CLOUD, task_type), t_completion, t_service=t_service)
                e_to_schedule.append(e_completion)

            else:
                logger.debug("{} sent to CLOUDLET at {}".format(task_type, t_arrival))
                t_completion, t_service = self.cloudlet.submit_arrival(task_type, t_arrival)
                e_completion = Event(EventType.of(Action.COMPLETION, Scope.CLOUDLET, task_type), t_completion, t_service=t_service)
                e_to_schedule.append(e_completion)

        else:
            raise ValueError("Unrecognized task type {}".format(task_type))

        return e_to_schedule, e_to_unschedule

    def submit_completion_cloudlet(self, task_type, t_completion, t_service):
        """
        Submit the completion of a task in Cloudlet.
        :param task_type: (TaskType) the type of task.
        :param t_completion: (float) the occurrence time of the event.
        :param t_service: (float) the service time.
        :return: None
        """
        logger.debug("{} completed in CLOUDLET at {}".format(task_type, t_completion))

        # Check correctness
        assert self.cloudlet.n[task_type] > 0

        # Update state
        self.n[task_type] -= 1

        # Update local metrics
        self.completed[task_type] += 1
        self.service[task_type] += t_service

        # Update batch metrics
        self.statistics.t_response.add_sample(t_service)
        self.statistics.completed.add_value(1)
        self.statistics.throughput.add_sample(self.completed[task_type], t_completion)  # BUG

        # Process event
        self.cloudlet.submit_completion(task_type, t_completion)

    def submit_completion_cloud(self, task_type, t_completion, t_service):
        """
        Submit the completion of a task in Cloud.
        :param task_type: (TaskType) the type of task.
        :param t_completion: (float) the occurrence time of the event.
        :param t_service: (float) the service time.
        :return: None
        """
        logger.debug("{} completed in CLOUD at {}".format(task_type, t_completion))

        # Check correctness
        assert self.cloud.n[task_type] > 0

        # Update state
        self.n[task_type] -= 1

        # Update local metrics
        self.completed[task_type] += 1
        self.service[task_type] += t_service

        # Update batch metrics
        self.statistics.t_response.add_sample(t_service)
        self.statistics.completed.add_value(1)
        self.statistics.throughput.add_sample(self.completed[task_type], t_completion)  # BUG

        # Process event
        self.cloud.submit_completion(task_type, t_completion, t_service)

    # ==================================================================================================================
    # METRICS
    # ==================================================================================================================

    #def get_response_time(self):
    #    """
    #    Compute the overall system response time (mean).
    #    :return: (float) the overall system response time.
    #    """
    #    return self.statistics.response_time.get_mean()

    #def get_throughput(self):
    #    """
    #    Compute the overall system throughput.
    #    :return: (float) the overall system throughput.
    #    """
    #    return (self.n_served_1 + self.n_served_2) / self.t_last_completion

    #def get_utilization(self):
    #    """
    #    Compute the overall system utilization.
    #    :return: (float) the overall system utilization.
    #    """
    #    return self.area_service / self.t_last_completion

    #def get_wasted_time(self):
    #    """
    #    Compute the overall system wasted time.
    #    :return: (float) the overall system wasted time.
    #    """
    #    return self.cloudlet.t_wasted_2 + self.cloud.t_restart_2

    # ==================================================================================================================
    # OTHER
    # ==================================================================================================================

    def empty(self):
        """
        Check weather the system is empty or not.
        :return: True, if the system is empty; False, otherwise.
        """
        return self.n[Task.TASK_1] + self.n[Task.TASK_2] == 0

    def __str__(self):
        """
        String representation.
        :return: the string representation.
        """
        sb = ["{attr}={value}".format(attr=attr, value=self.__dict__[attr]) for attr in self.__dict__ if
              not attr.startswith("__") and not callable(getattr(self, attr))]
        return "System({}:{})".format(id(self), ", ".join(sb))