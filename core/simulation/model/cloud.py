from core.simulation.model.event import EventType
from core.simulation.model.scope import SystemScope
from core.simulation.model.scope import ActionScope
from core.random.rndcmp import RandomComponent
import logging

# Logging
from core.simulation.model.scope import TaskScope

logger = logging.getLogger(__name__)


class SimpleCloud:
    """
    A Cloud subsystem.
    """

    def __init__(self, rndgen, config, state, statistics):
        """
        Create a new Cloud server.
        :param rndgen: (object) the multi-stream random number generator.
        :param config: (dict) the configuration.
        :param state: the system state.
        :param statistics: the system statistics.
        """

        # Randomization - Service
        self.rndservice = RandomComponent(
            gen=rndgen,
            str={tsk: EventType.of(ActionScope.COMPLETION, SystemScope.CLOUD, tsk).value for tsk in TaskScope.concrete()},
            var={tsk: config["service"][tsk]["distribution"] for tsk in TaskScope.concrete()},
            par={tsk: config["service"][tsk]["parameters"] for tsk in TaskScope.concrete()}
        )

        # Randomization - Setup
        self.rndsetup = RandomComponent(
            gen=rndgen,
            str={tsk: EventType.of(ActionScope.RESTART, SystemScope.CLOUD, tsk).value for tsk in TaskScope.concrete()},
            var={tsk: config["setup"][tsk]["distribution"] for tsk in TaskScope.concrete()},
            par={tsk: config["setup"][tsk]["parameters"] for tsk in TaskScope.concrete()}
        )

        # State
        self.state = state

        # Statistics
        self.statistics = statistics

    # ==================================================================================================================
    # EVENT SUBMISSION
    #   * ARRIVAL
    #   * RESTART
    #   * COMPLETION
    # ==================================================================================================================

    def submit_arrival(self, tsk, t_now, restart=False):
        """
        Submit to the Cloud the arrival of a task.
        :param tsk: (TaskType) the type of the task.
        :param t_now: (float) the current time.
        :param restart: (bool) if True, the arrival is a restarted task.
        :return: (float) the completion time.
        """
        # Update state
        self.state[tsk] += 1

        # Generate completion
        t_service = self.rndservice.generate(tsk) + (0.0 if not restart else self.rndsetup.generate(tsk))
        t_completion = t_now + t_service

        # Update statistics
        self.statistics.metrics.arrived[SystemScope.CLOUD][tsk].increment(1)
        if restart:
            self.statistics.metrics.switched[SystemScope.CLOUD][tsk].increment(1)
        self.sample_mean_population()

        return t_completion

    def submit_completion(self, tsk, t_now, t_arrival, switched=False):
        """
        Submit to the Cloud the completion of a task.
        :param tsk: (TaskType) the type of the task.
        :param t_now: (float) the completion time.
        :param t_arrival: (float) the arrival time.
        :param switched: (bool) True if the completion is associated to a switched task.
        :return: None
        """
        # Check correctness
        assert self.state[tsk] > 0

        # Update state
        self.state[tsk] -= 1

        t_served = t_now - t_arrival

        # Update statistics
        self.statistics.metrics.completed[SystemScope.CLOUD][tsk].increment(1)
        self.statistics.metrics.service[SystemScope.CLOUD][tsk].increment(t_served)
        if switched:
            self.statistics.metrics.switched_completed[SystemScope.CLOUD][tsk].increment(1)
            self.statistics.metrics.switched_service[SystemScope.CLOUD][tsk].increment(t_served)
        self.sample_mean_population()

    # ==================================================================================================================
    # OTHER
    # ==================================================================================================================
    def is_idle(self):
        """
        Check weather the Cloud is idle or not.
        :return: True, if the Cloud is idle; False, otherwise.
        """
        return sum(self.state[tsk] for tsk in TaskScope.concrete()) == 0

    def sample_mean_population(self):
        """
        Register the sample for the mean population.
        :return: None.
        """
        for tsk in TaskScope.concrete():
            self.statistics.metrics.population[SystemScope.CLOUD][tsk].add_sample(self.state[tsk])
        self.statistics.metrics.population[SystemScope.CLOUD][TaskScope.GLOBAL].add_sample(
            sum(self.state[tsk] for tsk in TaskScope.concrete()))

    def __str__(self):
        """
        String representation.
        :return: the string representation.
        """
        sb = ["{attr}={value}".format(attr=attr, value=self.__dict__[attr]) for attr in self.__dict__ if
              not attr.startswith("__") and not callable(getattr(self, attr))]
        return "Cloud({}:{})".format(id(self), ", ".join(sb))