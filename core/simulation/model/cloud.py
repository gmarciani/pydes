from core.simulation.model.event import EventType
from core.simulation.model.scope import SystemScope
from core.simulation.model.scope import ActionScope
from core.rnd.rndcmp import RandomComponent
import logging

# Logging
from core.simulation.model.scope import TaskScope

logger = logging.getLogger(__name__)


class SimpleCloud:
    """
    A Cloud subsystem.
    """

    def __init__(self, rndgen, config, state, metrics):
        """
        Create a new Cloud server.
        :param rndgen: (object) the multi-stream rnd number generator.
        :param config: (dict) the Cloud configuration.
        :param state: (dict) the Cloud state.
        :param metrics: (SimulationMetrics) the simulation metrics.
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

        # Timing
        self.t_last_event = {tsk: 0.0 for tsk in TaskScope.concrete()}

        # Metrics
        self.metrics = metrics

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
        # Generate completion
        t_service = self.rndservice.generate(tsk) + (0.0 if not restart else self.rndsetup.generate(tsk))
        t_completion = t_now + t_service

        # Update statistics
        self.metrics.counters.arrived[SystemScope.CLOUD][tsk] += 1
        if restart:
            self.metrics.counters.switched[SystemScope.CLOUD][tsk] += 1
        self.metrics.counters.population_area[SystemScope.CLOUD][tsk] += (t_now - self.t_last_event[tsk]) * self.state[tsk]

        # Update state
        self.state[tsk] += 1

        # Update timing
        self.t_last_event[tsk] = t_now

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

        # Compute served time
        t_served = t_now - t_arrival

        # Update statistics
        self.metrics.counters.completed[SystemScope.CLOUD][tsk] += 1
        self.metrics.counters.service[SystemScope.CLOUD][tsk] += t_served
        if switched:
            self.metrics.counters.switched_completed[SystemScope.CLOUD][tsk] += 1
            self.metrics.counters.switched_service[SystemScope.CLOUD][tsk] += t_served
        self.metrics.counters.population_area[SystemScope.CLOUD][tsk] += (t_now - self.t_last_event[tsk]) * self.state[tsk]

        # Update state
        self.state[tsk] -= 1

        # Update timing
        self.t_last_event[tsk] = t_now

    # ==================================================================================================================
    # OTHER
    # ==================================================================================================================
    def is_idle(self):
        """
        Check weather the Cloud is idle or not.
        :return: True, if the Cloud is idle; False, otherwise.
        """
        return sum(self.state[tsk] for tsk in TaskScope.concrete()) == 0

    def __str__(self):
        """
        String representation.
        :return: the string representation.
        """
        sb = ["{attr}={value}".format(attr=attr, value=self.__dict__[attr]) for attr in self.__dict__ if
              not attr.startswith("__") and not callable(getattr(self, attr))]
        return "Cloud({}:{})".format(id(self), ", ".join(sb))