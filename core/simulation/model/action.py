from enum import Enum, unique


@unique
class Action(Enum):
    """
    The actions:
        * arrival
        * completion
        * interruption
        * restart
    """
    ARRIVAL = 0
    COMPLETION = 1
    INTERRUPTION = 2
    RESTART = 3