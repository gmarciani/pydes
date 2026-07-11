import unittest

from pydes.core.metrics.simulation_metrics import SimulationMetrics
from pydes.core.rnd.rndgen import MarcianiMultiStream
from pydes.core.rnd.rndvar import Variate
from pydes.core.simulation.model.cloudlet import SimpleCloudlet
from pydes.core.simulation.model.controller import ControllerAlgorithm, ControllerAlgorithm1
from pydes.core.simulation.model.scope import TaskScope
from pydes.core.simulation.model.server import ServerState
from pydes.core.simulation.model.server_selection import SelectionRule


def make_config(n_servers=2, controller_algorithm=ControllerAlgorithm.ALGORITHM_1, threshold=None):
    config = {
        "service": {
            TaskScope.TASK_1: {"distribution": Variate.EXPONENTIAL, "parameters": {"m": 1.0}},
            TaskScope.TASK_2: {"distribution": Variate.EXPONENTIAL, "parameters": {"m": 1.0}},
        },
        "n_servers": n_servers,
        "server_selection": SelectionRule.ORDER,
        "controller_algorithm": controller_algorithm,
    }
    if threshold is not None:
        config["threshold"] = threshold
    return config


class SimpleCloudletTest(unittest.TestCase):
    def setUp(self):
        self.rndgen = MarcianiMultiStream()
        self.metrics = SimulationMetrics(10)
        self.state = {TaskScope.TASK_1: 0, TaskScope.TASK_2: 0}

    def test_algorithm_1_controller_is_used(self):
        """
        Verify that requesting ALGORITHM_1 wires up a ControllerAlgorithm1 controller.
        :return: None
        """
        cloudlet = SimpleCloudlet(
            self.rndgen, make_config(controller_algorithm=ControllerAlgorithm.ALGORITHM_1), self.state, self.metrics
        )
        self.assertIsInstance(cloudlet.controller, ControllerAlgorithm1)
        self.assertEqual(cloudlet.controller.controller_algorithm, ControllerAlgorithm.ALGORITHM_1)

    def test_algorithm_2_with_invalid_threshold_raises_value_error(self):
        """
        Verify that a threshold outside [0, n_servers] is rejected.
        :return: None
        """
        config = make_config(n_servers=2, controller_algorithm=ControllerAlgorithm.ALGORITHM_2, threshold=5)
        with self.assertRaises(ValueError):
            SimpleCloudlet(self.rndgen, config, self.state, self.metrics)

    def test_unrecognized_controller_algorithm_raises_value_error(self):
        """
        Verify that an unrecognized controller algorithm value is rejected.
        :return: None
        """
        config = make_config(controller_algorithm="NOT-A-REAL-ALGORITHM")
        with self.assertRaises(ValueError):
            SimpleCloudlet(self.rndgen, config, self.state, self.metrics)

    def test_submit_arrival_raises_runtime_error_when_no_idle_server(self):
        """
        If the external state accounting and the actual server states get out of sync (all servers
        busy despite the state counters allowing an arrival), submission must fail loudly.
        :return: None
        """
        cloudlet = SimpleCloudlet(self.rndgen, make_config(n_servers=2), self.state, self.metrics)
        for server in cloudlet.servers:
            server.state = ServerState.BUSY

        with self.assertRaises(RuntimeError):
            cloudlet.submit_arrival(TaskScope.TASK_1, 0.0)

    def test_submit_interruption_raises_runtime_error_when_no_matching_server(self):
        """
        Interrupting a task type with no server actually serving it must fail loudly.
        :return: None
        """
        cloudlet = SimpleCloudlet(self.rndgen, make_config(n_servers=2), self.state, self.metrics)
        self.state[TaskScope.TASK_1] = 1  # bypass the internal correctness assertion

        with self.assertRaises(RuntimeError):
            cloudlet.submit_interruption(TaskScope.TASK_1, 0.0)

    def test_submit_completion_raises_runtime_error_when_no_matching_server(self):
        """
        Completing a task type with no server serving it at the given completion time must fail loudly.
        :return: None
        """
        cloudlet = SimpleCloudlet(self.rndgen, make_config(n_servers=2), self.state, self.metrics)
        self.state[TaskScope.TASK_1] = 1  # bypass the internal correctness assertion

        with self.assertRaises(RuntimeError):
            cloudlet.submit_completion(TaskScope.TASK_1, 5.0, 0.0)

    def test_find_completion_server_idx_returns_none_when_not_found(self):
        """
        Verify the direct behaviour of find_completion_server_idx() when no server matches.
        :return: None
        """
        cloudlet = SimpleCloudlet(self.rndgen, make_config(n_servers=2), self.state, self.metrics)
        self.assertIsNone(cloudlet.find_completion_server_idx(TaskScope.TASK_1, 5.0))

    def test_str(self):
        """
        Verify the string representation does not raise.
        :return: None
        """
        cloudlet = SimpleCloudlet(self.rndgen, make_config(n_servers=2), self.state, self.metrics)
        self.assertIn("Cloudlet(", str(cloudlet))


if __name__ == "__main__":
    unittest.main()
