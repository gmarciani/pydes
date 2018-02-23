from enum import Enum, unique


@unique
class Task(Enum):
    """
    The types of tasks.
    """
    TASK_1 = 1
    TASK_2 = 2