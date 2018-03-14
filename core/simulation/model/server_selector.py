from random import choice
from core.simulation.model.server import ServerState
from core.simulation.model.scope import TaskScope


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
        candidates = [(idx, server) for idx, server in enumerate(self._servers) if server.state is ServerState.IDLE]
        if len(candidates) == 0:
            return None
        return candidates[0][0]

    def select_interruption(self, task_type):
        """
        Select an interruption server, according to the adopted server selection rule.
        :param task_type: (TaskType) the type of the task.
        :return: (int) the index of the selected server, if present; None, otherwise.
        """
        candidates = [(idx, server) for idx, server in enumerate(self._servers) if server.task_type is task_type]
        if len(candidates) == 0:
            return None
        return candidates[0][0]


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
        candidates = [(idx, server) for idx, server in enumerate(self._servers[self._last:]) if server.state is ServerState.IDLE]
        if len(candidates) == 0:
            return None
        self._last = selected_server = choice(candidates)[0]
        return selected_server

    def select_interruption(self, task_type):
        """
        Select an interruption server, according to the adopted server selection rule.
        :param task_type: (TaskType) the type of the task.
        :return: (int) the index of the selected server, if present; None, otherwise.
        """
        candidates = [(idx, server) for idx, server in enumerate(self._servers[self._last:]) if server.task_type is task_type]
        if len(candidates) == 0:
            return None
        self._last = selected_server = choice(candidates)[0]
        return selected_server


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
        return max(candidates, key=lambda elem: elem.idle_time)[0]

    def select_interruption(self, task_type):
        """
        Select an interruption server, according to the adopted server selection rule.
        :param task_type: (TaskType) the type of the task.
        :return: (int) the index of the selected server, if present; None, otherwise.
        """
        candidates = [(idx, server) for idx, server in enumerate(self._servers) if server.task_type is task_type]
        if len(candidates) == 0:
            return None
        return min(candidates, key=lambda elem: elem.switched[task_type])[0]


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
        return choice(candidates)[0]

    def select_interruption(self, task_type):
        """
        Select an interruption server, according to the adopted server selection rule.
        :param task_type: (TaskType) the type of the task.
        :return: (int) the index of the selected server, if present; None, otherwise.
        """
        candidates = [(idx, server) for idx, server in enumerate(self._servers) if server.task_type is task_type]
        if len(candidates) == 0:
            return None
        return choice(candidates)[0]