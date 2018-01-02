from enum import Enum

class TaskType(Enum):
    """
    The types of tasks.
    """
    TASK_1 = 1
    TASK_2 = 2

class SimpleTask:
    """
    A simple task, defined by its type and arrival time.
    """

    def __init__(self, type, t_arrival):
        """
        Create a new job.
        :param type: (TaskType) the type of the task.
        :param t_arrival: (float) the arrival time of the task (s).
        """
        self.type = type
        self.t_arrival = t_arrival

    def __str__(self):
        """
        String representation.
        :return: the string representation.
        """
        sb = ["{attr}='{value}'".format(attr=attr, value=self.__dict__[attr]) for attr in self.__dict__ if not attr.startswith("__") and not callable(getattr(self, attr))]
        return "Task({}:{})".format(id(self), ", ".join(sb))

    def __repr__(self):
        """
        String representation.
        :return: the string representation.
        """
        return self.__str__()

    def __eq__(self, other):
        if not isinstance(other, SimpleTask):
            return False
        return self.type == other.type and self.t_arrival == other.t_arrival


if __name__ == "__main__":
    task_1 = SimpleTask(TaskType.TASK_1, 0)
    print("Task 1:", task_1)
    task_2 = SimpleTask(TaskType.TASK_1, 0)
    print("Task 2:", task_2)
    task_3 = SimpleTask(TaskType.TASK_2, 10)
    print("Task 3:", task_3)

    print("Task 1 equals Task 2:", task_1 == task_2)
    print("Task 1 equals Task 3:", task_1 == task_3)