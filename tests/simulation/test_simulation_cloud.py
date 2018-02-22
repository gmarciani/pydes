import unittest
from core.simulation.config.configuration import get_default_configuration
from core.simulation.simulation import Simulation as Simulation


class SimulationCloudTest(unittest.TestCase):

    def setUp(self):
        """
        The test setup.
        :return: None
        """
        self.t_stop = 300

    def test_verification_flow_balance(self):
        """
        Verify the flow balance.
        :return: None
        """

        config = get_default_configuration()
        config["general"]["t_stop"] = self.t_stop

        simulation = Simulation(config)
        simulation.run()

        report = simulation.generate_report()

        self.assertEqual(0, int(report.get("system",          "n_1")))
        self.assertEqual(0, int(report.get("system/cloudlet", "n_1")))
        self.assertEqual(0, int(report.get("system/cloud",    "n_1")))

        self.assertEqual(0, int(report.get("system",          "n_2")))
        self.assertEqual(0, int(report.get("system/cloudlet", "n_2")))
        self.assertEqual(0, int(report.get("system/cloud",    "n_2")))

        self.assertEqual(int(report.get("tasks", "n_generated_1")), int(report.get("system", "n_arrival_1")))
        self.assertEqual(int(report.get("tasks", "n_generated_1")), int(report.get("system", "n_served_1")))

        self.assertEqual(int(report.get("tasks", "n_generated_2")), int(report.get("system", "n_arrival_2")))
        self.assertEqual(int(report.get("tasks", "n_generated_2")), int(report.get("system", "n_served_2")))

        self.assertEqual(int(report.get("system/cloudlet", "n_arrival_1")), int(report.get("system/cloudlet", "n_served_1")))
        self.assertEqual(int(report.get("system/cloudlet", "n_arrival_2")), int(report.get("system/cloudlet", "n_served_2")) + int(report.get("system/cloudlet", "n_interrupted_2")))

        self.assertEqual(int(report.get("system/cloud", "n_arrival_1")), int(report.get("system/cloud", "n_served_1")))
        self.assertEqual(int(report.get("system/cloud", "n_arrival_2")), int(report.get("system/cloud", "n_served_2")))

        self.assertEqual(int(report.get("system/cloudlet", "n_interrupted_2")), int(report.get("system/cloud", "n_restarted_2")))

    def test_verification_workload_change_duration(self):
        """
        Verify that the model responses correctly to workload changes (duration).
        :return: None
        """

        config_1 = get_default_configuration()
        config_1["general"]["t_stop"] = self.t_stop

        simulation_1 = Simulation(config_1)
        simulation_1.run()

        report_1 = simulation_1.generate_report()

        config_2 = get_default_configuration()
        config_2["general"]["t_stop"] = 2 * self.t_stop

        simulation_2 = Simulation(config_2)
        simulation_2.run()

        report_2 = simulation_2.generate_report()

        self.assertLess(int(report_1.get("system", "n_arrival_1")), int(report_2.get("system", "n_arrival_1")))
        self.assertLess(int(report_1.get("system", "n_arrival_2")), int(report_2.get("system", "n_arrival_2")))

    def test_verification_workload_change_arrival_rates(self):
        """
        Verify that the model responses correctly to workload changes (arrival rates).
        :return: None
        """

        config_1 = get_default_configuration()
        config_1["general"]["t_stop"] = self.t_stop
        config_1["tasks"]["arrival_rate_1"] = 3.25
        config_1["tasks"]["arrival_rate_2"] = 6.25

        simulation_1 = Simulation(config_1)
        simulation_1.run()

        report_1 = simulation_1.generate_report()

        config_2 = get_default_configuration()
        config_2["general"]["t_stop"] = self.t_stop
        config_2["tasks"]["arrival_rate_1"] = 4.25
        config_2["tasks"]["arrival_rate_2"] = 10.25

        simulation_2 = Simulation(config_2)
        simulation_2.run()

        report_2 = simulation_2.generate_report()

        self.assertGreater(float(report_2.get("tasks", "n_generated_1")), float(report_1.get("tasks", "n_generated_1")))
        self.assertGreater(float(report_2.get("tasks", "n_generated_2")), float(report_1.get("tasks", "n_generated_2")))

        self.assertGreater(float(report_2.get("system", "n_arrival_1")), float(report_1.get("system", "n_arrival_1")))
        self.assertGreater(float(report_2.get("system", "n_arrival_2")), float(report_1.get("system", "n_arrival_2")))

        self.assertGreater(float(report_2.get("system", "n_served_1")), float(report_1.get("system", "n_served_1")))
        self.assertGreater(float(report_2.get("system", "n_served_2")), float(report_1.get("system", "n_served_2")))

        self.assertGreater(float(report_2.get("system", "response_time")), float(report_1.get("system", "response_time")))
        self.assertGreater(float(report_2.get("system", "wasted_time")), float(report_1.get("system", "wasted_time")))
        self.assertLess(float(report_2.get("system", "throughput")), float(report_1.get("system", "throughput")))


    def test_verification_workload_change_service_rates(self):
        """
        Verify that the model responses correctly to workload changes (service rates).
        :return: None
        """

        config_1 = get_default_configuration()
        config_1["general"]["t_stop"] = self.t_stop
        config_1["system"]["cloudlet"]["service_rate_1"] = 0.45
        config_1["system"]["cloudlet"]["service_rate_2"] = 0.30
        config_1["system"]["cloud"]["service_rate_1"] = 0.25
        config_1["system"]["cloud"]["service_rate_2"] = 0.22

        simulation_1 = Simulation(config_1)
        simulation_1.run()

        report_1 = simulation_1.generate_report()

        config_2 = get_default_configuration()
        config_2["general"]["t_stop"] = self.t_stop
        config_2["system"]["cloudlet"]["service_rate_1"] = 0.10
        config_2["system"]["cloudlet"]["service_rate_2"] = 0.8
        config_2["system"]["cloud"]["service_rate_1"] = 0.5
        config_2["system"]["cloud"]["service_rate_2"] = 0.3

        simulation_2 = Simulation(config_2)
        simulation_2.run()

        report_2 = simulation_2.generate_report()

        self.assertGreater(float(report_2.get("system", "response_time")), float(report_1.get("system", "response_time")))
        self.assertLess(float(report_2.get("system", "throughput")), float(report_1.get("system", "throughput")))
        self.assertLess(float(report_2.get("system", "wasted_time")), float(report_1.get("system", "wasted_time")))


if __name__ == "__main__":
    unittest.main()

