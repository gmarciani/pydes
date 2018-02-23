from enum import Enum, unique


@unique
class Scope(Enum):
    """
    The actions:
        * system
        * cloudlet
        * cloud
    """
    SYSTEM = 0
    CLOUDLET = 1
    CLOUD = 2