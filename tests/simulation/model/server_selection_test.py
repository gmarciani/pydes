import unittest
from types import SimpleNamespace

from pydes.core.simulation.model.scope import TaskScope
from pydes.core.simulation.model.server import ServerState, SimpleServer
from pydes.core.simulation.model.server_selection import (
    BaseServerSelection,
    ServerSelectorCyclic,
    ServerSelectorEquity,
    ServerSelectorOrder,
    ServerSelectorRandom,
)


def make_servers(n):
    """
    Build n bare SimpleServer instances (idle, no task) without requiring a real random component.
    """
    fake_rndservice = SimpleNamespace(str={})
    return [SimpleServer(fake_rndservice, i) for i in range(n)]


class BaseServerSelectionTest(unittest.TestCase):
    def test_select_idle_not_implemented(self):
        selector = BaseServerSelection(make_servers(1))
        with self.assertRaises(NotImplementedError):
            selector.select_idle()

    def test_select_interruption_not_implemented(self):
        selector = BaseServerSelection(make_servers(1))
        with self.assertRaises(NotImplementedError):
            selector.select_interruption(TaskScope.TASK_1)


class ServerSelectorOrderTest(unittest.TestCase):
    def test_select_idle_returns_none_when_all_busy(self):
        servers = make_servers(2)
        for s in servers:
            s.state = ServerState.BUSY
        selector = ServerSelectorOrder(servers)
        self.assertIsNone(selector.select_idle())

    def test_select_idle_returns_first_idle(self):
        servers = make_servers(3)
        servers[0].state = ServerState.BUSY
        selector = ServerSelectorOrder(servers)
        self.assertEqual(selector.select_idle(), 1)

    def test_select_interruption_returns_none_when_no_match(self):
        servers = make_servers(2)
        selector = ServerSelectorOrder(servers)
        self.assertIsNone(selector.select_interruption(TaskScope.TASK_1))

    def test_select_interruption_returns_matching_server(self):
        servers = make_servers(2)
        servers[1].task_type = TaskScope.TASK_1
        selector = ServerSelectorOrder(servers)
        self.assertEqual(selector.select_interruption(TaskScope.TASK_1), 1)


class ServerSelectorCyclicTest(unittest.TestCase):
    def test_select_idle_returns_none_when_all_busy(self):
        servers = make_servers(2)
        for s in servers:
            s.state = ServerState.BUSY
        selector = ServerSelectorCyclic(servers)
        self.assertIsNone(selector.select_idle())

    def test_select_interruption_returns_none_when_no_match(self):
        servers = make_servers(2)
        selector = ServerSelectorCyclic(servers)
        self.assertIsNone(selector.select_interruption(TaskScope.TASK_1))

    def test_select_idle_cycles_through_servers(self):
        servers = make_servers(3)
        selector = ServerSelectorCyclic(servers)
        first = selector.select_idle()
        second = selector.select_idle()
        self.assertNotEqual(first, second)

    def test_select_interruption_updates_last(self):
        servers = make_servers(3)
        servers[0].task_type = TaskScope.TASK_1
        servers[2].task_type = TaskScope.TASK_1
        selector = ServerSelectorCyclic(servers)
        first = selector.select_interruption(TaskScope.TASK_1)
        self.assertIn(first, (0, 2))


class ServerSelectorEquityTest(unittest.TestCase):
    def test_select_idle_returns_none_when_all_busy(self):
        servers = make_servers(2)
        for s in servers:
            s.state = ServerState.BUSY
        selector = ServerSelectorEquity(servers)
        self.assertIsNone(selector.select_idle())

    def test_select_interruption_returns_none_when_no_match(self):
        servers = make_servers(2)
        selector = ServerSelectorEquity(servers)
        self.assertIsNone(selector.select_interruption(TaskScope.TASK_1))

    def test_select_idle_returns_the_most_idle_server(self):
        servers = make_servers(2)
        servers[0].t_idle = 1.0
        servers[1].t_idle = 5.0
        selector = ServerSelectorEquity(servers)
        self.assertEqual(selector.select_idle(), 1)

    def test_select_interruption_returns_the_least_switched_server(self):
        servers = make_servers(2)
        servers[0].task_type = TaskScope.TASK_1
        servers[1].task_type = TaskScope.TASK_1
        servers[0].switched[TaskScope.TASK_1] = 3
        servers[1].switched[TaskScope.TASK_1] = 1
        selector = ServerSelectorEquity(servers)
        self.assertEqual(selector.select_interruption(TaskScope.TASK_1), 1)


class ServerSelectorRandomTest(unittest.TestCase):
    def test_select_idle_returns_none_when_all_busy(self):
        servers = make_servers(2)
        for s in servers:
            s.state = ServerState.BUSY
        selector = ServerSelectorRandom(servers)
        self.assertIsNone(selector.select_idle())

    def test_select_interruption_returns_none_when_no_match(self):
        servers = make_servers(2)
        selector = ServerSelectorRandom(servers)
        self.assertIsNone(selector.select_interruption(TaskScope.TASK_1))

    def test_select_idle_returns_an_idle_server(self):
        servers = make_servers(3)
        servers[0].state = ServerState.BUSY
        selector = ServerSelectorRandom(servers)
        self.assertIn(selector.select_idle(), [1, 2])

    def test_select_interruption_returns_a_matching_server(self):
        servers = make_servers(3)
        servers[1].task_type = TaskScope.TASK_1
        selector = ServerSelectorRandom(servers)
        self.assertEqual(selector.select_interruption(TaskScope.TASK_1), 1)


if __name__ == "__main__":
    unittest.main()
