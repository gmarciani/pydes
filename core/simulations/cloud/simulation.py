from core.simulations.cloud.model.cloudlet import SimpleCloudLet as Cloudlet
from core.simulations.cloud.model.cloud import SimpleCloud as Cloud
from core.rnd import rndgen
from core.simulations.cloud.model.taskgen import SimpleTaskgen as Taskgen
from core.simulations.utils.calendar import NextEventCalendar as Calendar
from core.utils.report import SimpleReport as Report
from enum import Enum


class Event(Enum):
    """
    Simulation events.
    """
    TASK_1_ARRIVAL = 0
    TASK_2_ARRIVAL = 1
    TASK_1_COMPLETION = 2
    TASK_2_COMPLETION = 3


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

        # Configuration - Tasks
        config_tasks = config["tasks"]
        self.taskgen = Taskgen(
            config_tasks["arrival_rate_1"],
            config_tasks["arrival_rate_2"]
        )

        # Configuration - Cloudlet
        config_cloudlet = self.config["cloudlet"]
        self.cloudlet = Cloudlet(
            config_cloudlet["n_servers"],
            config_cloudlet["service_rate_1"],
            config_cloudlet["service_rate_2"],
            config_cloudlet["threshold"]
        )

        # Configuration - Cloud
        config_cloud = self.config["cloud"]
        self.cloud = Cloud(config_cloud["service_rate_1"], config_cloud["service_rate_2"], config_cloud["t_setup_mean"])

        # Configuration _ Calendar
        self.calendar = Calendar([
            Event.TASK_1_ARRIVAL,
            Event.TASK_2_ARRIVAL,
            Event.TASK_1_COMPLETION,
            Event.TASK_2_COMPLETION
        ], t_clock=0.0)

    def run(self):
        """
        Run the simulation.
        :return: the simulation report.
        """
        # Simulation Core

        # Reporting
        report = self.generate_report()
        return report

    def generate_report(self):
        report = Report('SIMULATION')

        # Report - General
        report.add("general", "simulation_class", self.__class__.__name__)
        report.add("general", "t_stop", self.t_stop)
        report.add("general", "replica", self.replica)
        report.add("general", "random_generator", self.rnd.__class__.__name__)
        report.add("general", "random_seed", self.rnd.get_initial_seed())

        # Report - Tasks
        for attr in self.taskgen.__dict__:
            if not attr.startswith("__") and not attr.startswith("_") and not callable(getattr(self.taskgen, attr)):
                report.add("tasks", attr, self.taskgen.__dict__[attr])

        # Report - Cloudlet
        for attr in self.cloudlet.__dict__:
            if not attr.startswith("__") and not attr.startswith("_") and not callable(getattr(self.cloudlet, attr)):
                report.add("cloudlet", attr, self.cloudlet.__dict__[attr])

        # Report - Cloud
        for attr in self.cloud.__dict__:
            if not attr.startswith("__") and not attr.startswith("_") and not callable(getattr(self.cloud, attr)):
                report.add("cloud", attr, self.cloud.__dict__[attr])

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
    from core.simulations.cloud.config.configuration import default_configuration

    simulation_1 = SimpleCloudSimulation(default_configuration)

    print("Simulation 1", simulation_1)