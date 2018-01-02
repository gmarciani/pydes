from core.simulations.cloud.model.cloudlet import SimpleCloudLet as Cloudlet
from core.simulations.cloud.model.cloud import SimpleCloud as Cloud
from core.rnd import rndgen
from core.utils.report import SimpleReport as Report


class SimpleCloudSimulation:
    """
    A simple simulation about Cloud computing.
    """

    def __init__(self, config):
        """
        Create a new simulation.
        :param config: the configuration for the simulation
        """
        self.config = config

        # Configuration - General
        config_general = config["general"]
        self.t_stop = config_general["t_stop"]
        self.replica = config_general["replica"]
        self.rnd = getattr(rndgen, config_general["random"]["generator"])(config_general["random"]["seed"])

        # Configuration - Cloudlet
        config_cloudlet = self.config["cloudlet"]
        self.cloudlet = Cloudlet(config_cloudlet["n_servers"])

        # Configuration - Cloud
        config_cloud = self.config["cloud"]
        self.cloud = Cloud(config_cloud["t_service_rate_1"], config_cloud["t_service_rate_2"], config_cloud["t_setup"])

    def run(self):
        """
        Run the simulation.
        :return: the simulation report.
        """
        report = self.generate_report()
        return report

    def generate_report(self):
        report = Report('SIMULATION')
        report.add("general", "simulation_class", self.__class__.__name__)
        report.add("general", "t_stop", self.t_stop)
        report.add("general", "replica", self.replica)
        report.add("general", "random_generator", self.rnd.__class__.__name__)
        report.add("general", "random_seed", self.rnd.get_initial_seed())

        return report

    def __str__(self):
        """
        String representation.
        :return: the string representation.
        """
        sb = ["{attr}='{value}'".format(attr=attr, value=self.__dict__[attr]) for attr in self.__dict__ if not attr.startswith('__') and not callable(getattr(self, attr))]
        return "Simulation({}:{})".format(id(self), ', '.join(sb))

    def __repr__(self):
        """
        String representation.
        :return: the string representation.
        """
        return self.__str__()


if __name__ == "__main__":
    from core.simulations.cloud import default_configuration

    simulation_1 = SimpleCloudSimulation(default_configuration)

    print("Simulation 1", simulation_1)