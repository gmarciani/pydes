from core.simulation.model.server import SimpleServer as Server
from core.simulation.model.event import EventType
from core.simulation.model.scope import SystemScope
from core.simulation.model.scope import ActionScope
from core.simulation.model.scope import TaskScope
from core.random.rndcmp import RandomComponent
from core.random.rndvar import Variate
from core.simulation.model.server_selection import SelectionRule
import logging

# Logging
logger = logging.getLogger(__name__)


class SimpleCloudlet:
    """
    A Cloudlet subsystem.
    """

    def __init__(self, rndgen, config, state, statistics):
        """
        Create a new Cloudlet.
        :param rndgen: (object) the multi-stream random number generator.
        :param config: (dict) the configuration.
        :param state: the system state.
        :param statistics: the system statistics.
        """
        # Randomization - Service
        self.rndservice = RandomComponent(
            gen=rndgen,
            str={tsk: EventType.of(ActionScope.COMPLETION, SystemScope.CLOUDLET, tsk).value for tsk in
                 TaskScope.concrete()},
            var={tsk: Variate[config["service"][tsk.name]["distribution"]] for tsk in TaskScope.concrete()},
            par={tsk: config["service"][tsk.name]["parameters"] for tsk in TaskScope.concrete()}
        )

        # Servers
        self.n_servers = config["n_servers"]
        self.threshold = config["threshold"]
        self.servers = [Server(self.rndservice, i) for i in range(self.n_servers)]
        self.server_selector = SelectionRule[config["server_selection"]].selector(self.servers)

        if not (0 <= self.threshold <= self.n_servers):
            raise ValueError(
                "Invalid threhsold: should be >= 0 and <= n_servers, but threshold is {} and n_servers is {}".format(
                    self.threshold, self.n_servers))

        # State
        self.state = state

        # Statistics
        self.statistics = statistics

    # ==================================================================================================================
    # EVENT SUBMISSION
    #   * ARRIVAL (TASK_1 | TASK_2)
    #   * INTERRUPTION (TASK_1 | TASK_2)
    #   * COMPLETION (TASK_1 | TASK_2)
    # ==================================================================================================================

    def submit_arrival(self, tsk, t_arrival):
        """
        Submit the arrival of a task.
        :param tsk: (TaskType) the type of the task.
        :param t_arrival: (float) the arrival time.
        :return: (float) the completion time.
        """
        # Check correctness
        assert self.state[TaskScope.TASK_1] + self.state[TaskScope.TASK_2] < self.n_servers

        # Update state
        server_idx = self.server_selector.select_idle()
        if server_idx is None:
            raise RuntimeError("Cannot find server for arrival of task {} at time {}".format(tsk, t_arrival))
        t_completion = self.servers[server_idx].submit_arrival(tsk, t_arrival)
        self.state[tsk] += 1

        # Update statistics
        self.statistics.metrics.arrived[SystemScope.CLOUDLET][tsk].increment(1)
        self.sample_mean_population()

        return t_completion

    def submit_interruption(self, tsk, t_interruption):
        """
        Submit the interruption of a task.
        :param tsk: (TaskType) the type of the task.
        :param t_interruption: (float) the interruption time.
        :return: (c,w,s,r) where
        *c* is the completion time to ignore;
        *a* is the arrival time;
        *r* is the remaining service time ratio;
        """
        # Check correctness
        assert self.state[tsk] > 0

        # Update state
        server_idx = self.server_selector.select_interruption(tsk)
        if server_idx is None:
            raise RuntimeError("Cannot find server for interruption of task {} at time {}".format(tsk, t_interruption))
        t_completion_to_ignore, t_arrival, t_served, r_remaining = self.servers[server_idx].submit_interruption(tsk, t_interruption)
        self.state[tsk] -= 1

        # Update statistics
        self.statistics.metrics.switched[SystemScope.CLOUDLET][tsk].increment(1)
        self.statistics.metrics.switched_service[SystemScope.CLOUDLET][tsk].increment(t_served)
        self.statistics.metrics.service[SystemScope.CLOUDLET][tsk].increment(t_served)
        self.sample_mean_population()

        return t_completion_to_ignore, t_arrival, r_remaining

    def submit_completion(self, tsk, t_completion, t_arrival):
        """
        Submit the completion of a task.
        :param tsk: (TaskType) the type of the task.
        :param t_completion: (float) the completion time.
        :param t_arrival: (float) the arrival time.
        :return: None
        """
        # Check correctness
        assert self.state[tsk] > 0

        # Update state
        server_idx = self.find_completion_server_idx(tsk, t_completion)
        if server_idx is None:
            raise RuntimeError("Cannot find server for completion of task {} at time {}".format(tsk, t_completion))
        self.servers[server_idx].submit_completion()
        self.state[tsk] -= 1

        t_served = t_completion - t_arrival

        # Update statistics
        self.statistics.metrics.completed[SystemScope.CLOUDLET][tsk].increment(1)
        self.statistics.metrics.service[SystemScope.CLOUDLET][tsk].increment(t_served)
        self.sample_mean_population()

    # ==================================================================================================================
    # OTHER
    # ==================================================================================================================

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

    def sample_mean_population(self):
        """
        Register the sample for the mean population.
        :return: None.
        """
        for tsk in TaskScope.concrete():
            self.statistics.metrics.population[SystemScope.CLOUDLET][tsk].add_sample(self.state[tsk])
        self.statistics.metrics.population[SystemScope.CLOUDLET][TaskScope.GLOBAL].add_sample(
            sum(self.state[tsk] for tsk in TaskScope.concrete()))

    def __str__(self):
        """
        String representation.
        :return: the string representation.
        """
        sb = ["{attr}={value}".format(attr=attr, value=self.__dict__[attr]) for attr in self.__dict__ if
              not attr.startswith("__") and not callable(getattr(self, attr))]
        return "Cloudlet({}:{})".format(id(self), ", ".join(sb))