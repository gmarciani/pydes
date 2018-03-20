from enum import Enum, unique

from core.simulation.model.scope import ActionScope
from core.simulation.model.scope import SystemScope
from core.simulation.model.scope import TaskScope
from types import SimpleNamespace


@unique
class EventType(Enum):
    """
    The types of events.
    """
    def __new__(cls, *args, **kwds):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, action, scope, task):
        self.action = action
        self.scope = scope
        self.task = task

    ARRIVAL_TASK_1 = ActionScope.ARRIVAL, SystemScope.SYSTEM, TaskScope.TASK_1  # 0
    ARRIVAL_TASK_2 = ActionScope.ARRIVAL, SystemScope.SYSTEM, TaskScope.TASK_2  # 1
    COMPLETION_CLOUDLET_TASK_1 = ActionScope.COMPLETION, SystemScope.CLOUDLET, TaskScope.TASK_1  # 2
    COMPLETION_CLOUDLET_TASK_2 = ActionScope.COMPLETION, SystemScope.CLOUDLET, TaskScope.TASK_2  # 3
    COMPLETION_CLOUD_TASK_1 = ActionScope.COMPLETION, SystemScope.CLOUD, TaskScope.TASK_1  # 4
    COMPLETION_CLOUD_TASK_2 = ActionScope.COMPLETION, SystemScope.CLOUD, TaskScope.TASK_2  # 5
    SWITCH_TASK_1 = ActionScope.SWITCH, SystemScope.SYSTEM, TaskScope.TASK_1  # 6
    SWITCH_TASK_2 = ActionScope.SWITCH, SystemScope.SYSTEM, TaskScope.TASK_2  # 7

    @staticmethod
    def arrivals():
        """
        Return the list of events representing an arrival.
        :return: the list of events representing an arrival.
        """
        return [EventType.ARRIVAL_TASK_1, EventType.ARRIVAL_TASK_2]

    @staticmethod
    def is_arrival(etype):
        """
        Check whether a event type is an arrival.
        :param etype: (EventType) the type of event.
        :return: the list of events representing an arrival.
        """
        return etype is EventType.ARRIVAL_TASK_1 or etype is EventType.ARRIVAL_TASK_2

    @staticmethod
    def of(action, sys, tsk):
        """
        Return the event type from action, scope and task.
        :param action: (Action) the action.
        :param sys: (Scope) the scope.
        :param tsk:  (TaskType) the task type.
        :return: (EventType) the event type.
        """
        for event_type in EventType:
            if event_type.action is action and event_type.scope is sys and event_type.task is tsk:
                return event_type
        raise KeyError("Cannot find event type for action={}, scope={}, task={}".format(action, sys, tsk))


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
        self.meta = SimpleNamespace(**kwargs)

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