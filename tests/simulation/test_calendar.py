import unittest
from core.simulation.model.calendar import NextEventCalendar
from core.simulation.model.event import SimpleEvent as Event
from core.simulation.model.event import EventType
from core.rnd.rndgen import MarcianiMultiStream


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


if __name__ == "__main__":
    unittest.main()
