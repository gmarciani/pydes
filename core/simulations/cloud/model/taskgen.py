from core.simulations.cloud.model.event import SimpleEvent as Event
from core.simulations.cloud.model.event import EventType
from core.rnd.rndvar import exponential
import logging

# Configure logger
logger = logging.getLogger(__name__)


class SimpleTaskgen:
    """
    A simple tasks generator.
    """

    def __init__(self, rndgen, arrival_rate_1, arrival_rate_2):
        """
        Create a new tasks generator.
        :param rndgen: (object) the multi-stream random number generator.
        :param arrival_rate_1: (float) the arrival rate for tasks of type 1 (tasks/s).
        :param arrival_rate_2: (float) the arrival rate for tasks of type 2 (tasks/s).
        """
        self._rndgen = rndgen
        self.arrival_rate_1 = arrival_rate_1
        self.arrival_rate_2 = arrival_rate_2

        # state
        self.n_tasks_1 = 0  # total number of generated tasks of type 1
        self.n_tasks_2 = 0  # total number of generated tasks of type 2

    def generate_new_arrival_1(self, t_clock):
        """
        Generate a new random arrival for a task of type 1.
        :param t_clock: (float) the current time.
        :return: (SimpleEvent) a new random arrival for a task of type 1.
        """
        arrival_time = t_clock + self.get_inter_arrival_task_1()
        arrival = Event(EventType.ARRIVAL_TASK_1, arrival_time)

        # state change
        self.n_tasks_1 += 1

        return arrival

    def generate_new_arrival_2(self, t_clock):
        """
        Generate a new random arrival for a task of type 2.
        :param t_clock: (float) the current time.
        :return: (SimpleEvent) a new random arrival for a task of type 2.
        """
        arrival_time = t_clock + self.get_inter_arrival_task_2()
        arrival = Event(EventType.ARRIVAL_TASK_2, arrival_time)

        # state change
        self.n_tasks_2 += 1

        return arrival

    def get_inter_arrival_task_1(self):
        """
        Generate an inter-arrival time for task of type 1, exponentially distributed with rate *arrival_rate_1*.
        :return: the inter-arrival time for task of type 1 (s).
        """
        self._rndgen.stream(EventType.ARRIVAL_TASK_1.value)
        u = self._rndgen.rnd()
        m = 1.0 / self.arrival_rate_1
        return exponential(m, u)

    def get_inter_arrival_task_2(self):
        """
        Generate an inter-arrival time for task of type 2, exponentially distributed with rate *arrival_rate_2*.
        :return: the inter-arrival time for task of type 2 (s).
        """
        self._rndgen.stream(EventType.ARRIVAL_TASK_2.value)
        u = self._rndgen.rnd()
        m = 1.0 / self.arrival_rate_1
        return exponential(m, u)

    def __str__(self):
        """
        String representation.
        :return: the string representation.
        """
        sb = ["{attr}='{value}'".format(attr=attr, value=self.__dict__[attr]) for attr in self.__dict__ if not attr.startswith("__") and not callable(getattr(self, attr))]
        return "Taskgen({}:{})".format(id(self), ", ".join(sb))

    def __repr__(self):
        """
        String representation.
        :return: the string representation.
        """
        return self.__str__()

    def __eq__(self, other):
        if not isinstance(other, SimpleTaskgen):
            return False
        return self._rndgen == other._rndgen and \
               self.arrival_rate_1 == other.arrival_rate_1 and \
               self.arrival_rate_2 == other.arrival_rate_2


if __name__ == "__main__":
    from core.rnd.rndgen import MarcianiMultiStream as RandomGenerator

    rndgen = RandomGenerator(123456789)

    # Creation
    taskgen_1 = SimpleTaskgen(rndgen, 0.5, 0.25)
    print("Taskgen 1:", taskgen_1)
    taskgen_2 = SimpleTaskgen(rndgen, 0.5, 0.25)
    print("Taskgen 2:", taskgen_2)
    taskgen_3 = SimpleTaskgen(rndgen, 0.25, 0.125)
    print("Taskgen 3:", taskgen_3)

    # Equality check
    print("Taskgen 1 equals Taskgen 2:", taskgen_1 == taskgen_2)
    print("Taskgen 1 equals Taskgen 3:", taskgen_1 == taskgen_3)

    # Inter-arrivals of tasks of type 1
    for i in range(10):
        t_inter_arrival_1 = taskgen_1.get_inter_arrival_task_1()
        print("inter-arrival task 1: ", t_inter_arrival_1)

    # Inter-arrivals of tasks of type 2
    for i in range(10):
        t_inter_arrival_2 = taskgen_1.get_inter_arrival_task_2()
        print("inter-arrival task 2: ", t_inter_arrival_2)