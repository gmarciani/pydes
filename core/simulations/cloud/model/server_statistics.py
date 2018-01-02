class SimpleServerStatistics:
    """
    A simple collection of statistics for a server.
    """

    def __init__(self):
        """
        Create a new collection of server statistics.
        """
        self.n_served_jobs = 0  # the number of total served job
        self.n_served_jobs_1 = 0  # the number of served job of type 1
        self.n_served_jobs_2 = 0  # the number of served job of type 2
        self.t_wasted = 0.0  # the wasted time

    def __str__(self):
        """
        String representation.
        :return: the string representation.
        """
        sb = ["{attr}='{value}'".format(attr=attr, value=self.__dict__[attr]) for attr in self.__dict__ if not attr.startswith('__') and not callable(getattr(self, attr))]
        return "ServerStatistics({}:{})".format(id(self), ', '.join(sb))

    def __repr__(self):
        """
        String representation.
        :return: the string representation.
        """
        return self.__str__()

    def __eq__(self, other):
        if not isinstance(other, SimpleServerStatistics):
            return False
        return self.n_served_jobs == other.n_served_jobs and \
               self.n_served_jobs_1 == other.n_served_jobs_1 and \
               self.n_served_jobs_2 == other.n_served_jobs_2 and \
               self.t_wasted == other.t_wasted


if __name__ == "__main__":
    server_statistics_1 = SimpleServerStatistics()
    print("Server Statistics 1:", server_statistics_1)
    server_statistics_2 = SimpleServerStatistics()
    print("Server Statistics 2:", server_statistics_2)

    print("Server Statistics 1 equals Server Statistics 2:", server_statistics_1 == server_statistics_2)
