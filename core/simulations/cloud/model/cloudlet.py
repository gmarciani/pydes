from core.simulations.cloud.model.server import SimpleServer as Server

class SimpleCloudLet:
    """
    A simple Cloudlet, defined by its state.
    """

    def __init__(self, n_servers):
        """
        Create a new cloudlet.
        :param n_servers: the number of servers.
        """
        self.n_servers = n_servers
        self.servers = [Server()] * self.n_servers
        self.n_jobs_1 = 0  # number of jobs of type 1
        self.n_jobs_2 = 0  # number of jobs of type 2

    def __str__(self):
        """
        String representation.
        :return: the string representation.
        """
        sb = ["{attr}='{value}'".format(attr=attr, value=self.__dict__[attr]) for attr in self.__dict__ if not attr.startswith('__') and not callable(getattr(self, attr))]
        return "Cloudlet({}:{})".format(id(self), ', '.join(sb))

    def __repr__(self):
        """
        String representation.
        :return: the string representation.
        """
        return self.__str__()

    def __eq__(self, other):
        if not isinstance(other, SimpleCloudLet):
            return False
        return id(self) == id(other)


if __name__ == "__main__":
    cloudlet_1 = SimpleCloudLet(10)
    print("Cloudlet 1:", cloudlet_1)
    cloudlet_2 = SimpleCloudLet(20)
    print("Cloudlet 2:", cloudlet_2)

    print("Cloudlet 1 equals Cloudlet 2:", cloudlet_1 == cloudlet_2)