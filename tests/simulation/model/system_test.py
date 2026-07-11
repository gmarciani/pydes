import unittest
from types import SimpleNamespace

from pydes.core.simulation.model.event import EventType
from pydes.core.simulation.model.event import SimpleEvent as Event
from pydes.core.simulation.model.scope import SystemScope, TaskScope
from pydes.core.simulation.model.system import SimpleCloudletCloudSystem


class FakeSystem(SimpleCloudletCloudSystem):
    """
    A system subclass that skips constructing real Cloudlet/Cloud subsystems, so that the pure
    dispatch logic in submit()/submit_completion() can be tested in isolation.
    """

    def __init__(self):
        self.state = {sys: {tsk: 0 for tsk in TaskScope.concrete()} for sys in SystemScope.subsystems()}
        self.metrics = None
        self.cloudlet = SimpleNamespace()
        self.cloud = SimpleNamespace()


class SimpleCloudletCloudSystemTest(unittest.TestCase):
    def setUp(self):
        self.system = FakeSystem()

    def test_submit_unrecognized_event_action_raises_value_error(self):
        """
        Only ARRIVAL and COMPLETION events are supported by submit().
        :return: None
        """
        event = Event(EventType.INTERRUPTION_CLOUDLET_TASK_2, 1.0)
        with self.assertRaises(ValueError):
            self.system.submit(event)

    def test_submit_completion_unrecognized_scope_raises_value_error(self):
        """
        submit_completion() only supports CLOUDLET and CLOUD scopes. The internal state dict is only
        ever keyed by those two subsystem scopes, so to exercise the "unrecognized scope" branch in
        isolation, a fake scope key has to be injected directly into the state.
        :return: None
        """
        fake_scope = "FAKE_SCOPE"
        self.system.state[fake_scope] = {TaskScope.TASK_1: 1}

        with self.assertRaises(ValueError):
            self.system.submit_completion(TaskScope.TASK_1, fake_scope, 1.0, SimpleNamespace(t_arrival=0.0))

    def test_submit_arrival_unrecognized_controller_response_raises_value_error(self):
        """
        submit_arrival() only handles the three known ControllerResponse values; an unrecognized
        response from the controller must fail loudly rather than being silently ignored.
        :return: None
        """
        self.system.cloudlet.controller = SimpleNamespace(process=lambda tsk: "NOT-A-REAL-RESPONSE")

        with self.assertRaises(ValueError):
            self.system.submit_arrival(TaskScope.TASK_1, 0.0)

    def test_is_idle_delegates_to_subsystems(self):
        """
        Verify that is_idle() combines both subsystem idle states.
        :return: None
        """
        self.system.cloudlet.is_idle = lambda: True
        self.system.cloud.is_idle = lambda: True
        self.assertTrue(self.system.is_idle())

        self.system.cloud.is_idle = lambda: False
        self.assertFalse(self.system.is_idle())

    def test_str(self):
        """
        Verify the string representation does not raise.
        :return: None
        """
        self.assertIn("System(", str(self.system))


if __name__ == "__main__":
    unittest.main()
