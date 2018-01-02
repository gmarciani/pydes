class Calendar(object):
    """
    Implementation of a Next-Event calendar.
    """

    def __init__(self, event_classes, t_clock=0.0):
        """
        Creates a new *Calendar*.
        :param event_classes: ([object]) list of event classes that the calendar
        will operate on; typically it a list of integers, or a list of strings.
        :param t_clock: (float) optional, initialization time for the clock.
        """
        self._clock = t_clock
        self._events = dict()
        for event_class in event_classes:
            self._events[event_class] = (float('inf'), None)

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

    def schedule(self, event_class, event_time, event_sid):
        """
        Schedules a new event.
        :param event_class: (object) the object representing the event class;
        must be one of those passed during the calendar initialization.
        :param event_time: (float) the occurrence time of the event.
        :param event_sid: (int) the session that the event belongs to.
        """
        self._events[event_class] = (event_time, event_sid)

    def mark_impossible(self, event_class):
        """
        Marks an event class as impossible. An impossible event is never
        returned as next event.
        :param event_class: (object) the object representing the event class;
        must be one of those passed during the calendar initialization.
        """
        self._events[event_class] = (float('inf'), None)

    def get_next_event(self):
        """
        Retrieves the next scheduled event.
        :return: ((c,t,s)) the event, where *c* is the event class, *t* is the
        occurrence time and *s* is the session that the event belongs to.
        """
        e = min(self._events.items(), key=lambda v: v[1][0])
        e_class = e[0]
        e_time = e[1][0]
        e_sid = e[1][1]
        return e_class, e_time, e_sid