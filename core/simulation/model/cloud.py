from core.simulation.model.event import EventType
from core.simulation.model.scope import SystemScope
from core.simulation.model.scope import TaskScope
from core.simulation.model.scope import ActionScope
from core.random.rndvar import exponential
import logging

# Configure logger
from core.simulation.model.scope import TaskScope

logger = logging.getLogger(__name__)


class SimpleCloud:
    """
    A simple Cloud server, defined by its state.
    """

    def __init__(self, rndgen, config, state, statistics):
        """
        Create a new Cloud server.
        :param rndgen: (object) the multi-stream random number generator.
        :param config: (dict) the configuration.
        :param state: the system state.
        :param statistics: the system statistics.
        """
        # Service rates
        #self.rates = {tsk: config["service_rate_{}".format(tsk.value)] for tsk in TaskScope.concrete()}

        # Setup
        #self.setup_mean = config["t_setup_mean"]

        # Randomization
        self.rndgen = rndgen
        self.streams = {tsk: EventType.of(ActionScope.COMPLETION, SystemScope.CLOUD, tsk).value for tsk in TaskScope.concrete()}
        self.streams[EventType.SWITCH_TASK_2] = EventType.SWITCH_TASK_2.value

        # State
        self.state = state

        # Statistics
        self.statistics = statistics

    # ==================================================================================================================
    # EVENT SUBMISSION
    #   * ARRIVAL_TASK_1
    #   * ARRIVAL_TASK_2
    #   * RESTART_CLOUD_TASK_2
    #   * COMPLETION_CLOUD_TASK_1
    #   * COMPLETION_CLOUD_TASK_2
    # ==================================================================================================================

    def submit_arrival(self, task_type, t_arrival):
        """
        Submit to the Cloud the arrival of a task.
        :param task_type: (TaskType) the type of the task.
        :param t_arrival: (float) the arrival time.
        :return: (float) the completion time.
        """
        # Update state
        self.state[task_type] += 1

        # Generate completion
        t_service = self.get_service_time(task_type)
        t_completion = t_arrival + t_service

        # Update statistics
        self.statistics.metrics.arrived[SystemScope.CLOUD][task_type].increment(1)
        #self.statistics.metrics.population[SystemScope.CLOUD][task_type].add_sample(self.state[task_type])

        return t_completion

    def submit_restart(self, task_type, t_arrival, ratio_remaining):
        """
        Submit to the Cloud the restart of a task.
        :param task_type: (TaskType) the type of the task.
        :param t_arrival: (float) the arrival time.
        :param ratio_remaining: (float) the remaining ratio.
        :return: (float) the completion time.
        """
        # Update state
        self.state[task_type] += 1

        # Generate completion
        t_setup = self.get_setup_time()
        t_service = ratio_remaining * self.get_service_time(task_type) + t_setup
        t_completion = t_arrival + t_service

        # Update statistics
        self.statistics.metrics.switched[SystemScope.CLOUD][task_type].increment(1)
        #self.statistics.metrics.population[SystemScope.CLOUD][task_type].add_sample(self.state[task_type])

        return t_completion

    def submit_completion(self, task_type, t_completion, t_arrival, switched=False):
        """
        Submit to the Cloud the completion of a task.
        :param task_type: (TaskType) the type of the task.
        :param t_completion: (float) the completion time.
        :param t_arrival: (float) the arrival time.
        :param switched: (bool) True if the completion is associated to a switched task.
        :return: None
        """
        # Check correctness
        assert self.state[task_type] > 0

        # Update state
        self.state[task_type] -= 1

        # Update statistics
        self.statistics.metrics.completed[SystemScope.CLOUD][task_type].increment(1)
        self.statistics.metrics.service[SystemScope.CLOUD][task_type].increment(t_completion - t_arrival)
        if switched:
            self.statistics.metrics.switched_completed[SystemScope.CLOUD][task_type].increment(1)
            self.statistics.metrics.switched_service[SystemScope.CLOUD][task_type].increment(t_completion - t_arrival)
        #self.statistics.metrics.population[SystemScope.CLOUD][task_type].add_sample(self.state[task_type])

    # ==================================================================================================================
    # RANDOM TIME GENERATION
    #   * service time
    #   * setup time
    # ==================================================================================================================

    def get_service_time(self, task_type):
        """
        Generate the service time for a task.
        :param task_type: (TaskType) the type of the task.
        :return: (float) the service time for a task of type 1 (s).
        """
        self.rndgen.stream(self.streams[task_type])
        return exponential(1.0 / self.rates[task_type], self.rndgen.rnd())

    def get_setup_time(self):
        """
        Generate the setup time for a restarted task.
        :return: (float) the setup time for a restarted task.
        """
        self.rndgen.stream(self.streams[EventType.SWITCH_TASK_2])
        return exponential(self.setup_mean, self.rndgen.rnd())

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