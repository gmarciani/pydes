from core.random.rndvar import Variate
from core.simulation.model.event import SimpleEvent as Event
from core.simulation.model.event import EventType
from core.simulation.model.scope import SystemScope
from core.simulation.model.scope import ActionScope
from core.simulation.model.scope import TaskScope
from core.random.rndcmp import RandomComponent
from core.random.rndvar import exponential
from sys import maxsize
from core.utils.logutils import get_logger


# Logging
logger = get_logger(__name__)


class ExponentialTaskgen:
    """
    A tasks generator for exponential inter-arrivals.
    """

    def __init__(self, rndgen, config, t_stop=maxsize):
        """
        Create a new tasks generator.
        :param rndgen: (object) the multi-stream random number generator.
        :param config: (dict) the arrival rates configuration.
        :param t_stop: (float) the final stop time. Events with arrival time greater than stop time are not counted in
        taskgen tate.
        """
        # Arrival rates
        self.rates = {tsk: 1.0 / config[tsk]["parameters"]["m"] for tsk in TaskScope.concrete()}

        # Randomization
        self.rndgen = rndgen
        self.stream = {tsk: EventType.of(ActionScope.ARRIVAL, SystemScope.SYSTEM, tsk).value for tsk in TaskScope}
        self.lambda_tot = sum(self.rates[tsk] for tsk in TaskScope.concrete())
        self.p_1 = self.rates[TaskScope.TASK_1] / self.lambda_tot

        # Events
        self.event_types = {tsk: EventType.of(ActionScope.ARRIVAL, SystemScope.SYSTEM, tsk) for tsk in TaskScope.concrete()}

        # State
        self.generated = {tsk: 0 for tsk in TaskScope.concrete()}

        # Generation management
        self.t_stop = t_stop

    def generate(self, t_clock):
        """
        Generate a new random arrival.
        :param t_clock: (float) the current time.
        :param tsk: (TaskType) the type of the task. Default: None
        :return: (SimpleEvent) a new random arrival.
        """
        # Select the type of arrival and the corresponding arrival time
        self.rndgen.stream(self.stream[TaskScope.GLOBAL])
        u = self.rndgen.rnd()
        tsk = TaskScope.TASK_1 if u <= self.p_1 else TaskScope.TASK_2
        self.rndgen.stream(self.stream[tsk])
        t_event = t_clock + exponential(m=(1.0 / self.lambda_tot), u=self.rndgen.rnd())

        # Generate the arrival event
        arrival = Event(self.event_types[tsk], t_event)

        # Update state
        if t_event < self.t_stop:
            self.generated[tsk] += 1

        return arrival

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
        return "Taskgen({}:{})".format(id(self), ", ".join(sb))


class GeneralTaskgen:
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
        self.rndgen = rndgen
        self.rndarrival = RandomComponent(
            gen=rndgen,
            str={tsk: EventType.of(ActionScope.ARRIVAL, SystemScope.SYSTEM, tsk).value for tsk in TaskScope.concrete()},
            var={tsk: config[tsk.name]["distribution"] for tsk in TaskScope.concrete()},
            par={tsk: config[tsk.name]["parameters"] for tsk in TaskScope.concrete()}
        )

        # Events
        self.event_types = {tsk: EventType.of(ActionScope.ARRIVAL, SystemScope.SYSTEM, tsk) for tsk in TaskScope.concrete()}

        # State
        self.generated = {tsk: 0 for tsk in TaskScope.concrete()}

        # Generation management
        self.t_stop = t_stop
        if all(var is Variate.EXPONENTIAL for var in self.rndarrival.var.values()):
            self.lambda_tot = sum(1.0 / self.rndarrival.par[tsk]["m"] for tsk in TaskScope.concrete())
            self.p_1 = (1.0 / self.rndarrival.par[TaskScope.TASK_1]["m"]) / self.lambda_tot
            self._generate = self._generate_exponential
        else:
            raise NotImplementedError("The type selection for general arrival process has not been implemented, yet.")

    def generate(self, t_clock):
        """
        Generate a new random arrival.
        :param t_clock: (float) the current time.
        :param tsk: (TaskType) the type of the task. Default: None
        :return: (SimpleEvent) a new random arrival.
        """
        # Select the type of arrival and the corresponding arrival time
        tsk, t_event = self._generate(t_clock)

        # Generate the arrival event
        arrival = Event(self.event_types[tsk], t_event)

        # Update state
        if t_event < self.t_stop:
            self.generated[tsk] += 1

        return arrival

    def _generate_exponential(self, t_clock):
        """
        Generate random arrival event for exponential arrival process.
        :param t_clock: (float) the current time.
        :return: tsk, t_event
        """
        self.rndgen.stream(STREAM_ARRIVAL_TYPE)
        u = self.rndgen.rnd()
        tsk = TaskScope.TASK_1 if u <= self.p_1 else TaskScope.TASK_2
        t_event = t_clock + exponential(m=(1.0 / self.lambda_tot), u=self.rndgen.rnd())
        return tsk, t_event

    def _generate_general(self, t_clock):
        """
        Generate random arrival event for general arrival process.
        :param t_clock: (float) the current time.
        :return: tsk, t_event
        """
        raise NotImplementedError("The type selection for general arrival process has not been implemented, yet.")

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
        return "Taskgen({}:{})".format(id(self), ", ".join(sb))