import unittest
from core.simulations.cloud.config.configuration import get_default_configuration
from core.simulations.cloud.simulation import SimpleCloudSimulation as Simulation
from core.simulations.cloud.statistics.report import generate_report


class SimulationCloudTest(unittest.TestCase):

    def test_verification_1(self):
        """
        Verify that every arrival have been served.
        :return: (void)
        """

        config = get_default_configuration()
        config["general"]["t_stop"] = 100

        simulation = Simulation(config)
        simulation.run()

        report = generate_report(simulation)

        self.assertTrue(report.get("system", "n_1") == report.get("system/cloudlet", "n_1") == report.get("system/cloud", "n_1") == 0)
        self.assertTrue(report.get("system", "n_2") == report.get("system/cloudlet", "n_2") == report.get("system/cloud", "n_2") == 0)

        self.assertTrue(report.get("system", "n_served_1") == report.get("system", "n_arrival_1") == report.get("tasks", "n_generated_1"))
        self.assertTrue(report.get("system", "n_served_2") == report.get("system", "n_arrival_2") == report.get("tasks", "n_generated_2"))

        self.assertTrue(report.get("system/cloudlet", "n_arrival_1") == report.get("system/cloudlet", "n_served_1"))
        self.assertTrue(report.get("system/cloudlet", "n_arrival_2") == report.get("system/cloudlet", "n_served_2") + report.get("system/cloudlet", "n_removed_2"))

        self.assertTrue(report.get("system/cloud", "n_arrival_1") == report.get("system/cloud", "n_served_1"))
        self.assertTrue(report.get("system/cloud", "n_arrival_2") == report.get("system/cloud", "n_served_2"))

        self.assertTrue(report.get("system/cloud", "n_restarted_2") == report.get("system/cloudlet", "n_removed_2"))

    def test_verification_2(self):
        """
        Verify that the model responses correctly to parameter changes.
        :return: (void)
        """

        config_1 = get_default_configuration()
        config_1["general"]["t_stop"] = 100

        simulation_1 = Simulation(config_1)
        simulation_1.run()

        report_1 = generate_report(simulation_1)

        config_2 = get_default_configuration()
        config_2["general"]["t_stop"] = 500

        simulation_2 = Simulation(config_2)
        simulation_2.run()

        report_2 = generate_report(simulation_2)

        self.assertTrue(report_1.get("system", "n_arrival_1") < report_2.get("system", "n_arrival_1"))
        self.assertTrue(report_1.get("system", "n_arrival_2") < report_2.get("system", "n_arrival_2"))


if __name__ == '__main__':
    unittest.main()
