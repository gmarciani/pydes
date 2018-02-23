from core.simulation.model.event import SimpleEvent as Event
from core.simulation.model.event import EventType
from core.random.rndvar import exponential
from sys import maxsize
import logging

# Configure logger
from core.simulation.model.task import Task

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
        self.t_stop = t_stop

        self.rates = {
            Task.TASK_1: arrival_rate_1,
            Task.TASK_2: arrival_rate_2
        }

        self.streams = {
            Task.TASK_1: EventType.ARRIVAL_TASK_1.value,
            Task.TASK_2: EventType.ARRIVAL_TASK_2.value
        }

        self.event_types = {
            Task.TASK_1: EventType.ARRIVAL_TASK_1,
            Task.TASK_2: EventType.ARRIVAL_TASK_2
        }

        # state
        self.generated = {
            Task.TASK_1: 0,  # total number of generated tasks of type 1
            Task.TASK_2: 0  # total number of generated tasks of type 2
        }

    def generate(self, task_type, t_clock):
        """
        Generate a new random task arrival of the specified type.
        :param task_type: (TaskType) the type of the task.
        :param t_clock: (float) the current time.
        :return: (SimpleEvent) a new random arrival of the specified type.
        """
        self._rndgen.stream(self.streams.get(task_type))
        inter_arrival_time = exponential(1.0 / self.rates[task_type], self._rndgen.rnd())
        arrival_time = t_clock + inter_arrival_time
        event_type = self.event_types[task_type]
        arrival = Event(event_type, arrival_time)

        # state change
        if arrival_time < self.t_stop:
            self.generated[task_type] += 1

        return arrival

    def __str__(self):
        """
        String representation.
        :return: the string representation.
        """
        sb = ["{attr}={value}".format(attr=attr, value=self.__dict__[attr]) for attr in self.__dict__ if
              not attr.startswith("__") and not callable(getattr(self, attr))]
        return "Taskgen({}:{})".format(id(self), ", ".join(sb))