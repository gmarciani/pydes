from core.random.rndvar import Variate
from core.simulation.model.event import SimpleEvent as Event
from core.simulation.model.event import EventType
from core.simulation.model.scope import SystemScope
from core.simulation.model.scope import ActionScope
from core.simulation.model.scope import TaskScope
from core.random.rndcmp import RandomComponent
from sys import maxsize
from core.utils.logutils import get_logger


# Logging
logger = get_logger(__name__)


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

        # Randomization
        self.rndarrival = RandomComponent(
            gen=rndgen,
            str={tsk: EventType.of(ActionScope.ARRIVAL, SystemScope.SYSTEM, tsk).value for tsk in TaskScope.concrete()},
            var={tsk: Variate[config[tsk.name]["distribution"]] for tsk in TaskScope.concrete()},
            par={tsk: config[tsk.name]["parameters"] for tsk in TaskScope.concrete()}
        )

        # Events
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
        arrival_time = t_clock + self.rndarrival.generate(tsk)
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