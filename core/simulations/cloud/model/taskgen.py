from core.simulations.cloud.model.event import SimpleEvent as Event
from core.simulations.cloud.model.event import EventType
from core.random.rndvar import exponential
from sys import maxsize
import logging

# Configure logger
logger = logging.getLogger(__name__)


class SimpleTaskgen:
    """
    A simple tasks generator.
    """

    def __init__(self, rndgen, arrival_rate_1, arrival_rate_2, t_stop=maxsize):
        """
        Create a new tasks generator.
        :param rndgen: (object) the multi-stream random number generator.
        :param arrival_rate_1: (float) the arrival rate for tasks of type 1 (tasks/s).
        :param arrival_rate_2: (float) the arrival rate for tasks of type 2 (tasks/s).
        :param t_stop: (float) the final stop time. Events with arrival time greater than stop time are not counted in
        taskgen tate.
        """
        self._rndgen = rndgen
        self.arrival_rate_1 = arrival_rate_1
        self.arrival_rate_2 = arrival_rate_2
        self.t_stop = t_stop

        # state
        self.n_generated_1 = 0  # total number of generated tasks of type 1
        self.n_generated_2 = 0  # total number of generated tasks of type 2

    def generate_new_arrival_1(self, t_clock):
        """
        Generate a new random arrival for a task of type 1.
        :param t_clock: (float) the current time.
        :return: (SimpleEvent) a new random arrival for a task of type 1.
        """
        self._rndgen.stream(EventType.ARRIVAL_TASK_1.value)
        inter_arrival_time = exponential(1.0 / self.arrival_rate_1, self._rndgen.rnd())
        arrival_time = t_clock + inter_arrival_time
        arrival = Event(EventType.ARRIVAL_TASK_1, arrival_time)

        # state change
        if arrival_time < self.t_stop:
            self.n_generated_1 += 1

        return arrival

    def generate_new_arrival_2(self, t_clock):
        """
        Generate a new random arrival for a task of type 2.
        :param t_clock: (float) the current time.
        :return: (SimpleEvent) a new random arrival for a task of type 2.
        """
        self._rndgen.stream(EventType.ARRIVAL_TASK_2.value)
        inter_arrival_time = exponential(1.0 / self.arrival_rate_2, self._rndgen.rnd())
        arrival_time = t_clock + inter_arrival_time
        arrival = Event(EventType.ARRIVAL_TASK_2, arrival_time)

        # state change
        if arrival_time < self.t_stop:
            self.n_generated_2 += 1

        return arrival

    def __str__(self):
        """
        String representation.
        :return: the string representation.
        """
        sb = ["{attr}={value}".format(attr=attr, value=self.__dict__[attr]) for attr in self.__dict__ if
              not attr.startswith("__") and not callable(getattr(self, attr))]
        return "Taskgen({}:{})".format(id(self), ", ".join(sb))