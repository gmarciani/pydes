import unittest
from core.simulation.config.configuration import get_default_configuration
from core.simulation.model.task import TaskType
from core.simulation.simulation import Simulation as Simulation


class SimulationCloudTest(unittest.TestCase):

    def setUp(self):
        """
        The test setup.
        :return: None
        """
        self.n_batch = 1
        self.t_batch = 200

    def test_verification_flow_balance(self):
        """
        Verify the flow balance.
        :return: None
        """

        config = get_default_configuration()
        config["general"]["n_batch"] = self.n_batch
        config["general"]["t_batch"] = self.t_batch

        simulation = Simulation(config)
        simulation.run()

        for task_type in TaskType:
            self.assertEqual(simulation.taskgen.generated[task_type],
                             simulation.system.arrived[task_type])

            self.assertEqual(simulation.system.arrived[task_type],
                             simulation.system.n[task_type] + simulation.system.completed[task_type])

            self.assertEqual(simulation.system.cloudlet.arrived[task_type],
                             simulation.system.cloudlet.n[task_type] + simulation.system.cloudlet.completed[task_type] +
                             simulation.system.cloudlet.interrupted[task_type])

            self.assertEqual(simulation.system.cloud.arrived[task_type],
                             simulation.system.cloudlet.n[task_type] + simulation.system.cloudlet.completed[task_type])

            self.assertEqual(simulation.system.cloudlet.interrupted[task_type],
                             simulation.system.cloud.restarted[task_type])

    def test_verification_workload_change_duration(self):
        """
        Verify that the model responses correctly to workload changes (duration).
        :return: None
        """

        config_1 = get_default_configuration()
        config_1["general"]["n_batch"] = self.n_batch
        config_1["general"]["t_batch"] = self.t_batch

        simulation_1 = Simulation(config_1)
        simulation_1.run()

        config_2 = get_default_configuration()
        config_2["general"]["n_batch"] = self.n_batch
        config_2["general"]["t_batch"] = 2 * self.t_batch

        simulation_2 = Simulation(config_2)
        simulation_2.run()

        for task_type in TaskType:
            self.assertGreater(simulation_2.system.arrived[task_type],
                               simulation_1.system.arrived[task_type])

    def test_verification_workload_change_arrival_rates(self):
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

        for task_type in TaskType:
            self.assertGreater(simulation_2.taskgen.generated[task_type],
                               simulation_1.taskgen.generated[task_type])

            self.assertGreater(simulation_2.system.arrived[task_type],
                               simulation_1.system.arrived[task_type])

            self.assertGreater(simulation_2.system.completed[task_type],
                               simulation_1.system.completed[task_type])

        self.assertGreater(simulation_2.statistics.t_response.mean(),
                           simulation_1.statistics.t_response.mean())

        self.assertLess(simulation_2.statistics.throughput.mean(),
                        simulation_1.statistics.throughput.mean())

    def test_verification_workload_change_service_rates(self):
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

        self.assertGreater(simulation_2.statistics.t_response.mean(),
                           simulation_1.statistics.t_response.mean())

        self.assertLess(simulation_2.statistics.throughput.mean(),
                        simulation_1.statistics.throughput.mean())


if __name__ == "__main__":
    unittest.main()

