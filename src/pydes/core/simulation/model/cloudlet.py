import logging

from pydes.core.rnd.rndcmp import RandomComponent
from pydes.core.simulation.model.controller import (
    ControllerAlgorithm,
    ControllerAlgorithm1,
    ControllerAlgorithm2,
)
from pydes.core.simulation.model.event import EventType
from pydes.core.simulation.model.scope import ActionScope, SystemScope, TaskScope
from pydes.core.simulation.model.server import SimpleServer as Server

# Logging
logger = logging.getLogger(__name__)


class SimpleCloudlet:
    """
    A Cloudlet subsystem.
    """

    def __init__(self, rndgen, config, state, metrics):
        """
        Create a new Cloudlet.
        :param rndgen: (object) the multi-stream rnd number generator.
        :param config: (dict) the Cloudlet configuration.
        :param state: (dict) the Cloudlet state.
        :param metrics: (SimulationMetrics) the simulation metrics.
        """
        # Randomization - Service
        self.rndservice = RandomComponent(
            gen=rndgen,
            str={
                tsk: EventType.of(ActionScope.COMPLETION, SystemScope.CLOUDLET, tsk).value
                for tsk in TaskScope.concrete()
            },
            var={tsk: config["service"][tsk]["distribution"] for tsk in TaskScope.concrete()},
            par={tsk: config["service"][tsk]["parameters"] for tsk in TaskScope.concrete()},
        )

        # Servers
        self.n_servers = config["n_servers"]
        self.servers = [Server(self.rndservice, i) for i in range(self.n_servers)]
        self.server_selector = config["server_selection"].selector(self.servers)

        # State
        self.state = state

        # Controller
        controller_algorithm = config["controller_algorithm"]
        if controller_algorithm is ControllerAlgorithm.ALGORITHM_1:
            self.controller = ControllerAlgorithm1(self.state, self.n_servers)
        elif controller_algorithm is ControllerAlgorithm.ALGORITHM_2:
            self.threshold = config["threshold"]
            self.controller = ControllerAlgorithm2(self.state, self.n_servers, self.threshold)
            if not (0 <= self.threshold <= self.n_servers):
                raise ValueError(
                    "Invalid threshold: should be >= 0 and <= n_servers, but threshold is {} and n_servers is {}".format(
                        self.threshold, self.n_servers
                    )
                )
        else:
            raise ValueError("Unrecognized controller algorithm type {}".format(controller_algorithm))

        # Timing
        self.t_last_event = {tsk: 0.0 for tsk in TaskScope.concrete()}

        # Metrics
        self.metrics = metrics

    # ==================================================================================================================
    # EVENT SUBMISSION
    #   * ARRIVAL
    #   * INTERRUPTION
    #   * COMPLETION
    # ==================================================================================================================

    def submit_arrival(self, tsk, t_now):
        """
        Submit the arrival of a task.
        :param tsk: (TaskType) the type of the task.
        :param t_now: (float) the current time.
        :return: (float) the completion time.
        """
        # Check correctness
        assert sum(self.state[tsk] for tsk in TaskScope.concrete()) < self.n_servers

        # Generate completion
        server_idx = self.server_selector.select_idle()
        if server_idx is None:
            raise RuntimeError("Cannot find server for arrival of task {} at time {}".format(tsk, t_now))
        t_completion = self.servers[server_idx].submit_arrival(tsk, t_now)

        # Update metrics
        self.metrics.counters.arrived[SystemScope.CLOUDLET][tsk] += 1
        self.metrics.counters.population_area[SystemScope.CLOUDLET][tsk] += (
            t_now - self.t_last_event[tsk]
        ) * self.state[tsk]

        # Update state
        self.state[tsk] += 1

        # Update timing
        self.t_last_event[tsk] = t_now

        return t_completion

    def submit_interruption(self, tsk, t_now):
        """
        Submit the interruption of a task.
        :param tsk: (TaskType) the type of the task.
        :param t_now: (float) the current time.
        :return: (c,w,s,r) where
        *c* is the completion time to ignore;
        *a* is the arrival time;
        *r* is the remaining service time ratio;
        """
        # Check correctness
        assert self.state[tsk] > 0

        # Compute served time
        server_idx = self.server_selector.select_interruption(tsk)
        if server_idx is None:
            raise RuntimeError("Cannot find server for interruption of task {} at time {}".format(tsk, t_now))
        t_completion_to_ignore, t_arrival = self.servers[server_idx].submit_interruption(tsk, t_now)
        t_served = t_now - t_arrival

        # Update metrics
        self.metrics.counters.switched[SystemScope.CLOUDLET][tsk] += 1
        self.metrics.counters.switched_service_lost[SystemScope.CLOUDLET][tsk] += t_served
        self.metrics.counters.service[SystemScope.CLOUDLET][tsk] += t_served
        self.metrics.counters.population_area[SystemScope.CLOUDLET][tsk] += (
            t_now - self.t_last_event[tsk]
        ) * self.state[tsk]

        # Update state
        self.state[tsk] -= 1

        # Update timing
        self.t_last_event[tsk] = t_now

        return t_completion_to_ignore, t_arrival

    def submit_completion(self, tsk, t_now, t_arrival):
        """
        Submit the completion of a task.
        :param tsk: (TaskType) the type of the task.
        :param t_now: (float) the completion time.
        :param t_arrival: (float) the arrival time.
        :return: None
        """
        # Check correctness
        assert self.state[tsk] > 0

        # Compute served time
        server_idx = self.find_completion_server_idx(tsk, t_now)
        if server_idx is None:
            raise RuntimeError("Cannot find server for completion of task {} at time {}".format(tsk, t_now))
        self.servers[server_idx].submit_completion()
        t_served = t_now - t_arrival

        # Update metrics
        self.metrics.counters.completed[SystemScope.CLOUDLET][tsk] += 1
        self.metrics.counters.service[SystemScope.CLOUDLET][tsk] += t_served
        self.metrics.counters.population_area[SystemScope.CLOUDLET][tsk] += (
            t_now - self.t_last_event[tsk]
        ) * self.state[tsk]

        # Update state
        self.state[tsk] -= 1

        # Update timing
        self.t_last_event[tsk] = t_now

    # ==================================================================================================================
    # OTHER
    # ==================================================================================================================

    def is_idle(self):
        """
        Check weather the Cloudlet is idle or not.
        :return: True, if the Cloudlet is idle; False, otherwise.
        """
        return sum(self.state[tsk] for tsk in TaskScope.concrete()) == 0

    def find_completion_server_idx(self, task_type, t_completion):
        """
        Select a completion server for the given task type and time.
        :param task_type: (TaskType) the type of task.
        :param t_completion: (float) the completion time.
        :return: (int) the index of the completion server, if present; None, otherwise.
        """
        for idx, server in enumerate(self.servers):
            if server.task_type is task_type and server.t_completion == t_completion:
                return idx
        return None

    def __str__(self):
        """
        String representation.
        :return: the string representation.
        """
        sb = [
            "{attr}={value}".format(attr=attr, value=self.__dict__[attr])
            for attr in self.__dict__
            if not attr.startswith("__") and not callable(getattr(self, attr))
        ]
        return "Cloudlet({}:{})".format(id(self), ", ".join(sb))
