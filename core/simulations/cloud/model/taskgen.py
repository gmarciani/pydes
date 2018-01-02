class SimpleTaskgen:
    """
    A simple tasks generator.
    """

    def __init__(self, arrival_rate_1, arrival_rate_2):
        """
        Create a new tasks generator.
        :param arrival_rate_1: (float) the arrival rate for tasks of type 1 (tasks/s).
        :param arrival_rate_2: (float) the arrival rate for tasks of type 2 (tasks/s).
        """
        self.arrival_rate_1 = arrival_rate_1
        self.arrival_rate_2 = arrival_rate_2

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
        if not isinstance(other, SimpleTaskgen):
            return False
        return self.arrival_rate_1 == other.arrival_rate_1 and \
               self.arrival_rate_2 == other.arrival_rate_2


if __name__ == "__main__":
    taskgen_1 = SimpleTaskgen(0.5, 0.25)
    print("Taskgen 1:", taskgen_1)
    taskgen_2 = SimpleTaskgen(0.5, 0.25)
    print("Taskgen 2:", taskgen_2)
    taskgen_3 = SimpleTaskgen(0.25, 0.125)
    print("Taskgen 3:", taskgen_3)

    print("Taskgen 1 equals Taskgen 2:", taskgen_1 == taskgen_2)
    print("Taskgen 1 equals Taskgen 3:", taskgen_1 == taskgen_3)