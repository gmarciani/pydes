from core.simulation.model.cloudlet import SimpleCloudlet as Cloudlet
from core.simulation.model.cloud import SimpleCloud as Cloud
from core.simulation.model.event import SimpleEvent as Event, EventType
from core.simulation.model.scope import SystemScope
from core.simulation.model.scope import TaskScope
from core.simulation.model.scope import ActionScope
from core.utils.logutils import get_logger


# Logging
logger = get_logger(__name__)


class SimpleCloudletCloudSystem:
    """
    A system composed by a Cloudlet and a Cloud.
    """

    def __init__(self, rndgen, config, statistics):
        """
        Create a new system.
        :param rndgen: (object) the multi-stream random number generator.
        :param config: (dictionary) the configuration for the system.
        :param statistics: (SimulationStatistics) the simulation statistics.
        """
        # State
        self.state = {sys: {tsk: 0 for tsk in TaskScope.concrete()} for sys in SystemScope.subsystems()}

        # Statistics
        self.statistics = statistics

        # Subsystem - Cloudlet
        self.cloudlet = Cloudlet(
            rndgen,
            config["cloudlet"],
            self.state[SystemScope.CLOUDLET],
            self.statistics
        )

        # Subsystem - Cloud
        self.cloud = Cloud(
            rndgen,
            config["cloud"],
            self.state[SystemScope.CLOUD],
            self.statistics
        )

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

        if event.type.act is ActionScope.ARRIVAL:

            # Submit the arrival
            e_completions_to_schedule, e_completions_to_unschedule = self.submit_arrival(event.type.tsk, event.time)

            # Add completions to schedule
            response_events_to_schedule.extend(e_completions_to_schedule)

            # Add completions to unschedule
            response_events_to_unschedule.extend(e_completions_to_unschedule)

        elif event.type.act is ActionScope.COMPLETION:

            # Submit the completion
            self.submit_completion(event.type.tsk, event.type.sys, event.time, event.meta)
        else:
            raise ValueError("Unrecognized event: {}".format(event))

        # Update statistics (only population)
        #self.sample_mean_population()

        return response_events_to_schedule, response_events_to_unschedule

    def submit_arrival(self, tsk, t_now):
        """
        Submit the arrival of a task.
        :param tsk: (TaskType) the type of task.
        :param t_now: (float) the arrival time.
        :return: (s,u) where
        *s* is a list of events to schedule;
        *u* is a list of events to unschedule;
        """
        e_to_schedule = []
        e_to_unschedule = []

        # Process event
        if tsk is TaskScope.TASK_1:

            if self.state[SystemScope.CLOUDLET][TaskScope.TASK_1] == self.cloudlet.n_servers:
                logger.debug("{} sent to CLOUD at {}".format(tsk, t_now))
                t_completion = self.cloud.submit_arrival(tsk, t_now)
                e_completion = Event(EventType.of(ActionScope.COMPLETION, SystemScope.CLOUD, tsk), t_completion, t_arrival=t_now)
                e_to_schedule.append(e_completion)

            elif self.state[SystemScope.CLOUDLET][TaskScope.TASK_1] + self.state[SystemScope.CLOUDLET][TaskScope.TASK_2] < self.cloudlet.threshold:
                logger.debug("{} sent to CLOUDLET at {}".format(tsk, t_now))
                t_completion = self.cloudlet.submit_arrival(tsk, t_now)
                e_completion = Event(EventType.of(ActionScope.COMPLETION, SystemScope.CLOUDLET, tsk), t_completion, t_arrival=t_now)
                e_to_schedule.append(e_completion)

            elif self.state[SystemScope.CLOUDLET][TaskScope.TASK_2] > 0:
                tsk_interrupt = TaskScope.TASK_2
                logger.debug("{} interrupted in CLOUDLET at {}".format(tsk_interrupt, t_now))
                t_completion_1, t_arrival_1 = self.cloudlet.submit_interruption(tsk_interrupt, t_now)
                e_completion_to_ignore = Event(EventType.of(ActionScope.COMPLETION, SystemScope.CLOUDLET, tsk_interrupt), t_completion_1)
                e_to_unschedule.append(e_completion_to_ignore)

                logger.debug("{} restarted in CLOUD at {}".format(tsk_interrupt, t_now))
                t_completion = self.cloud.submit_arrival(tsk_interrupt, t_now, restart=True)
                # TODO check t_arrival=t_arrival_1 or t_now
                e_completion = Event(EventType.of(ActionScope.COMPLETION, SystemScope.CLOUD, tsk_interrupt), t_completion, t_arrival=t_now, switched=True)
                e_to_schedule.append(e_completion)

                logger.debug("{} sent to CLOUDLET at {}".format(tsk, t_now))
                t_completion = self.cloudlet.submit_arrival(tsk, t_now)
                e_completion = Event(EventType.of(ActionScope.COMPLETION, SystemScope.CLOUDLET, tsk), t_completion, t_arrival=t_now)
                e_to_schedule.append(e_completion)

            else:
                logger.debug("{} sent to CLOUDLET at {}".format(tsk, t_now))
                t_completion = self.cloudlet.submit_arrival(tsk, t_now)
                e_completion = Event(EventType.of(ActionScope.COMPLETION, SystemScope.CLOUDLET, tsk), t_completion, t_arrival=t_now)
                e_to_schedule.append(e_completion)

        elif tsk is TaskScope.TASK_2:
            if self.state[SystemScope.CLOUDLET][TaskScope.TASK_1] + self.state[SystemScope.CLOUDLET][TaskScope.TASK_2] >= self.cloudlet.threshold:
                logger.debug("{} sent to CLOUD at {}".format(tsk, t_now))
                t_completion = self.cloud.submit_arrival(tsk, t_now)
                e_completion = Event(EventType.of(ActionScope.COMPLETION, SystemScope.CLOUD, tsk), t_completion, t_arrival=t_now)
                e_to_schedule.append(e_completion)

            else:
                logger.debug("{} sent to CLOUDLET at {}".format(tsk, t_now))
                t_completion = self.cloudlet.submit_arrival(tsk, t_now)
                e_completion = Event(EventType.of(ActionScope.COMPLETION, SystemScope.CLOUDLET, tsk), t_completion, t_arrival=t_now)
                e_to_schedule.append(e_completion)

        else:
            raise ValueError("Unrecognized task type {}".format(tsk))

        return e_to_schedule, e_to_unschedule

    def submit_completion(self, tsk, scope, t_now, meta):
        """
        Submit the completion of a task.
        :param tsk: (TaskType) the type of task.
        :param scope: (Scope) the scope.
        :param t_now: (float) the occurrence time of the event.
        :param meta: (dict) metadata associate to the completion event.
        :return: None
        """
        logger.debug("{} completed in {} at {}".format(tsk, scope, t_now))

        # Check correctness
        assert self.state[scope][tsk] > 0

        # Process event
        if scope is SystemScope.CLOUDLET:
            self.cloudlet.submit_completion(tsk, t_now, meta.t_arrival)
        elif scope is SystemScope.CLOUD:
            switched = meta.switched if "switched" in meta.__dict__ else False
            self.cloud.submit_completion(tsk, t_now, meta.t_arrival, switched)
        else:
            raise ValueError("Unrecognized scope {}".format(scope))

    # ==================================================================================================================
    # OTHER
    # ==================================================================================================================

    def is_idle(self):
        """
        Check weather the system is idle or not.
        :return: True, if the system is idle; False, otherwise.
        """
        return self.cloudlet.is_idle() and self.cloud.is_idle()

    def sample_mean_population(self):
        """
        Register the sample for the mean population.
        :return: None.
        """
        for tsk in TaskScope.concrete():
            self.statistics.metrics.population[SystemScope.SYSTEM][tsk].add_sample(
                sum(self.state[sys][tsk] for sys in SystemScope.subsystems()))
        self.statistics.metrics.population[SystemScope.SYSTEM][TaskScope.GLOBAL].add_sample(
            sum(x for sys in SystemScope.subsystems() for x in self.state[sys].values()))

    def __str__(self):
        """
        String representation.
        :return: the string representation.
        """
        sb = ["{attr}={value}".format(attr=attr, value=self.__dict__[attr]) for attr in self.__dict__ if
              not attr.startswith("__") and not callable(getattr(self, attr))]
        return "System({}:{})".format(id(self), ", ".join(sb))