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
    RESTART_TASK_2 = 6


class SimpleEvent:
    """
    A simple event, defined by its type, occurrence time and metadata.
    """

    def __init__(self, type, time, **kwargs):
        """
        Create a new event.
        :param type: (EventType) the type of the event.
        :param time: (float) the occurrence time of the event (s).
        :param kwargs: (dict) optional metadata.
        """
        self.type = type
        self.time = time
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __str__(self):
        """
        String representation.
        :return: the string representation.
        """
        sb = ["{attr}={value}".format(attr=attr, value=self.__dict__[attr]) for attr in self.__dict__ if
              not attr.startswith("__") and not callable(getattr(self, attr))]
        return "Event({})".format(", ".join(sb))

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
    e = SimpleEvent(EventType.COMPLETION_CLOUDLET_TASK_1, 10, t_service=5)
    print(e)