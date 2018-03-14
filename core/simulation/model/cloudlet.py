from core.simulation.model.server import SimpleServer as Server
from core.simulation.model.event import EventType
from core.simulation.model.scope import SystemScope
from core.simulation.model.scope import TaskScope
from core.simulation.model.scope import ActionScope
from core.simulation.model.server_selection_rule import SelectionRule
from core.simulation.model.scope import TaskScope
import logging

# Configure logger
logger = logging.getLogger(__name__)


class SimpleCloudlet:
    """
    A simple Cloudlet, defined by its state.
    """

    def __init__(self, rndgen, config, state, statistics):
        """
        Create a new Cloudlet.
        :param rndgen: (object) the multi-stream random number generator.
        :param config: (dict) the configuration.
        :param state: the system state.
        :param statistics: the system statistics.
        """
        # Service rates
        self.rates = {tsk: config["service_rate_{}".format(tsk.value)] for tsk in TaskScope.concrete()}

        # Randomization
        self.rndgen = rndgen
        self.streams = {tsk: EventType.of(ActionScope.COMPLETION, SystemScope.CLOUDLET, tsk).value for tsk in TaskScope.concrete()}

        # Servers
        self.n_servers = config["n_servers"]
        self.threshold = config["threshold"]
        self.servers = [Server(rndgen, self.rates, i) for i in range(self.n_servers)]
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
    #   * ARRIVAL_TASK_1
    #   * ARRIVAL_TASK_2
    #   * COMPLETION_CLOUDLET_TASK_1
    #   * COMPLETION_CLOUDLET_TASK_2
    # ==================================================================================================================

    def submit_arrival(self, task_type, t_arrival):
        """
        Submit the arrival of a task.
        :param task_type: (TaskType) the type of the task.
        :param t_arrival: (float) the arrival time.
        :return: (float) the completion time.
        """
        # Check correctness
        assert self.state[TaskScope.TASK_1] + self.state[TaskScope.TASK_2] < self.n_servers

        # Update state
        server_idx = self.server_selector.select_idle()
        if server_idx is None:
            raise RuntimeError("Cannot find server for arrival of task {} at time {}".format(task_type, t_arrival))
        t_completion = self.servers[server_idx].submit_arrival(task_type, t_arrival)
        self.state[task_type] += 1

        # Update statistics
        self.statistics.metrics.arrived[SystemScope.CLOUDLET][task_type].increment(1)
        #self.statistics.metrics.population[SystemScope.CLOUDLET][task_type].add_sample(self.state[task_type])

        return t_completion

    def submit_interruption(self, task_type, t_interruption):
        """
        Submit the interruption of a task.
        :param task_type: (TaskType) the type of the task.
        :param t_interruption: (float) the interruption time.
        :return: (c,w,s,r) where
        *c* is the completion time to ignore;
        *a* is the arrival time;
        *r* is the remaining service time ratio;
        """
        # Check correctness
        assert self.state[task_type] > 0

        # Update state
        server_idx = self.server_selector.select_interruption(task_type)
        if server_idx is None:
            raise RuntimeError("Cannot find server for interruption of task {} at time {}".format(task_type, t_interruption))
        t_completion_to_ignore, t_arrival, t_served, r_remaining = self.servers[server_idx].submit_interruption(task_type, t_interruption)
        self.state[task_type] -= 1

        # Update statistics
        self.statistics.metrics.switched[SystemScope.CLOUDLET][task_type].increment(1)
        self.statistics.metrics.switched_service[SystemScope.CLOUDLET][task_type].increment(1)
        self.statistics.metrics.service[SystemScope.CLOUDLET][task_type].increment(t_served)
        #self.statistics.metrics.population[SystemScope.CLOUDLET][task_type].add_sample(self.state[task_type])

        return t_completion_to_ignore, t_arrival, r_remaining

    def submit_completion(self, task_type, t_completion, t_arrival):
        """
        Submit the completion of a task.
        :param task_type: (TaskType) the type of the task.
        :param t_completion: (float) the completion time.
        :param t_arrival: (float) the arrival time.
        :return: None
        """
        # Check correctness
        assert self.state[task_type] > 0

        # Update state
        server_idx = self.find_completion_server_idx(task_type, t_completion)
        if server_idx is None:
            raise RuntimeError("Cannot find server for completion of task {} at time {}".format(task_type, t_completion))
        self.servers[server_idx].submit_completion()
        self.state[task_type] -= 1

        # Update statistics
        self.statistics.metrics.completed[SystemScope.CLOUDLET][task_type].increment(1)
        self.statistics.metrics.service[SystemScope.CLOUDLET][task_type].increment(t_completion - t_arrival)
        #self.statistics.metrics.population[SystemScope.CLOUDLET][task_type].add_sample(self.state[task_type])

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

    def __str__(self):
        """
        String representation.
        :return: the string representation.
        """
        sb = ["{attr}={value}".format(attr=attr, value=self.__dict__[attr]) for attr in self.__dict__ if
              not attr.startswith("__") and not callable(getattr(self, attr))]
        return "Cloudlet({}:{})".format(id(self), ", ".join(sb))