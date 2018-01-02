class SimpleCloud:
    """
    A simple Cloud server, defined by its state.
    """

    def __init__(self, service_rate_1, service_rate_2, t_setup_mean):
        """
        Create a new Cloud server.
        :param service_rate_1: (float) the service rate for job of type 1 (tasks/s).
        :param service_rate_2: (float) the service rate for job of type 2 (tasks/s).
        :param t_setup_mean: (float) the mean setup time to restart a task of type 2 in the Cloud (s).
        """
        self.service_rate_1 = service_rate_1
        self.service_rate_2 = service_rate_2
        self.t_setup_mean = t_setup_mean

        self.t_service = 0.0
        self.t_service_1 = 0.0
        self.t_service_2 = 0.0
        self.t_max_completion = 0.0
        self.t_max_completion_1 = 0.0
        self.t_max_completion_2 = 0.0
        self.t_service_swapped = 0.0
        self.n_served = 0
        self.n_served_1 = 0
        self.n_served_2 = 0
        self.n_swapped_2 = 0

    def __str__(self):
        """
        String representation.
        :return: the string representation.
        """
        sb = ["{attr}='{value}'".format(attr=attr, value=self.__dict__[attr]) for attr in self.__dict__ if not attr.startswith("__") and not callable(getattr(self, attr))]
        return "Cloud({}:{})".format(id(self), ", ".join(sb))

    def __repr__(self):
        """
        String representation.
        :return: the string representation.
        """
        return self.__str__()

    def __eq__(self, other):
        if not isinstance(other, SimpleCloud):
            return False
        return id(self) == id(other)


if __name__ == "__main__":
    cloud_1 = SimpleCloud(0.25, 0.35, 3)
    print("Cloud 1:", cloud_1)
    cloud_2 = SimpleCloud(0.25, 0.35, 3)
    print("Cloud 2:", cloud_2)

    print("Cloud 1 equals Cloud 2:", cloud_1 == cloud_2)