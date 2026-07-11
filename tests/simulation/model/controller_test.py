import unittest

from pydes.core.simulation.model.controller import (
    ControllerAlgorithm,
    ControllerAlgorithm1,
    ControllerAlgorithm2,
    ControllerResponse,
    SimpleController,
)
from pydes.core.simulation.model.scope import TaskScope


class SimpleControllerTest(unittest.TestCase):
    def test_process_not_implemented(self):
        """
        The base controller does not implement process().
        :return: None
        """
        controller = SimpleController(ControllerAlgorithm.ALGORITHM_1)
        with self.assertRaises(NotImplementedError):
            controller.process(TaskScope.TASK_1)

    def test_str(self):
        """
        Verify the string representation does not raise.
        :return: None
        """
        controller = SimpleController(ControllerAlgorithm.ALGORITHM_1)
        self.assertIn("Controller(", str(controller))


class ControllerAlgorithm1Test(unittest.TestCase):
    def setUp(self):
        self.n_servers = 2
        self.state = {TaskScope.TASK_1: 0, TaskScope.TASK_2: 0}
        self.controller = ControllerAlgorithm1(self.state, self.n_servers)

    def test_submit_to_cloudlet_when_servers_available(self):
        response = self.controller.process(TaskScope.TASK_1)
        self.assertEqual(response, ControllerResponse.SUBMIT_TO_CLOUDLET)

    def test_submit_to_cloud_when_servers_full(self):
        self.state[TaskScope.TASK_1] = 1
        self.state[TaskScope.TASK_2] = 1
        response = self.controller.process(TaskScope.TASK_2)
        self.assertEqual(response, ControllerResponse.SUBMIT_TO_CLOUD)


class ControllerAlgorithm2Test(unittest.TestCase):
    def setUp(self):
        self.n_servers = 5
        self.threshold = 3
        self.state = {TaskScope.TASK_1: 0, TaskScope.TASK_2: 0}
        self.controller = ControllerAlgorithm2(self.state, self.n_servers, self.threshold)

    def test_task_1_submit_to_cloud_when_cloudlet_full_of_task_1(self):
        self.state[TaskScope.TASK_1] = self.n_servers
        response = self.controller.process(TaskScope.TASK_1)
        self.assertEqual(response, ControllerResponse.SUBMIT_TO_CLOUD)

    def test_task_1_submit_to_cloudlet_below_threshold(self):
        self.state[TaskScope.TASK_1] = 1
        response = self.controller.process(TaskScope.TASK_1)
        self.assertEqual(response, ControllerResponse.SUBMIT_TO_CLOUDLET)

    def test_task_1_submit_to_cloudlet_with_interruption(self):
        # n1 + n2 >= threshold, n1 < n_servers, n2 > 0
        self.state[TaskScope.TASK_1] = 2
        self.state[TaskScope.TASK_2] = 1
        response = self.controller.process(TaskScope.TASK_1)
        self.assertEqual(response, ControllerResponse.SUBMIT_TO_CLOUDLET_WITH_INTERRUPTION)

    def test_task_1_submit_to_cloudlet_when_no_task_2_to_interrupt(self):
        # n1 + n2 >= threshold, n1 < n_servers, n2 == 0
        self.state[TaskScope.TASK_1] = 3
        self.state[TaskScope.TASK_2] = 0
        response = self.controller.process(TaskScope.TASK_1)
        self.assertEqual(response, ControllerResponse.SUBMIT_TO_CLOUDLET)

    def test_task_2_submit_to_cloud_when_above_threshold(self):
        self.state[TaskScope.TASK_1] = 2
        self.state[TaskScope.TASK_2] = 1
        response = self.controller.process(TaskScope.TASK_2)
        self.assertEqual(response, ControllerResponse.SUBMIT_TO_CLOUD)

    def test_task_2_submit_to_cloudlet_below_threshold(self):
        self.state[TaskScope.TASK_1] = 0
        self.state[TaskScope.TASK_2] = 0
        response = self.controller.process(TaskScope.TASK_2)
        self.assertEqual(response, ControllerResponse.SUBMIT_TO_CLOUDLET)

    def test_unrecognized_task_type_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.controller.process(TaskScope.GLOBAL)


if __name__ == "__main__":
    unittest.main()
