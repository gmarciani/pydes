from enum import Enum, unique


@unique
class EventType(Enum):
    """
    The types of events.
    """
    ARRIVAL_TASK_1 = 0
    ARRIVAL_TASK_2 = 1
    COMPLETION_CLOUDLET_TASK_1 = 2
    COMPLETION_CLOUDLET_TASK_2 = 3
    COMPLETION_CLOUD_TASK_1 = 4
    COMPLETION_CLOUD_TASK_2 = 5


class SimpleEvent:
    """
    A simple event, defined by its type and occurrence time.
    """

    def __init__(self, type, time, meta=None):
        """
        Create a new event.
        :param type: (EventType) the type of the event.
        :param time: (float) the occurrence time of the event (s).
        :param meta: (dict) event metadata.
        """
        self.type = type
        self.time = time
        self.meta = meta

    def __str__(self):
        """
        String representation.
        :return: the string representation.
        """
        sb = ["{attr}='{value}'".format(attr=attr, value=self.__dict__[attr]) for attr in self.__dict__ if not attr.startswith("__") and not callable(getattr(self, attr))]
        return "Event({})".format(", ".join(sb))

    def __repr__(self):
        """
        String representation.
        :return: the string representation.
        """
        return self.__str__()

    def __eq__(self, other):
        if not isinstance(other, SimpleEvent):
            return False
        return self.type == other.type and self.time == other.time

    def __gt__(self, other):
        return self.time >= other.time

    def __lt__(self, other):
        return self.time < other.time

    def __hash__(self):
        return hash((self.type, self.time))


if __name__ == "__main__":
    # Creation
    event_1 = SimpleEvent(EventType.ARRIVAL_TASK_1, 10)
    print("Event 1:", event_1)
    event_2 = SimpleEvent(EventType.COMPLETION_CLOUDLET_TASK_1, 20)
    print("Event 2:", event_2)

    # Equality check
    print("Event 1 equals Event 2:", event_1 == event_2)