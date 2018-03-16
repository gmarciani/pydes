import random
from core.simulation.model.server import ServerState
from core.utils.logutils import get_logger


# Logging
logger = get_logger(__name__)


class BaseServerSelection:

    def __init__(self, servers):
        """
        Create a new server selector.
        :param servers: ([SimpleServer]) the list of servers.
        """
        self._servers = servers

    def select_idle(self):
        """
        Select an idle idle server, according to the adopted server selection rule.
        :return: (int) the index of the selected server, if present; None, otherwise.
        """
        raise NotImplementedError

    def select_interruption(self, task_type):
        """
        Select an interruption server, according to the adopted server selection rule.
        :param task_type: (TaskType) the type of the task.
        :return: (int) the index of the selected server, if present; None, otherwise.
        """
        raise NotImplementedError


class ServerSelectorOrder(BaseServerSelection):

    def __init__(self, servers):
        """
        Create a new server selector based on Order Selection Rule
        :param servers: ([SimpleServer]) the list of servers.
        """
        BaseServerSelection.__init__(self, servers)

    def select_idle(self):
        """
        Select an idle server, according to the adopted server selection rule.
        :return: (int) the index of the selected server, if present; None, otherwise.
        """
        for (idx, srv) in enumerate(self._servers):
            if srv.state is ServerState.IDLE:
                return idx
        return None

    def select_interruption(self, task_type):
        """
        Select an interruption server, according to the adopted server selection rule.
        :param task_type: (TaskType) the type of the task.
        :return: (int) the index of the selected server, if present; None, otherwise.
        """
        for (idx, srv) in enumerate(self._servers):
            if srv.task_type is task_type:
                return idx
        return None


class ServerSelectorCyclic(BaseServerSelection):

    def __init__(self, servers):
        """
        Create a new server selector based on Cyclic Selection Rule.
        :param servers: ([SimpleServer]) the list of servers.
        """
        BaseServerSelection.__init__(self, servers)
        self._last = 0  # the last selected index

    def select_idle(self):
        """
        Select an idle server, according to the adopted server selection rule.
        :return: (int) the index of the selected server, if present; None, otherwise.
        """
        for i in range(1, len(self._servers)+1):
            idx = (self._last + i) % len(self._servers)
            srv = self._servers[idx]
            if srv.state is ServerState.IDLE:
                self._last = idx
                return idx
        return None

    def select_interruption(self, task_type):
        """
        Select an interruption server, according to the adopted server selection rule.
        :param task_type: (TaskType) the type of the task.
        :return: (int) the index of the selected server, if present; None, otherwise.
        """
        for i in range(1, len(self._servers)+1):
            idx = (self._last + i) % len(self._servers)
            srv = self._servers[idx]
            if srv.task_type is task_type:
                self._last = idx
                return idx
        return None


class ServerSelectorEquity(BaseServerSelection):

    def __init__(self, servers):
        """
        Create a new server selector based on Equity Selection Rule.
        :param servers: ([SimpleServer]) the list of servers.
        """
        BaseServerSelection.__init__(self, servers)

    def select_idle(self):
        """
        Select an idle server, according to the adopted server selection rule.
        :return: (int) the index of the selected server, if present; None, otherwise.
        """
        candidates = [(idx, server) for idx, server in enumerate(self._servers) if server.state is ServerState.IDLE]
        if len(candidates) == 0:
            return None
        return max(candidates, key=lambda x: x[1].t_idle)[0]

    def select_interruption(self, tsk):
        """
        Select an interruption server, according to the adopted server selection rule.
        :param tsk: (TaskType) the type of the task.
        :return: (int) the index of the selected server, if present; None, otherwise.
        """
        candidates = [(idx, server) for idx, server in enumerate(self._servers) if server.task_type is tsk]
        if len(candidates) == 0:
            return None
        return min(candidates, key=lambda x: x[1].switched[tsk])[0]


class ServerSelectorRandom(BaseServerSelection):

    def __init__(self, servers):
        """
        Create a new server selector based on Random Selection Rule.
        :param servers: ([SimpleServer]) the list of servers.
        """
        BaseServerSelection.__init__(self, servers)

    def select_idle(self):
        """
        Select an idle server, according to the adopted server selection rule.
        :return: (int) the index of the selected server, if present; None, otherwise.
        """
        candidates = [(idx, server) for idx, server in enumerate(self._servers) if server.state is ServerState.IDLE]
        if len(candidates) == 0:
            return None
        return random.choice(candidates)[0]

    def select_interruption(self, tsk):
        """
        Select an interruption server, according to the adopted server selection rule.
        :param tsk: (TaskType) the type of the task.
        :return: (int) the index of the selected server, if present; None, otherwise.
        """
        candidates = [(idx, server) for idx, server in enumerate(self._servers) if server.task_type is tsk]
        if len(candidates) == 0:
            return None
        return random.choice(candidates)[0]