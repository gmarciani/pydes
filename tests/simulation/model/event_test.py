import unittest

from pydes.core.simulation.model.event import EventType
from pydes.core.simulation.model.event import SimpleEvent as Event
from pydes.core.simulation.model.scope import ActionScope, SystemScope, TaskScope


class EventTypeTest(unittest.TestCase):
    def test_arrivals(self):
        """
        Verify the list of arrival event types.
        :return: None
        """
        arrivals = EventType.arrivals()
        self.assertEqual(arrivals, [EventType.ARRIVAL_TASK_1, EventType.ARRIVAL_TASK_2])

    def test_of_returns_matching_event_type(self):
        """
        Verify that of() retrieves the event type matching action, scope and task.
        :return: None
        """
        event_type = EventType.of(ActionScope.COMPLETION, SystemScope.CLOUD, TaskScope.TASK_2)
        self.assertEqual(event_type, EventType.COMPLETION_CLOUD_TASK_2)

    def test_of_raises_key_error_when_not_found(self):
        """
        Verify that of() raises a KeyError when no event type matches.
        :return: None
        """
        with self.assertRaises(KeyError):
            EventType.of(ActionScope.INTERRUPTION, SystemScope.CLOUDLET, TaskScope.GLOBAL)

    def test_str_and_repr(self):
        """
        Verify the string and repr representations of an event type.
        :return: None
        """
        self.assertEqual(str(EventType.ARRIVAL_TASK_1), "ARRIVAL_TASK_1")
        self.assertEqual(repr(EventType.ARRIVAL_TASK_1), "ARRIVAL_TASK_1")


class SimpleEventTest(unittest.TestCase):
    def test_str_and_repr(self):
        """
        Verify that the string and repr representations do not raise and are equal.
        :return: None
        """
        event = Event(EventType.ARRIVAL_TASK_1, 1.5, t_arrival=1.5)
        self.assertIn("Event(", str(event))
        self.assertEqual(str(event), repr(event))

    def test_eq_with_non_event_returns_false(self):
        """
        Verify that comparing an event with a non-event object is always False.
        :return: None
        """
        event = Event(EventType.ARRIVAL_TASK_1, 1.0)
        self.assertFalse(event == "not-an-event")
        self.assertNotEqual(event, 42)

    def test_eq_with_matching_event(self):
        """
        Verify that two events with the same type and time are equal.
        :return: None
        """
        event_1 = Event(EventType.ARRIVAL_TASK_1, 1.0)
        event_2 = Event(EventType.ARRIVAL_TASK_1, 1.0)
        self.assertEqual(event_1, event_2)

    def test_gt_and_lt(self):
        """
        Verify the ordering operators based on event time.
        :return: None
        """
        earlier = Event(EventType.ARRIVAL_TASK_1, 1.0)
        later = Event(EventType.ARRIVAL_TASK_2, 2.0)
        same_time = Event(EventType.ARRIVAL_TASK_2, 1.0)

        self.assertTrue(later > earlier)
        self.assertTrue(earlier < later)
        self.assertFalse(later < earlier)
        # __gt__ uses >=, so events with equal time also compare as "greater".
        self.assertTrue(earlier > same_time)

    def test_hash(self):
        """
        Verify that events are hashable and consistent with equality.
        :return: None
        """
        event_1 = Event(EventType.ARRIVAL_TASK_1, 1.0)
        event_2 = Event(EventType.ARRIVAL_TASK_1, 1.0)
        self.assertEqual(hash(event_1), hash(event_2))


if __name__ == "__main__":
    unittest.main()
