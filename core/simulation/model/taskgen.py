from core.simulation.model.event import SimpleEvent as Event
from core.simulation.model.event import EventType
from core.simulation.model.scope import SystemScope
from core.simulation.model.scope import ActionScope
from core.simulation.model.scope import TaskScope
from core.rnd.rndvar import exponential
from core.utils.logutils import get_logger


# Logging
logger = get_logger(__name__)


class ExponentialTaskgen:
    """
    A tasks generator for exponential inter-arrivals.
    """

    def __init__(self, rndgen, config):
        """
        Create a new tasks generator.
        :param rndgen: (object) the multi-stream rnd number generator.
        :param config: (dict) the arrival rates configuration.
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

    def generate(self, t_clock):
        """
        Generate a new rnd arrival.
        :param t_clock: (float) the current time.
        :param tsk: (TaskType) the type of the task. Default: None
        :return: (SimpleEvent) a new rnd arrival.
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


if __name__ == "__main__":
    from core.rnd.rndgen import MarcianiMultiStream
    from core.simulation.model import config

    rndgenerator = MarcianiMultiStream(123456789)
    configuration = config.get_default_configuration()

    taskgen = ExponentialTaskgen(rndgenerator, configuration["arrival"])

    t_clock = 0
    t_stop = 100000

    while t_clock < t_stop:
        event = taskgen.generate(t_clock)
        t_clock = event.time

    rate_task_1 = taskgen.rates[TaskScope.TASK_1]
    rate_task_2 = taskgen.rates[TaskScope.TASK_2]
    rate_total = rate_task_1 + rate_task_2

    probability_task_1 = rate_task_1 / rate_total
    probability_task_2 = rate_task_2 / rate_total

    generated_task_1 = taskgen.generated[TaskScope.TASK_1]
    generated_task_2 = taskgen.generated[TaskScope.TASK_2]
    generated_total = generated_task_1 + generated_task_2

    ratio_generated_tsk_1 = generated_task_1 / generated_total
    ratio_generated_tsk_2 = generated_task_2 / generated_total

    generation_rate_tsk_1 = generated_task_1 / t_stop
    generation_rate_tsk_2 = generated_task_2 / t_stop

    print("rate_task_1: ", rate_task_1)
    print("rate_task_2: ", rate_task_2)
    print("rate_total: ", rate_total)

    print("probability_task_1: ", probability_task_1)
    print("ratio_generated_tsk_1: ", ratio_generated_tsk_1)
    print("generation_rate_tsk_1: ", generation_rate_tsk_1)

    print("probability_task_2: ", probability_task_2)
    print("ratio_generated_tsk_2: ", ratio_generated_tsk_2)
    print("generation_rate_tsk_2: ", generation_rate_tsk_2)
