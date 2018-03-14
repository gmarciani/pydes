from core.simulation.model.event import SimpleEvent as Event
from core.simulation.model.event import EventType
from core.simulation.model.scope import SystemScope
from core.simulation.model.scope import TaskScope
from core.simulation.model.scope import ActionScope
from core.random.rndvar import exponential
from sys import maxsize
import logging

# Configure logger
from core.simulation.model.scope import TaskScope

logger = logging.getLogger(__name__)


class SimpleTaskgen:
    """
    A simple tasks generator.
    """

    def __init__(self, rndgen, config, t_stop=maxsize):
        """
        Create a new tasks generator.
        :param rndgen: (object) the multi-stream random number generator.
        :param config: (dict) the configuration.
        :param t_stop: (float) the final stop time. Events with arrival time greater than stop time are not counted in
        taskgen tate.
        """
        # Arrival rates
        self.rates = {tsk: config["arrival_rate_{}".format(tsk.value)] for tsk in TaskScope.concrete()}

        # Randomization
        self.rndgen = rndgen
        self.streams = {tsk: EventType.of(ActionScope.ARRIVAL, SystemScope.SYSTEM, tsk).value for tsk in TaskScope.concrete()}

        self.event_types = {tsk: EventType.of(ActionScope.ARRIVAL, SystemScope.SYSTEM, tsk) for tsk in TaskScope.concrete()}

        # State
        self.generated = {tsk: 0 for tsk in TaskScope.concrete()}

        # Generation management
        self.t_stop = t_stop

    def generate(self, tsk, t_clock):
        """
        Generate a new random task arrival of the specified type.
        :param tsk: (TaskType) the type of the task.
        :param t_clock: (float) the current time.
        :return: (SimpleEvent) a new random arrival of the specified type.
        """
        self.rndgen.stream(self.streams.get(tsk))
        inter_arrival_time = exponential(1.0 / self.rates[tsk], self.rndgen.rnd())
        arrival_time = t_clock + inter_arrival_time
        event_type = self.event_types[tsk]
        arrival = Event(event_type, arrival_time)

        # state change
        if arrival_time < self.t_stop:
            self.generated[tsk] += 1

        return arrival

    def __str__(self):
        """
        String representation.
        :return: the string representation.
        """
        sb = ["{attr}={value}".format(attr=attr, value=self.__dict__[attr]) for attr in self.__dict__ if
              not attr.startswith("__") and not callable(getattr(self, attr))]
        return "Taskgen({}:{})".format(id(self), ", ".join(sb))