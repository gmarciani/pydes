from core.simulations.cloud.model.server import SimpleServer as Server
from core.simulations.cloud.model.server import ServerState
from core.simulations.cloud.model.event import SimpleEvent as Event
from core.simulations.cloud.model.event import EventType
from core.simulations.cloud.model.task import TaskType
from core.random.rndvar import exponential
import logging

# Configure logger
logger = logging.getLogger(__name__)


class SimpleCloudLet:
    """
    A simple Cloudlet, defined by its state.
    """

    def __init__(self, rndgen, n_servers, service_rate_1, service_rate_2, threshold):
        """
        Create a new Cloudlet.
        :param rndgen: (object) the multi-stream random number generator.
        :param n_servers: (integer) the number of servers.
        :param service_rate_1: (float) the service rate for job of type 1 (tasks/s).
        :param service_rate_2: (float) the service rate for job of type 2 (tasks/s).
        :param threshold: (int) the occupancy threshold.
        """
        self._rndgen = rndgen
        self.n_servers = n_servers
        self.service_rate_1 = service_rate_1
        self.service_rate_2 = service_rate_2
        self.threshold = threshold

        # state
        self.n_1 = 0  # number of tasks of type 1 serving in the Cloudlet
        self.n_2 = 0  # number of tasks of type 2 serving in the Cloudlet
        self._servers = [Server(rndgen, service_rate_1, service_rate_2) for i in range(n_servers)]

        # statistics
        self.n_arrival_1 = 0  # number of tasks of type 1 arrived to the Cloudlet
        self.n_arrival_2 = 0  # number of tasks of type 2 arrived to the Cloudlet
        self.n_served_1 = 0  # number of tasks of type 1 served in the Cloudlet
        self.n_served_2 = 0  # number of tasks of type 2 served in the Cloudlet
        self.n_removed_2 = 0  # number of tasks of type 2 removed from the Cloudlet

        self.t_service_1 = 0.0  # the total service time for tasks of type 1
        self.t_service_2 = 0.0  # the total service time for tasks of type 2
        self.t_wasted_2 = 0.0  # the total service time for tasks of type 2, wasted due to removal

    def submit_arrival_task_1(self, event_time):
        """
        Submit to the Cloudlet the arrival of a task of type 1.
        :param event_time: (float) the occurrence time of the event.
        :return: (SimpleEvent) the completion event of the submitted task of type 1.
        """
        assert self.n_1 + self.n_2 < self.n_servers

        # state change
        server_idx = self.select_idle_server_idx()
        if server_idx is None:
            raise RuntimeError("Cannot find idle server for arrival of task of type 1 \n {}".format(self))
        t_completion = self._servers[server_idx].submit_task_1(event_time)
        self.n_1 += 1

        # completion event
        completion_event = Event(EventType.COMPLETION_CLOUDLET_TASK_1, t_completion)

        # record statistics
        self.n_arrival_1 += 1
        self.t_service_1 += (t_completion - event_time)

        return completion_event

    def submit_arrival_task_2(self, event_time):
        """
        Submit to the Cloudlet the arrival of a task of type 2.
        :param event_time: (float) the occurrence time of the event.
        :return: (SimpleEvent) the completion event of the submitted task of type 2.
        """
        assert self.n_1 + self.n_2 < self.n_servers

        # state change
        server_idx = self.select_idle_server_idx()
        if server_idx is None:
            raise RuntimeError("Cannot find free server for arrival of task of type 2 \n {}".format(self))
        t_completion = self._servers[server_idx].submit_task_2(event_time)
        self.n_2 += 1

        # completion event
        completion_event = Event(EventType.COMPLETION_CLOUDLET_TASK_2, t_completion)

        # record statistics
        self.n_arrival_2 += 1
        self.t_service_2 += (t_completion - event_time)

        return completion_event

    def submit_removal_task_2(self, event_time):
        """
        Submit to the Cloudlet the removal of a task of type 2.
        :param event_time: (float) the occurrence time of the event.
        :return: (SimpleEvent) the completion event to ignore of the submitted task of type 2.
        """
        assert self.n_2 > 0

        # state change
        server_idx = self.select_interruption_server_idx()
        if server_idx is None:
            raise RuntimeError("Cannot find interruption server at time ", event_time)
        t_arrival, t_completion_to_ignore = self._servers[server_idx].interrupt_task_2(event_time)
        self.n_2 -= 1

        # completion event to ignore
        completion_event_to_ignore = Event(EventType.COMPLETION_CLOUDLET_TASK_2, t_completion_to_ignore)

        # record statistics
        self.n_removed_2 += 1
        self.t_wasted_2 += (event_time - t_arrival)

        return completion_event_to_ignore

    def submit_completion_task_1(self, event_time):
        """
        Submit to the Cloudlet the completion of a task of type 1.
        :param event_time: (float) the occurrence time of the event.
        :return: (void)
        """
        assert self.n_1 > 0

        # state change
        server_idx = self.find_completion_server_idx(TaskType.TASK_1, event_time)
        if server_idx is None:
            raise RuntimeError("Cannot find completion server for task of type 1 and completion time ", event_time)
        self._servers[server_idx].submit_completion()
        self.n_1 -= 1

        # record statistics
        self.n_served_1 += 1

    def submit_completion_task_2(self, event_time):
        """
        Submit to the Cloudlet the completion of a task of type 2.
        :param event_time: (float) the occurrence time of the event.
        :return: (void)
        """
        assert self.n_2 > 0

        # state change
        server_idx = self.find_completion_server_idx(TaskType.TASK_2, event_time)
        if server_idx is None:
            raise RuntimeError("Cannot find completion server for task of type 2 and completion time ", event_time)
        self._servers[server_idx].submit_completion()
        self.n_2 -= 1

        # record statistics
        self.n_served_2 += 1

    def select_idle_server_idx(self):
        """
        Select an idle server, according to the adopted selection rule.
        :return: (int) the index of the selected idle server, if present; None, otherwise.
        """
        for idx, server in enumerate(self._servers):
            if server.state is ServerState.IDLE:
                return idx
        return None

    def select_interruption_server_idx(self):
        """
        Select an interruption server, according to the adopted selection rule.
        :return: (int) the index of the selected interruption server, if present; None, otherwise.
        """
        for idx, server in enumerate(self._servers):
            if server.task_type is TaskType.TASK_2:
                return idx
        return None

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

    def get_completion_task_1(self):
        """
        Generate a completion time for a task of type 1, exponentially distributed with rate *service_rate_1*.
        :return: (float) the completion time for a task of type 1 (s).
        """
        self._rndgen.stream(EventType.COMPLETION_CLOUDLET_TASK_1.value)
        u = self._rndgen.rnd()
        m = 1.0 / self.service_rate_1
        return exponential(m, u)

    def get_completion_task_2(self):
        """
        Generate a completion time for a task of type 2, exponentially distributed with rate *service_rate_2*.
        :return: (float) the completion time for a task of type 2 (s).
        """
        self._rndgen.stream(EventType.COMPLETION_CLOUDLET_TASK_2.value)
        u = self._rndgen.rnd()
        m = 1.0 / self.service_rate_2
        return exponential(m, u)

    def __str__(self):
        """
        String representation.
        :return: the string representation.
        """
        sb = ["{attr}='{value}'".format(attr=attr, value=self.__dict__[attr]) for attr in self.__dict__ if not attr.startswith("__") and not callable(getattr(self, attr))]
        return "Cloudlet({}:{})".format(id(self), ", ".join(sb))

    def __repr__(self):
        """
        String representation.
        :return: the string representation.
        """
        return self.__str__()

    def __eq__(self, other):
        if not isinstance(other, SimpleCloudLet):
            return False
        return id(self) == id(other)


if __name__ == "__main__":
    from core.random.rndgen import MarcianiMultiStream as RandomGenerator

    rndgen = RandomGenerator(123456789)

    # Creation
    cloudlet_1 = SimpleCloudLet(rndgen, 10, 0.45, 0.30, 10)
    print("Cloudlet 1:", cloudlet_1)
    cloudlet_2 = SimpleCloudLet(rndgen, 20, 0.90, 0.60, 20)
    print("Cloudlet 2:", cloudlet_2)

    # Equality check
    print("Cloudlet 1 equals Cloudlet 2:", cloudlet_1 == cloudlet_2)

    # Service time of tasks of type 1
    for i in range(10):
        t_service_1 = cloudlet_1.get_completion_task_1()
        print("service time task 1: ", t_service_1)

    # Service time of tasks of type 2
    for i in range(10):
        t_service_2 = cloudlet_1.get_completion_task_2()
        print("sevice time task 2: ", t_service_2)