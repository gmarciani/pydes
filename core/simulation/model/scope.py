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

@unique
class TaskScope(Enum):
    """
    The scope ot tasks:
        * TASK_1
        * TASK_2
        * GLOBAL (special scope used in statistics)
    """
    TASK_1 = 1
    TASK_2 = 2
    GLOBAL = 3

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