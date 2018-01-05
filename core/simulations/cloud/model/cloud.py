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

    def __init__(self, rndgen, service_rate_1, service_rate_2, t_setup_mean):
        """
        Create a new Cloud server.
        :param rndgen: (object) the multi-stream random number generator.
        :param service_rate_1: (float) the service rate for job of type 1 (tasks/s).
        :param service_rate_2: (float) the service rate for job of type 2 (tasks/s).
        :param t_setup_mean: (float) the mean setup time to restart a task of type 2 in the Cloud (s).
        """
        self._rndgen = rndgen
        self.service_rate_1 = service_rate_1
        self.service_rate_2 = service_rate_2
        self.t_setup_mean = t_setup_mean

        # state
        self.n_1 = 0  # number of tasks of type 1 serving in the Cloud
        self.n_2 = 0  # number of tasks of type 2 serving in the Cloud

        # statistics
        self.n_arrival_1 = 0  # number of tasks of type 1 arrived to the Cloud
        self.n_arrival_2 = 0  # number of tasks of type 2 arrived to the Cloud
        self.n_served_1 = 0  # number of tasks of type 1 served in the Cloud
        self.n_served_2 = 0  # number of tasks of type 2 served in the Cloud
        self.n_restarted_2 = 0  # number of tasks of type 2 restarted in the Cloudlet

        self.t_last_arrival = 0.0  # the last arrival time (float) (s)
        self.t_last_completion = 0.0  # the last completion time (float) (s)
        self.t_last_idle = 0.0  # the last idle time (float) (s)

        self.busy_time = 0.0  # the total busy time (float) (s)

    def submit_arrival_task_1(self, event_time):
        """
        Submit to the Cloud the arrival of a task of type 1.
        :param event_time: (float) the occurrence time of the event.
        :return: (SimpleEvent) the completion event of the submitted task of type 1.
        """
        # record statistics
        self.n_arrival_1 += 1

        # state change
        self.n_1 += 1

        # completion event
        t_completion = event_time + self.get_service_time_task_1()
        completion_event = Event(EventType.COMPLETION_CLOUD_TASK_1, t_completion)

        self.t_last_arrival = event_time

        return completion_event

    def submit_arrival_task_2(self, event_time):
        """
        Submit to the Cloud the arrival of a task of type 2.
        :param event_time: (float) the occurrence time of the event.
        :return: (SimpleEvent) the completion event of the submitted task of type 2.
        """
        # record statistics
        self.n_arrival_2 += 1

        # state change
        self.n_2 += 1

        # completion event
        t_completion = event_time + self.get_service_time_task_2()
        completion_event = Event(EventType.COMPLETION_CLOUD_TASK_2, t_completion)

        self.t_last_arrival = event_time

        return completion_event

    def submit_restart_task_2(self, event_time):
        """
        Submit to the Cloud the restart of a task of type 2.
        :param event_time: (float) the occurrence time of the event.
        :return: (float) the completion time for the submitted task.
        """
        # record statistics
        self.n_arrival_2 += 1
        self.n_restarted_2 += 1

        # state change
        self.n_2 += 1

        # completion event
        t_completion = event_time + self.get_service_time_restarted_task_2()
        completion_event = Event(EventType.COMPLETION_CLOUD_TASK_2, t_completion)

        self.t_last_arrival = event_time

        return completion_event

    def submit_completion_task_1(self, event_time):
        """
        Submit to the Cloud the completion of a task of type 1.
        :param event_time: (float) the occurrence time of the event.
        :return: (void)
        """
        # state change
        self.n_1 -= 1

        # record statistics
        self.n_served_1 += 1
        self.t_last_completion = event_time

        if self.n_1 + self.n_2 == 0:
            self.t_last_idle = event_time

    def submit_completion_task_2(self, event_time):
        """
        Submit to the Cloud the completion of a task of type 2.
        :param event_time: (float) the occurrence time of the event.
        :return: (void)
        """
        # state change
        self.n_2 -= 1

        # record statistics
        self.n_served_2 += 1
        self.t_last_completion = event_time

        if self.n_1 + self.n_2 == 0:
            self.t_last_idle = event_time

    def get_service_time_task_1(self):
        """
        Generate the service time for a task of type 1, exponentially distributed with rate *service_rate_1*.
        :return: (float) the service time for a task of type 1 (s).
        """
        self._rndgen.stream(EventType.COMPLETION_CLOUD_TASK_1.value)
        u = self._rndgen.rnd()
        m = 1.0 / self.service_rate_1
        return exponential(m, u)

    def get_service_time_task_2(self):
        """
        Generate the service time for a task of type 2, exponentially distributed with rate *service_rate_2*.
        :return: (float) the service time for a task of type 2 (s).
        """
        self._rndgen.stream(EventType.COMPLETION_CLOUD_TASK_2.value)
        u = self._rndgen.rnd()
        m = 1.0 / self.service_rate_2
        return exponential(m, u)

    def get_service_time_restarted_task_2(self):
        """
        Generate the service time for a restarted task of type 2, exponentially distributed with rate *service_rate_2*.
        :return: (float) the service time for a restarted task of type 2 (s).
        """
        self._rndgen.stream(EventType.COMPLETION_CLOUD_TASK_2.value)
        u = self._rndgen.rnd()
        m = 1.0 / self.service_rate_2
        u_setup = self._rndgen.rnd()
        m_setup = self.t_setup_mean
        return exponential(m, u) + exponential(m_setup, u_setup)

    def __str__(self):
        """
        String representation.
        :return: the string representation.
        """
        sb = ["{attr}='{value}'".format(attr=attr, value=self.__dict__[attr]) for attr in self.__dict__ if not attr.startswith("__") and not callable(getattr(self, attr))]
        return "Cloud({}:{})".format(id(self), ", ".join(sb))

    def __repr__(self):
        """
        String representation.
        :return: the string representation.
        """
        return self.__str__()

    def __eq__(self, other):
        if not isinstance(other, SimpleCloud):
            return False
        return id(self) == id(other)


if __name__ == "__main__":
    from core.random.rndgen import MarcianiMultiStream as RandomGenerator

    rndgen = RandomGenerator(123456789)

    # Creation
    cloud_1 = SimpleCloud(rndgen, 0.25, 0.35, 3)
    print("Cloud 1:", cloud_1)
    cloud_2 = SimpleCloud(rndgen, 0.25, 0.35, 3)
    print("Cloud 2:", cloud_2)

    # Equality check
    print("Cloud 1 equals Cloud 2:", cloud_1 == cloud_2)

    # Service time of tasks of type 1
    for i in range(10):
        t_service_1 = cloud_1.get_service_time_task_1()
        print("service time task 1: ", t_service_1)

    # Service time of tasks of type 2
    for i in range(10):
        t_service_2 = cloud_1.get_service_time_task_2()
        print("sevice time task 2: ", t_service_2)

