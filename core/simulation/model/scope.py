from enum import Enum, unique


@unique
class SystemScope(Enum):
    """
    The scope of events:
        * SYSTEM
        * CLOUDLET
        * CLOUD
    """
    SYSTEM = 0
    CLOUDLET = 1
    CLOUD = 2

    @staticmethod
    def subsystems():
        """
        Return the subsystem scopes only.
        :return: the subsystems scopes only.
        """
        return list(x for x in SystemScope if x is not SystemScope.SYSTEM)

@unique
class TaskScope(Enum):
    """
    The scope ot tasks:
        * TASK_1
        * TASK_2
        * GLOBAL (special scope used in statistics)
    """
    GLOBAL = 0
    TASK_1 = 1
    TASK_2 = 2

    @staticmethod
    def concrete():
        """
        Return the concrete task scopes only.
        :return: the concrete task scopes only.
        """
        return list(x for x in TaskScope if x is not TaskScope.GLOBAL)

@unique
class ActionScope(Enum):
    """
    The scope of event actions:
        * ARRIVAL
        * COMPLETION
        * SWITCH
    """
    ARRIVAL = 0
    COMPLETION = 1
    SWITCH = 2