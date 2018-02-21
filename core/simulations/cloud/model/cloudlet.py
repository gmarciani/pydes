from core.simulations.cloud.model.server import SimpleServer as Server
from core.simulations.cloud.model.server_selector import SelectionRule,ServerSelectorOrder,ServerSelectorCyclic, ServerSelectorEquity, ServerSelectorRandom
from core.simulations.cloud.model.server import ServerState
from core.simulations.cloud.model.event import SimpleEvent as Event
from core.simulations.cloud.model.event import EventType
from core.simulations.cloud.model.task import TaskType
from core.random.rndvar import exponential
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
        self._rndgen = rndgen
        self.n_servers = n_servers
        self.service_rate_1 = service_rate_1
        self.service_rate_2 = service_rate_2
        self.threshold = threshold
        self.server_selection_rule = server_selection_rule

        # servers initialization
        self._servers = [Server(rndgen, service_rate_1, service_rate_2) for i in range(n_servers)]
        if self.server_selection_rule is SelectionRule.ORDER:
            self._server_selector = ServerSelectorOrder(self._servers)
        elif self.server_selection_rule is SelectionRule.CYCLIC:
            self._server_selector = ServerSelectorCyclic(self._servers)
        elif self.server_selection_rule is SelectionRule.EQUITY:
            self._server_selector = ServerSelectorEquity(self._servers)
        elif self.server_selection_rule is SelectionRule.RANDOM:
            self._server_selector = ServerSelectorRandom(self._servers)
        else:
            raise ValueError("Unrecognized server-selection rule: {}".format(self.server_selection_rule))

        if not (1 <= self.threshold <= self.n_servers):
            raise ValueError(
                "Invalid threhsold: should be >= 1 and <= n_servers, but threshold is {} and n_servers is {}".format(
                    self.threshold, self.n_servers))

        # state
        self.n_1 = 0  # number of tasks of type 1 serving in the Cloudlet
        self.n_2 = 0  # number of tasks of type 2 serving in the Cloudlet

        # statistics
        self.n_arrival_1 = 0  # number of tasks of type 1 arrived to the Cloudlet
        self.n_arrival_2 = 0  # number of tasks of type 2 arrived to the Cloudlet
        self.n_served_1 = 0  # number of tasks of type 1 served in the Cloudlet
        self.n_served_2 = 0  # number of tasks of type 2 served in the Cloudlet
        self.n_interrupted_2 = 0  # number of tasks of type 2 interrupted from the Cloudlet

        self.t_service_1 = 0.0  # the total service time for tasks of tye 1
        self.t_service_2 = 0.0  # the total service time for tasks of tye 2
        self.t_wasted_2 = 0.0  # the total service time wasted for interrupted tasks of type 2

    # ==================================================================================================================
    # EVENT SUBMISSION
    #   * ARRIVAL_TASK_1
    #   * ARRIVAL_TASK_2
    #   * COMPLETION_CLOUDLET_TASK_1
    #   * COMPLETION_CLOUDLET_TASK_2
    # ==================================================================================================================

    def submit_arrival_task_1(self, t_arrival):
        """
        Submit to the Cloudlet the arrival of a task of type 1.
        :param t_arrival: (float) the arrival time.
        :return: (SimpleEvent) the completion event of the submitted task of type 1.
        """
        # Check correctness
        assert self.n_1 + self.n_2 < self.n_servers

        # Update state
        server_idx = self._server_selector.select_idle()
        if server_idx is None:
            raise RuntimeError("Cannot find idle server for arrival of task of type 1")
        t_completion, t_service = self._servers[server_idx].submit_task_1(t_arrival)
        self.n_1 += 1

        # Update statistics
        self.n_arrival_1 += 1

        # Generate completion
        completion_event = Event(EventType.COMPLETION_CLOUDLET_TASK_1, t_completion, t_service=t_service)

        return completion_event

    def submit_arrival_task_2(self, t_arrival):
        """
        Submit to the Cloudlet the arrival of a task of type 2.
        :param t_arrival: (float) the occurrence time of the event.
        :return: (SimpleEvent) the completion event of the submitted task of type 2.
        """
        # Check correctness
        assert self.n_1 + self.n_2 < self.n_servers

        # Update state
        server_idx = self._server_selector.select_idle()
        if server_idx is None:
            raise RuntimeError("Cannot find free server for arrival of task of type 2")
        t_completion, t_service = self._servers[server_idx].submit_task_2(t_arrival)
        self.n_2 += 1

        # Update statistics
        self.n_arrival_2 += 1

        # Generate completion
        completion_event = Event(EventType.COMPLETION_CLOUDLET_TASK_2, t_completion, t_service=t_service)

        return completion_event

    def submit_interruption_task_2(self, t_removal):
        """
        Submit to the Cloudlet the interruption of a task of type 2.
        :param t_removal: (float) the time of removal.
        :return: (e,w) where *e* is the completion event to ignore of the submitted task of type 2;
        *w* is the wasted time.
        """
        # Check correctness
        assert self.n_2 > 0

        # Update state
        server_idx = self._server_selector.select_interruption()
        if server_idx is None:
            raise RuntimeError("Cannot find interruption server at time {}".format((t_removal)))
        t_completion_to_ignore, t_arrival, t_wasted = self._servers[server_idx].interrupt_task_2(t_removal)
        self.n_2 -= 1

        # Update statistics
        self.n_interrupted_2 += 1
        self.t_wasted_2 += t_wasted

        # Generate completion event to ignore
        completion_event_to_ignore = Event(EventType.COMPLETION_CLOUDLET_TASK_2, t_completion_to_ignore)

        return completion_event_to_ignore, t_wasted

    def submit_completion_task_1(self, t_completion):
        """
        Submit to the Cloudlet the completion of a task of type 1.
        :param t_completion: (float) the completion time.
        :return: None
        """
        # Check correctness
        assert self.n_1 > 0

        # Update state
        server_idx = self.find_completion_server_idx(TaskType.TASK_1, t_completion)
        if server_idx is None:
            raise RuntimeError("Cannot find server for task of type 1 and t_completion={}".format(t_completion))
        t_service = self._servers[server_idx].submit_completion()
        self.n_1 -= 1

        # Update statistics
        self.n_served_1 += 1
        self.t_service_1 += t_service

    def submit_completion_task_2(self, t_completion):
        """
        Submit to the Cloudlet the completion of a task of type 2.
        :param t_completion: (float) the completion time.
        :return: None
        """
        # Check correctness
        assert self.n_2 > 0

        # Update state
        server_idx = self.find_completion_server_idx(TaskType.TASK_2, t_completion)
        if server_idx is None:
            raise RuntimeError("Cannot find completion server for task of type 2 and t_completion={}\n{}".format(t_completion, str(self._servers)))
        t_service = self._servers[server_idx].submit_completion()
        self.n_2 -= 1

        # Update statistics
        self.n_served_2 += 1
        self.t_service_2 += t_service

    # ==================================================================================================================
    # RANDOM TIME GENERATION
    #   * service time task 1
    #   * service time task 2
    # ==================================================================================================================

    def get_service_time_task_1(self):
        """
        Generate the service time for a task of type 1, exponentially distributed with rate *service_rate_1*.
        :return: (float) the completion time for a task of type 1 (s).
        """
        self._rndgen.stream(EventType.COMPLETION_CLOUDLET_TASK_1.value)
        return exponential(1.0 / self.service_rate_1, self._rndgen.rnd())

    def get_service_time_task_2(self):
        """
        Generate the service time for a task of type 2, exponentially distributed with rate *service_rate_2*.
        :return: (float) the completion time for a task of type 2 (s).
        """
        self._rndgen.stream(EventType.COMPLETION_CLOUDLET_TASK_2.value)
        return exponential(1.0 / self.service_rate_2, self._rndgen.rnd())

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
        for idx, server in enumerate(self._servers):
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