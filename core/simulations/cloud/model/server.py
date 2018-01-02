from core.simulations.cloud.model.server_statistics import SimpleServerStatistics as ServerStatistics

class SimpleServer:
    """
    A simple Server, defined by its state.
    """

    def __init__(self, type=0):
        """
        Create a new server.
        :param type: the server type (default: 0).
        """
        self.status_free = True  # the status of the server: True if free, False otherwise
        self.type = type  # the job type: it can be 1 or 2
        self.t_arrival = 0.0  # the arrival time
        self.t_service = 0.0  # the total service time
        self.t_service_1 = 0.0  # the service time for job of type 1
        self.t_service_2 = 0.0  # the service time for job of type 2
        self.t_completion = 0.0  # the completion time
        self.statistics = ServerStatistics()  # the server statistics

    def addServiceTime(self, t_new_service):
        """
        Add the specified service time to the server, due to job schedule.
        :param t_new_service: the service time to add.
        :return: void
        """
        self.t_service += t_new_service
        if self.type == 1:
            self.t_service_1 += t_new_service
        else:
            self.t_service_2 += t_new_service

    def subServiceTime(self, t_new_arrival):
        """
        Subtracts the spcified service time to the server, due to job swap.
        :param t: the service time to subtract.
        :return: void
        """
        _t = self.t_completion - t_new_arrival
        self.t_service -= _t
        self.t_service_2 -= _t

    def utilization(self, t_stop):
        """
        Return the server utilization for the specified stop time.
        :param t_stop: the stop time.
        :return: the server utilization
        """
        return self.t_service / t_stop

    def __str__(self):
        """
        String representation.
        :return: the string representation.
        """
        sb = ["{attr}='{value}'".format(attr=attr, value=self.__dict__[attr]) for attr in self.__dict__ if not attr.startswith("__") and not callable(getattr(self, attr))]
        return "Server({}:{})".format(id(self), ", ".join(sb))

    def __repr__(self):
        """
        String representation.
        :return: the string representation.
        """
        return self.__str__()

    def __eq__(self, other):
        if not isinstance(other, SimpleServer):
            return False
        return id(self) == id(other)


if __name__ == "__main__":
    server_1 = SimpleServer()
    print("Server 1:", server_1)
    server_2 = SimpleServer()
    print("Server 2:", server_2)

    print("Server 1 equals Server 2:", server_1 == server_2)