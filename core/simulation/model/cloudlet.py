from core.simulation.model.server import SimpleServer as Server
from core.simulation.model.event import EventType
from core.simulation.model.server_selection_rule import SelectionRule
from core.simulation.model.scope import TaskScope
import logging

# Configure logger
logger = logging.getLogger(__name__)


class SimpleCloudlet:
    """
    A simple Cloudlet, defined by its state.
    """

    def __init__(self, rndgen, n_servers, service_rate_1, service_rate_2, threshold, server_selection_rule=SelectionRule.ORDER):
        """
        Create a new Cloudlet.
        :param rndgen: (object) the multi-stream random number generator.
        :param n_servers: (integer) the number of servers.
        :param service_rate_1: (float) the service rate for job of type 1 (tasks/s).
        :param service_rate_2: (float) the service rate for job of type 2 (tasks/s).
        :param threshold: (int) the occupancy threshold.
        :param server_selection_rule: (SelectionRule) the adopted server selection rule.
        """
        # Service rates
        self.rates = {
            TaskScope.TASK_1: service_rate_1,
            TaskScope.TASK_2: service_rate_2
        }

        # Randomization
        self.rndgen = rndgen
        self.streams = {
            TaskScope.TASK_1: EventType.COMPLETION_CLOUDLET_TASK_1.value,
            TaskScope.TASK_2: EventType.COMPLETION_CLOUDLET_TASK_2.value
        }

        # Servers
        self.n_servers = n_servers
        self.threshold = threshold
        self.servers = [Server(rndgen, service_rate_1, service_rate_2) for _ in range(n_servers)]
        self.server_selector = server_selection_rule.selector(self.servers)

        if not (0 <= self.threshold <= self.n_servers):
            raise ValueError(
                "Invalid threhsold: should be >= 0 and <= n_servers, but threshold is {} and n_servers is {}".format(
                    self.threshold, self.n_servers))

        # State
        self.n = {task: 0 for task in TaskScope}  # current number of tasks, by task type

        # Whole-run Statistics (used in verification)
        self.arrived = {task: 0 for task in TaskScope}  # total number of arrived tasks, by task type
        self.completed = {task: 0 for task in TaskScope}  # total number of completed tasks, by task type
        self.switched = {task: 0 for task in TaskScope}  # total number of interrupted tasks, by task type
        self.service = {task: 0 for task in TaskScope}  # total service time, by task type

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
        assert self.n[TaskScope.TASK_1] + self.n[TaskScope.TASK_2] < self.n_servers

        # Update state
        server_idx = self.server_selector.select_idle()
        if server_idx is None:
            raise RuntimeError("Cannot find server for arrival of task {} at time {}".format(task_type, t_arrival))
        t_completion = self.servers[server_idx].submit_arrival(task_type, t_arrival)
        self.n[task_type] += 1

        # Update statistics
        self.arrived[task_type] += 1

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
        assert self.n[task_type] > 0

        # Update state
        server_idx = self.server_selector.select_interruption(task_type)
        if server_idx is None:
            raise RuntimeError("Cannot find server for interruption of task {} at time {}".format(task_type, t_interruption))
        t_completion_to_ignore, t_arrival, t_served, r_remaining = self.servers[server_idx].submit_interruption(task_type, t_interruption)
        self.n[task_type] -= 1

        # Update statistics
        self.switched[task_type] += 1
        self.service[task_type] += t_served

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
        assert self.n[task_type] > 0

        # Update state
        server_idx = self.find_completion_server_idx(task_type, t_completion)
        if server_idx is None:
            raise RuntimeError("Cannot find server for completion of task {} at time {}".format(task_type, t_completion))
        self.servers[server_idx].submit_completion()
        self.n[task_type] -= 1

        # Update statistics
        self.completed[task_type] += 1
        self.service[task_type] += t_completion - t_arrival

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