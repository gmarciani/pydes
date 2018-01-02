class SimpleJob:
    """
    A simple job, defined by its type and arrival time.
    """

    def __init__(self, type, t_arrival):
        """
        Create a new job.
        :param type: the type of the job.
        :param t_arrival: the arrival time of the job.
        """
        self.type = type
        self.t_arrival = t_arrival

    def __str__(self):
        """
        String representation.
        :return: the string representation.
        """
        sb = ["{attr}='{value}'".format(attr=attr, value=self.__dict__[attr]) for attr in self.__dict__ if not attr.startswith('__') and not callable(getattr(self, attr))]
        return "Job({}:{})".format(id(self), ', '.join(sb))

    def __repr__(self):
        """
        String representation.
        :return: the string representation.
        """
        return self.__str__()

    def __eq__(self, other):
        if not isinstance(other, SimpleJob):
            return False
        return self.type == other.type and self.t_arrival == other.t_arrival


if __name__ == "__main__":
    job_1 = SimpleJob("type_1", 0)
    print("Job 1:", job_1)
    job_2 = SimpleJob("type_1", 0)
    print("Job 2:", job_2)
    job_3 = SimpleJob("type_2", 10)
    print("Job 3:", job_3)

    print("Job 1 equals Job 2:", job_1 == job_2)
    print("Job 1 equals Job 3:", job_1 == job_3)