from enum import Enum, unique


@unique
class SimulationMode(Enum):
    """
    A simulation can be executed according to this modes:
        * PERFORMANCE_ANALYSIS
        * TRANSIENT_ANALYSIS
    """

    def __new__(cls, *args, **kwds):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    PERFORMANCE_ANALYSIS = 0
    TRANSIENT_ANALYSIS = 1


if __name__ == "__main__":
    mode_1 = SimulationMode["PERFORMANCE_ANALYSIS"]
    print(mode_1)

    mode_2 = SimulationMode["TRANSIENT_ANALYSIS"]
    print(mode_2)
