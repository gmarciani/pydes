from enum import Enum, unique


@unique
class Action(Enum):
    """
    The actions:
        * arrival
        * completion
        * switch
    """
    ARRIVAL = 0
    COMPLETION = 1
    SWITCH = 2