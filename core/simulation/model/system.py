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

        # Whole-run Statistics (used in verification)
        self.arrived = {task: 0 for task in Task}  # total number of arrived tasks, by task type
        self.completed = {task: 0 for task in Task}  # total number of completed tasks, by task type
        self.switched = {task: 0 for task in Task}  # total number of restarted tasks, by task type
        self.service = {task: 0 for task in Task}  # total service time, by task type

        # Batch statistics
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

            # Submit the completion
            self.submit_completion(event.type.task, event.type.scope, event.time, event.t_arrival)

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

        # Update batch statistics
        self.statistics.n.add_sample(self.n[Task.TASK_1] + self.n[Task.TASK_2])
        self.statistics.arrived.increment()

        # Process event
        if task_type is Task.TASK_1:

            if self.cloudlet.n[Task.TASK_1] == self.cloudlet.n_servers:
                logger.debug("{} sent to CLOUD at {}".format(task_type, t_arrival))
                t_completion = self.cloud.submit_arrival(task_type, t_arrival)
                e_completion = Event(EventType.of(Action.COMPLETION, Scope.CLOUD, task_type), t_completion, t_arrival=t_arrival)
                e_to_schedule.append(e_completion)

            elif self.cloudlet.n[Task.TASK_1] + self.cloudlet.n[Task.TASK_2] < self.cloudlet.threshold:
                logger.debug("{} sent to CLOUDLET at {}".format(task_type, t_arrival))
                t_completion = self.cloudlet.submit_arrival(task_type, t_arrival)
                e_completion = Event(EventType.of(Action.COMPLETION, Scope.CLOUDLET, task_type), t_completion, t_arrival=t_arrival)
                e_to_schedule.append(e_completion)

            elif self.cloudlet.n[Task.TASK_2] > 0:
                task_to_interrupt = Task.TASK_2
                logger.debug("{} interrupted in CLOUDLET at {}".format(task_to_interrupt, t_arrival))
                t_completion_1, t_arrival_1, r_remaining_1 = self.cloudlet.submit_interruption(task_to_interrupt, t_arrival)
                e_completion_to_ignore = Event(EventType.of(Action.COMPLETION, Scope.CLOUDLET, task_to_interrupt), t_completion_1)
                e_to_unschedule.append(e_completion_to_ignore)

                logger.debug("{} restarted in CLOUD at {}".format(task_to_interrupt, t_arrival))
                t_completion = self.cloud.submit_restart(task_to_interrupt, t_arrival, r_remaining_1)
                e_completion = Event(EventType.of(Action.COMPLETION, Scope.CLOUD, task_to_interrupt), t_completion, t_arrival=t_arrival_1)
                e_to_schedule.append(e_completion)

                logger.debug("{} sent to CLOUDLET at {}".format(task_type, t_arrival))
                t_completion = self.cloudlet.submit_arrival(task_type, t_arrival)
                e_completion = Event(EventType.of(Action.COMPLETION, Scope.CLOUDLET, task_type), t_completion, t_arrival=t_arrival)
                e_to_schedule.append(e_completion)

                # Update statistic
                self.switched[task_type] += 1

                # Update batch statistics
                self.statistics.switched.increment()

            else:
                logger.debug("{} sent to CLOUDLET at {}".format(task_type, t_arrival))
                t_completion = self.cloudlet.submit_arrival(task_type, t_arrival)
                e_completion = Event(EventType.of(Action.COMPLETION, Scope.CLOUDLET, task_type), t_completion, t_arrival=t_arrival)
                e_to_schedule.append(e_completion)

        elif task_type is Task.TASK_2:
            if self.cloudlet.n[Task.TASK_1] + self.cloudlet.n[Task.TASK_2] >= self.cloudlet.threshold:
                logger.debug("{} sent to CLOUD at {}".format(task_type, t_arrival))
                t_completion = self.cloud.submit_arrival(task_type, t_arrival)
                e_completion = Event(EventType.of(Action.COMPLETION, Scope.CLOUD, task_type), t_completion, t_arrival=t_arrival)
                e_to_schedule.append(e_completion)

            else:
                logger.debug("{} sent to CLOUDLET at {}".format(task_type, t_arrival))
                t_completion = self.cloudlet.submit_arrival(task_type, t_arrival)
                e_completion = Event(EventType.of(Action.COMPLETION, Scope.CLOUDLET, task_type), t_completion, t_arrival=t_arrival)
                e_to_schedule.append(e_completion)

        else:
            raise ValueError("Unrecognized task type {}".format(task_type))

        return e_to_schedule, e_to_unschedule

    def submit_completion(self, task_type, scope, t_completion, t_arrival):
        """
        Submit the completion of a task.
        :param task_type: (TaskType) the type of task.
        :param scope: (Scope) the scope.
        :param t_completion: (float) the occurrence time of the event.
        :param t_arrival: (float) the arrival time.
        :return: None
        """
        logger.debug("{} completed in {} at {}".format(task_type, scope, t_completion))

        # Check correctness
        if scope is Scope.CLOUDLET:
            assert self.cloudlet.n[task_type] > 0
        if scope is Scope.CLOUD:
            assert self.cloud.n[task_type] > 0

        # Update state
        self.n[task_type] -= 1

        # Update local metrics
        self.completed[task_type] += 1
        self.service[task_type] += t_completion - t_arrival

        # Update batch metrics
        self.statistics.n.add_sample(self.n[Task.TASK_1] + self.n[Task.TASK_2])
        self.statistics.completed.increment()
        self.statistics.service.increment(t_completion - t_arrival)

        # Process event
        if scope is Scope.CLOUDLET:
            self.cloudlet.submit_completion(task_type, t_completion, t_arrival)
        elif scope is Scope.CLOUD:
            self.cloud.submit_completion(task_type, t_completion, t_arrival)
        else:
            raise ValueError("Unrecognized scope {}".format(scope))

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