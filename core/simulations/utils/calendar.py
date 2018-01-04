from queue import PriorityQueue
from core.simulations.cloud.model.event import SimpleEvent as Event
import logging

# Configure logger
logger = logging.getLogger(__name__)


class NextEventCalendar:
    """
    Implementation of a simple Next-Event calendar.
    """

    def __init__(self, t_clock=0.0):
        """
        Create a new *NextEventCalendar*.
        :param event_types: ([object]) list of event classes that the calendar
        will operate on; typically it a list of integers, or a list of strings.
        :param t_clock: (float) optional, initialization time for the clock.
        """
        self._clock = t_clock
        self._events = PriorityQueue()
        self._ignore = set()

    def get_clock(self):
        """
        Retrieves the calendar clock.
        :return: (float) the calendar clock.
        """
        return self._clock

    def set_clock(self, t):
        """
        Set the calendar clock.
        :param t: (float) time to set the calendar clock to.
        """
        self._clock = t

    def schedule(self, *events):
        """
        Schedule events.
        :param events: (SimpleEvent) the events to schedule.
        """
        for ev in events:
            self._events.put((ev.time, ev))
            logger.debug("Scheduled: {}".format(ev))

    def unschedule(self, *events):
        """
        Unschedule events.
        :param events: (SimpleEvent) the events to unschedule.
        """
        for ev in events:
            self._ignore.add(ev)
            logger.debug("Unscheduled: {}".format(ev))

    def get_next_event(self):
        """
        Retrieve the next scheduled event and update the clock.
        :return: (SimpleEvent) the next event, if present; None, otherwise.
        """
        if self._events.empty():
            return None
        else:
            candidate = self._events.get()[1]
            while candidate in self._ignore:
                self._ignore.discard(candidate)
                candidate = self._events.get()[1]
            self.set_clock(candidate.time)
            return candidate

    def is_empty(self):
        """
        Check if the calendar is empty.
        :return: True, if the calendar is empty; False, otherwise.
        """
        return self._events.empty()

    def __str__(self):
        """
        String representation.
        :return: the string representation.
        """
        sb = ["{attr}='{value}'".format(attr=attr, value=self.__dict__[attr]) for attr in self.__dict__ if not attr.startswith("__") and not callable(getattr(self, attr))]
        return "Calendar({}:{})".format(id(self), ", ".join(sb))

    def __repr__(self):
        """
        String representation.
        :return: the string representation.
        """
        return self.__str__()


if __name__ == "__main__":
    from core.simulations.cloud.model.event import EventType
    from core.rnd.rndgen import MarcianiMultiStream

    rndgen = MarcianiMultiStream(123456789)

    # Creation
    print("--- CREATION ---")
    calendar = NextEventCalendar()
    print(calendar)

    # Calendar loop without unscheduling
    print("--- CALENDAR LOOP WITHOUT UNSCHEDULING ---")

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
    while not calendar.is_empty():
        event = calendar.get_next_event()
        assert event == _events[_idx]
        print("Event: {} | clock: {}".format(event, calendar.get_clock()))
        _idx += 1

    # Calendar loop with unscheduling
    print("--- CALENDAR LOOP WITH UNSCHEDULING ---")

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
            print("Unscheduled: ", _ev)
    _events[:] = [x for x in _events if not x.type == EventType.ARRIVAL_TASK_2]

    # step 3: test
    _events.sort()
    _idx = 0
    while not calendar.is_empty():
        event = calendar.get_next_event()
        assert event == _events[_idx]
        print("Event: {} | clock: {}".format(event, calendar.get_clock()))
        _idx += 1