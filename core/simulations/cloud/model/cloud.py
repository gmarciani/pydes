from core.simulations.cloud.model.event import EventType
from core.simulations.cloud.model.event import SimpleEvent as Event
from core.random.rndvar import exponential
import logging

# Configure logger
logger = logging.getLogger(__name__)


class SimpleCloud:
    """
    A simple Cloud server, defined by its state.
    """

    def __init__(self, rndgen, service_rate_1, service_rate_2, setup_mean):
        """
        Create a new Cloud server.
        :param rndgen: (object) the multi-stream random number generator.
        :param service_rate_1: (float) the service rate for job of type 1 (tasks/s).
        :param service_rate_2: (float) the service rate for job of type 2 (tasks/s).
        :param setup_mean: (float) the mean setup time to restart a task of type 2 in the Cloud (s).
        """
        self._rndgen = rndgen
        self.service_rate_1 = service_rate_1
        self.service_rate_2 = service_rate_2
        self.setup_mean = setup_mean

        # state
        self.n_1 = 0  # number of tasks of type 1 serving in the Cloud
        self.n_2 = 0  # number of tasks of type 2 serving in the Cloud

        # statistics
        self.n_arrival_1 = 0  # number of tasks of type 1 arrived to the Cloud
        self.n_arrival_2 = 0  # number of tasks of type 2 arrived to the Cloud
        self.n_served_1 = 0  # number of tasks of type 1 served in the Cloud
        self.n_served_2 = 0  # number of tasks of type 2 served in the Cloud
        self.n_restarted_2 = 0  # number of tasks of type 2 restarted in the Cloudlet

        self.t_service_1 = 0.0  # the total service time for tasks of tye 1
        self.t_service_2 = 0.0  # the total service time for tasks of tye 2
        self.t_restart_2 = 0.0  # the total restart time wasted for restarted tasks of type 2

    # ==================================================================================================================
    # EVENT SUBMISSION
    #   * ARRIVAL_TASK_1
    #   * ARRIVAL_TASK_2
    #   * RESTART_CLOUD_TASK_2
    #   * COMPLETION_CLOUD_TASK_1
    #   * COMPLETION_CLOUD_TASK_2
    # ==================================================================================================================

    def submit_arrival_task_1(self, t_arrival):
        """
        Submit to the Cloud the arrival of a task of type 1.
        :param t_arrival: (float) the arrival time.
        :return: (SimpleEvent) the completion event of the submitted task of type 1.
        """
        # Update state
        self.n_1 += 1

        # Generate completion
        t_service = self.get_service_time_task_1()
        t_completion = t_arrival + t_service
        completion_event = Event(EventType.COMPLETION_CLOUD_TASK_1, t_completion, t_service=t_service)

        # Update statistics
        self.n_arrival_1 += 1

        return completion_event

    def submit_arrival_task_2(self, t_arrival):
        """
        Submit to the Cloud the arrival of a task of type 2.
        :param t_arrival: (float) the arrival time.
        :return: (SimpleEvent) the completion event of the submitted task of type 2.
        """
        # Update state
        self.n_2 += 1

        # Generate completion
        t_service = self.get_service_time_task_2()
        t_completion = t_arrival + t_service
        completion_event = Event(EventType.COMPLETION_CLOUD_TASK_2, t_completion, t_service=t_service)

        # Update statistics
        self.n_arrival_2 += 1

        return completion_event

    def submit_restart_task_2(self, t_arrival):
        """
        Submit to the Cloud the restart of a task of type 2.
        :param t_arrival: (float) the arrival time.
        :return: (SimpleEvent) the completion event of the submitted task of type 2.
        """
        # Update state
        self.n_2 += 1

        # Generate completion
        t_setup = self.get_setup_time_task_2()
        t_service = self.get_service_time_task_2()
        t_completion = t_arrival + t_service
        completion_event = Event(EventType.COMPLETION_CLOUD_TASK_2, t_completion, t_service=t_service, t_wait=t_setup)

        # Update statistics
        self.n_arrival_2 += 1
        self.n_restarted_2 += 1
        self.t_restart_2 += t_setup

        return completion_event

    def submit_completion_task_1(self, t_completion, t_service):
        """
        Submit to the Cloud the completion of a task of type 1.
        :param t_completion: (float) the completion time.
        :param t_service: (float) the service time.
        :return: None
        """
        # Check correctness
        assert self.n_1 > 0

        # Update state
        self.n_1 -= 1

        # Update statistics
        self.n_served_1 += 1
        self.t_service_1 += t_service

    def submit_completion_task_2(self, t_completion, t_service):
        """
        Submit to the Cloud the completion of a task of type 2.
        :param t_completion: (float) the completion time.
        :param t_service: (float) the service time.
        :return: None
        """
        # Check correctness
        assert self.n_2 > 0

        # Update state
        self.n_2 -= 1

        # Update statistics
        self.n_served_2 += 1
        self.t_service_2 += t_service

    # ==================================================================================================================
    # RANDOM TIME GENERATION
    #   * service time task 1
    #   * service time task 2
    #   * setup time task 2
    # ==================================================================================================================

    def get_service_time_task_1(self):
        """
        Generate the service time for a task of type 1, exponentially distributed with rate *service_rate_1*.
        :return: (float) the service time for a task of type 1 (s).
        """
        self._rndgen.stream(EventType.COMPLETION_CLOUD_TASK_1.value)
        return exponential(1.0 / self.service_rate_1, self._rndgen.rnd())

    def get_service_time_task_2(self):
        """
        Generate the service time for a task of type 2, exponentially distributed with rate *service_rate_2*.
        :return: (float) the service time for a task of type 2 (s).
        """
        self._rndgen.stream(EventType.COMPLETION_CLOUD_TASK_2.value)
        return exponential(1.0 / self.service_rate_2, self._rndgen.rnd())

    def get_setup_time_task_2(self):
        """
        Generate the setup time for a restarted task of type 2, exponentially distributed with mean *setup_mean*.
        :return: (float) the setup time for a restarted task of type 2 (s).
        """
        self._rndgen.stream(EventType.RESTART_TASK_2.value)
        return exponential(self.setup_mean, self._rndgen.rnd())

    # ==================================================================================================================
    # OTHER
    # ==================================================================================================================

    def __str__(self):
        """
        String representation.
        :return: the string representation.
        """
        sb = ["{attr}={value}".format(attr=attr, value=self.__dict__[attr]) for attr in self.__dict__ if
              not attr.startswith("__") and not callable(getattr(self, attr))]
        return "Cloud({}:{})".format(id(self), ", ".join(sb))

