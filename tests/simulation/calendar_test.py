import unittest

from pydes.core.rnd.rndgen import MarcianiMultiStream
from pydes.core.simulation.model.calendar import NextEventCalendar
from pydes.core.simulation.model.event import EventType
from pydes.core.simulation.model.event import SimpleEvent as Event


class CalendarTest(unittest.TestCase):
    def test_scheduling_simple(self):
        """
        Verify the correctness of scheduling, without unscheduling.
        :return: None
        """
        rndgen = MarcianiMultiStream()

        # Creation
        calendar = NextEventCalendar()

        # step 1: schedule
        _events = []
        for event_type in EventType:
            for i in range(10):
                u = rndgen.rnd()
                event = Event(event_type, u)
                calendar.schedule(event)
                _events.append(event)

        # step 3: test
        _events.sort()
        _idx = 0
        while not calendar.empty():
            event = calendar.get_next_event()
            self.assertEqual(_events[_idx], event)
            _idx += 1

    def test_scheduling_advanced(self):
        """
        Verify the correctness f scheduling, with unscheduling.
        :return: None
        """
        rndgen = MarcianiMultiStream()

        # Creation
        calendar = NextEventCalendar()

        # step 1: schedule
        _events = []
        for event_type in EventType:
            for i in range(10):
                u = rndgen.rnd()
                event = Event(event_type, u)
                calendar.schedule(event)
                _events.append(event)

        # step 2: unschedule
        for _ev in _events:
            if _ev.type is EventType.ARRIVAL_TASK_2:
                calendar.unschedule(_ev)
        _events[:] = [x for x in _events if not x.type == EventType.ARRIVAL_TASK_2]

        # step 3: test
        _events.sort()
        _idx = 0
        while not calendar.empty():
            event = calendar.get_next_event()
            self.assertEqual(_events[_idx], event)
            _idx += 1

    def test_get_next_event_on_empty_calendar_returns_none(self):
        """
        Verify that requesting the next event from an empty calendar returns None.
        :return: None
        """
        calendar = NextEventCalendar()
        self.assertTrue(calendar.empty())
        self.assertIsNone(calendar.get_next_event())

    def test_schedule_impossible_arrival_is_ignored(self):
        """
        Verify that an arrival scheduled beyond the stop time is not scheduled but counted as ignored.
        :return: None
        """
        calendar = NextEventCalendar(t_clock=0.0, t_stop=10.0)

        possible = Event(EventType.ARRIVAL_TASK_1, 5.0)
        impossible = Event(EventType.ARRIVAL_TASK_1, 10.0)

        nscheduled, nignored = calendar.schedule(possible, impossible)

        self.assertEqual(nscheduled, 1)
        self.assertEqual(nignored, 1)

        event = calendar.get_next_event()
        self.assertEqual(event, possible)
        self.assertTrue(calendar.empty())

    def test_schedule_non_arrival_events_are_not_bounded_by_stop_time(self):
        """
        Verify that non-ARRIVAL events are always scheduled, regardless of the stop time.
        :return: None
        """
        calendar = NextEventCalendar(t_clock=0.0, t_stop=10.0)

        event = Event(EventType.COMPLETION_CLOUDLET_TASK_1, 100.0)
        nscheduled, nignored = calendar.schedule(event)

        self.assertEqual(nscheduled, 1)
        self.assertEqual(nignored, 0)

    def test_schedule_handles_type_error(self):
        """
        Verify that a scheduling error (e.g. events with non-comparable times) is handled gracefully,
        without scheduling the offending event and without raising.
        :return: None
        """
        calendar = NextEventCalendar()

        # A normal, comparable event.
        calendar.schedule(Event(EventType.COMPLETION_CLOUDLET_TASK_1, 1.0))

        # An event with a time that cannot be compared against a float: triggers a TypeError
        # internally when the underlying priority queue attempts to order it.
        offending = Event(EventType.COMPLETION_CLOUDLET_TASK_1, complex(1, 2))
        nscheduled, nignored = calendar.schedule(offending)

        self.assertEqual(nscheduled, 0)
        self.assertEqual(nignored, 0)

    def test_str(self):
        """
        Verify that the string representation does not raise and contains useful info.
        :return: None
        """
        calendar = NextEventCalendar(t_clock=1.0)
        text = str(calendar)
        self.assertIn("Calendar(", text)


if __name__ == "__main__":
    unittest.main()
