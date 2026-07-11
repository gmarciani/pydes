import unittest
from enum import Enum

from pydes.core.rnd.rndvar import Variate
from pydes.core.simulation.model.config import get_default_configuration
from pydes.core.simulation.model.scope import TaskScope
from pydes.core.simulation.model.server_selection import SelectionRule
from pydes.core.simulation.simulation import Simulation as Simulation
from pydes.core.simulation.simulation_mode import SimulationMode


class SimulationCloudTest(unittest.TestCase):
    def setUp(self):
        """
        The test setup.
        :return: None
        """
        self.n_batch = 3
        self.t_batch = 50

    def test_run(self):
        """
        Check the absence of exception for notable configurations.
        :return: None
        """
        config = get_default_configuration()
        config["general"]["n_batch"] = self.n_batch
        config["general"]["t_batch"] = self.t_batch

        for ssr in SelectionRule:
            print("Server Selection Rule: ", ssr.name)
            config["system"]["cloudlet"]["server_selection"] = ssr
            simulation = Simulation(config)
            simulation.run(outdir="out/simulation_test")

    def test_run_performance_analysis_and_report(self):
        """
        Run a small PERFORMANCE_ANALYSIS simulation, with progress reporting enabled, and generate its report.
        :return: None
        """
        config = get_default_configuration(SimulationMode.PERFORMANCE_ANALYSIS)
        config["general"]["batches"] = 2
        config["general"]["batchdim"] = 5

        simulation = Simulation(config, name="PERFORMANCE-ANALYSIS-TEST")
        simulation.run(outdir="out/simulation_test/performance_analysis", show_progress=True)

        self.assertTrue(simulation.stop_condition())
        self.assertGreaterEqual(simulation.metrics.n_batches, config["general"]["batches"])

        report = simulation.generate_report()
        self.assertEqual(report.get("general", "batches"), config["general"]["batches"])
        self.assertEqual(report.get("general", "batchdim"), config["general"]["batchdim"])
        self.assertIsNone(report.get("general", "t_stop"))

        report_str = str(report)
        self.assertIn("PERFORMANCE_ANALYSIS", report_str)

        # __str__ of the simulation itself should also work without error.
        self.assertIn("Simulation(", str(simulation))

    def test_run_transient_analysis_and_report(self):
        """
        Run a small TRANSIENT_ANALYSIS simulation, with progress reporting enabled, and generate its report.
        :return: None
        """
        config = get_default_configuration(SimulationMode.TRANSIENT_ANALYSIS)
        config["general"]["t_stop"] = 100

        simulation = Simulation(config, name="TRANSIENT-ANALYSIS-TEST")
        simulation.run(outdir="out/simulation_test/transient_analysis", show_progress=True)

        self.assertTrue(simulation.stop_condition())
        self.assertGreaterEqual(simulation.calendar.get_clock(), config["general"]["t_stop"])

        report = simulation.generate_report()
        self.assertEqual(report.get("general", "t_stop"), config["general"]["t_stop"])
        self.assertIsNone(report.get("general", "batches"))
        self.assertIsNone(report.get("general", "batchdim"))

        report_str = str(report)
        self.assertIn("TRANSIENT_ANALYSIS", report_str)

    def test_invalid_mode_raises_runtime_error(self):
        """
        Construction with an unsupported simulation mode must fail loudly.
        :return: None
        """
        with self.assertRaises(RuntimeError):
            Simulation({"general": {"mode": "NOT-A-REAL-MODE"}})

    def test_non_exponential_arrival_raises_not_implemented(self):
        """
        Only exponential arrival processes are currently supported.
        :return: None
        """
        config = get_default_configuration()
        config["arrival"][TaskScope.TASK_1]["distribution"] = Variate.DETERMINISTIC

        with self.assertRaises(NotImplementedError):
            Simulation(config)

    def test_generate_report_with_non_exponential_service_distribution(self):
        """
        Cover the report branches for non-exponential service distributions, both in the Cloudlet
        and in the Cloud.
        :return: None
        """
        config = get_default_configuration()
        config["general"]["batches"] = 1
        config["general"]["batchdim"] = 2
        config["system"]["cloudlet"]["service"][TaskScope.TASK_1]["distribution"] = Variate.DETERMINISTIC
        config["system"]["cloudlet"]["service"][TaskScope.TASK_1]["parameters"] = {"v": 0.5}
        config["system"]["cloud"]["service"][TaskScope.TASK_1]["distribution"] = Variate.DETERMINISTIC
        config["system"]["cloud"]["service"][TaskScope.TASK_1]["parameters"] = {"v": 0.5}

        simulation = Simulation(config, name="NON-EXPONENTIAL-SERVICE-TEST")
        simulation.run(outdir="out/simulation_test/non_exponential_service")

        report = simulation.generate_report()
        self.assertEqual(report.get("system/cloudlet", "service_task_1_param_v"), 0.5)
        self.assertEqual(report.get("system/cloud", "service_task_1_param_v"), 0.5)

    def test_generate_report_invalid_mode_raises_runtime_error(self):
        """
        generate_report() must reject an unsupported simulation mode, even if constructed elsewhere.
        :return: None
        """
        config = get_default_configuration()
        config["general"]["batches"] = 1
        config["general"]["batchdim"] = 2
        simulation = Simulation(config)
        simulation.run(outdir="out/simulation_test/invalid_report_mode")

        class BogusMode(Enum):
            OTHER = 0

        simulation.mode = BogusMode.OTHER

        with self.assertRaises(RuntimeError):
            simulation.generate_report()

    @unittest.skip("Under Debugging")
    def test_flow_consistency(self):
        """
        Flow consistency check.
        :return: None
        """

        config = get_default_configuration()
        config["general"]["n_batch"] = self.n_batch
        config["general"]["t_batch"] = self.t_batch

        simulation = Simulation(config)
        simulation.run()

        for task_type in TaskScope:
            self.assertEqual(simulation.taskgen.generated[task_type], simulation.system.arrived[task_type])

            self.assertEqual(
                simulation.system.n[task_type],
                simulation.system.arrived[task_type] - simulation.system.completed[task_type],
            )

            self.assertEqual(
                simulation.system.cloudlet.n[task_type],
                simulation.system.cloudlet.arrived[task_type]
                - simulation.system.cloudlet.completed[task_type]
                - simulation.system.cloudlet.switched[task_type],
            )

            self.assertEqual(
                simulation.system.cloud.n[task_type],
                simulation.system.cloud.arrived[task_type]
                + simulation.system.cloud.switched[task_type]
                - simulation.system.cloud.completed[task_type],
            )

            self.assertEqual(
                simulation.system.cloudlet.switched[task_type], simulation.system.cloud.switched[task_type]
            )

    @unittest.skip("Under Debugging")
    def test_workload_change_consistency_1(self):
        """
        Verify that the model responses correctly to workload changes (arrival rates).
        :return: None
        """

        config_1 = get_default_configuration()
        config_1["general"]["n_batch"] = self.n_batch
        config_1["general"]["t_batch"] = self.t_batch
        config_1["tasks"]["arrival_rate_1"] = 3.25
        config_1["tasks"]["arrival_rate_2"] = 6.25

        simulation_1 = Simulation(config_1)
        simulation_1.run()

        config_2 = get_default_configuration()
        config_2["general"]["n_batch"] = self.n_batch
        config_2["general"]["t_batch"] = self.t_batch
        config_2["tasks"]["arrival_rate_1"] = 4.25
        config_2["tasks"]["arrival_rate_2"] = 10.25

        simulation_2 = Simulation(config_2)
        simulation_2.run()

        for task_type in TaskScope:
            self.assertGreater(simulation_2.taskgen.generated[task_type], simulation_1.taskgen.generated[task_type])

            self.assertGreater(simulation_2.system.arrived[task_type], simulation_1.system.arrived[task_type])

            self.assertGreater(simulation_2.system.completed[task_type], simulation_1.system.completed[task_type])

        self.assertGreater(simulation_2.metrics.response.mean(), simulation_1.metrics.response.mean())

        self.assertLess(simulation_2.metrics.throughput.mean(), simulation_1.metrics.throughput.mean())

    @unittest.skip("Under Debugging")
    def test_workload_change_consistency(self):
        """
        Verify that the model responses correctly to workload changes (service rates).
        :return: None
        """

        config_1 = get_default_configuration()
        config_1["general"]["n_batch"] = self.n_batch
        config_1["general"]["t_batch"] = self.t_batch
        config_1["system"]["cloudlet"]["service_rate_1"] = 0.45
        config_1["system"]["cloudlet"]["service_rate_2"] = 0.30
        config_1["system"]["cloud"]["service_rate_1"] = 0.25
        config_1["system"]["cloud"]["service_rate_2"] = 0.22

        simulation_1 = Simulation(config_1)
        simulation_1.run()

        config_2 = get_default_configuration()
        config_2["general"]["n_batch"] = self.n_batch
        config_2["general"]["t_batch"] = self.t_batch
        config_2["system"]["cloudlet"]["service_rate_1"] = 0.10
        config_2["system"]["cloudlet"]["service_rate_2"] = 0.8
        config_2["system"]["cloud"]["service_rate_1"] = 0.5
        config_2["system"]["cloud"]["service_rate_2"] = 0.3

        simulation_2 = Simulation(config_2)
        simulation_2.run()

        self.assertGreater(simulation_2.metrics.t_response.mean(), simulation_1.metrics.t_response.mean())

        self.assertLess(simulation_2.metrics.throughput.mean(), simulation_1.metrics.throughput.mean())


if __name__ == "__main__":
    unittest.main()
