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

    def __init__(self, act, sys, tsk):
        self.act = act
        self.sys = sys
        self.tsk = tsk

    ARRIVAL_TASK_1 = ActionScope.ARRIVAL, SystemScope.SYSTEM, TaskScope.TASK_1
    ARRIVAL_TASK_2 = ActionScope.ARRIVAL, SystemScope.SYSTEM, TaskScope.TASK_2
    ARRIVAL_GLOBAL = ActionScope.ARRIVAL, SystemScope.SYSTEM, TaskScope.GLOBAL  # fake event type, used only in taskgen
    COMPLETION_CLOUDLET_TASK_1 = ActionScope.COMPLETION, SystemScope.CLOUDLET, TaskScope.TASK_1
    COMPLETION_CLOUDLET_TASK_2 = ActionScope.COMPLETION, SystemScope.CLOUDLET, TaskScope.TASK_2
    COMPLETION_CLOUD_TASK_1 = ActionScope.COMPLETION, SystemScope.CLOUD, TaskScope.TASK_1
    COMPLETION_CLOUD_TASK_2 = ActionScope.COMPLETION, SystemScope.CLOUD, TaskScope.TASK_2
    INTERRUPTION_CLOUDLET_TASK_1 = (
        ActionScope.INTERRUPTION,
        SystemScope.CLOUDLET,
        TaskScope.TASK_1,
    )  # fake event type, added only for simmetry
    INTERRUPTION_CLOUDLET_TASK_2 = ActionScope.INTERRUPTION, SystemScope.CLOUDLET, TaskScope.TASK_2
    RESTART_CLOUD_TASK_1 = (
        ActionScope.RESTART,
        SystemScope.CLOUD,
        TaskScope.TASK_1,
    )  # fake event type, added only for simmetry
    RESTART_CLOUD_TASK_2 = ActionScope.RESTART, SystemScope.CLOUD, TaskScope.TASK_2

    @staticmethod
    def arrivals():
        """
        Return the list of events representing an arrival.
        :return: the list of events representing an arrival.
        """
        return [EventType.ARRIVAL_TASK_1, EventType.ARRIVAL_TASK_2]

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
            if event_type.act is action and event_type.sys is sys and event_type.tsk is tsk:
                return event_type
        raise KeyError("Cannot find event type for action={}, scope={}, task={}".format(action, sys, tsk))

    def __str__(self):
        """
        Return the string representation.
        :return: the string representation.
        """
        return self.name

    def __repr__(self):
        """
        Return the string representation.
        :return: the string representation.
        """
        return self.__str__()


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
        sb = [
            "{attr}={value}".format(attr=attr, value=self.__dict__[attr])
            for attr in self.__dict__
            if not attr.startswith("__") and not callable(getattr(self, attr))
        ]
        return "Event({})".format(", ".join(sb))

    def __repr__(self):
        """
        Return the string representation.
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
