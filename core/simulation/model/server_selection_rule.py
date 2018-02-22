from enum import Enum, unique

from core.simulation.model.server_selector import ServerSelectorOrder
from core.simulation.model.server_selector import ServerSelectorCyclic
from core.simulation.model.server_selector import ServerSelectorEquity
from core.simulation.model.server_selector import ServerSelectorRandom


@unique
class SelectionRule(Enum):
    """
    Enumerate server-selection rules.
    """

    def __new__(cls, *args, **kwds):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, selector):
        self.selector = selector

    ORDER = ServerSelectorOrder  # 0  Order Selection
    CYCLIC = ServerSelectorCyclic  # 1 Cyclic Selection
    EQUITY = ServerSelectorEquity  # 2 Equity Selection
    RANDOM = ServerSelectorRandom  # 3 Random Selection