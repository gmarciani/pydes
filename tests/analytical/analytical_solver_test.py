import copy
import unittest

from pydes.core.analytical.analytical_solver import AnalyticalSolver
from pydes.core.analytical.markov_chains import (
    MarkovChainAlgorithm1,
    MarkovChainAlgorithm2,
)
from pydes.core.simulation.model.scope import SystemScope, TaskScope


def _base_config(controller_algorithm="ALGORITHM_1", n_servers=1, threshold=None):
    config = {
        "arrival": {
            "TASK_1": {"distribution": "EXPONENTIAL", "parameters": {"r": 6.0}},
            "TASK_2": {"distribution": "EXPONENTIAL", "parameters": {"r": 6.25}},
        },
        "system": {
            "cloudlet": {
                "n_servers": n_servers,
                "controller_algorithm": controller_algorithm,
                "service": {
                    "TASK_1": {"distribution": "EXPONENTIAL", "parameters": {"r": 0.45}},
                    "TASK_2": {"distribution": "EXPONENTIAL", "parameters": {"r": 0.27}},
                },
            },
            "cloud": {
                "service": {
                    "TASK_1": {"distribution": "EXPONENTIAL", "parameters": {"r": 0.25}},
                    "TASK_2": {"distribution": "EXPONENTIAL", "parameters": {"r": 0.22}},
                },
                "setup": {
                    "TASK_2": {"parameters": {"m": 0.8}},
                },
            },
        },
    }
    if threshold is not None:
        config["system"]["cloudlet"]["threshold"] = threshold
    return config


class AnalyticalSolverAlgorithm1Test(unittest.TestCase):
    def setUp(self):
        self.config = _base_config(controller_algorithm="ALGORITHM_1", n_servers=2)
        self.solver = AnalyticalSolver(self.config)

    def test_init_parses_config(self):
        self.assertEqual(2, self.solver.clt_n_servers)
        self.assertIsNone(self.solver.clt_threshold)
        self.assertEqual(6.0, self.solver.arrival_rates[TaskScope.TASK_1])
        self.assertEqual(6.25, self.solver.arrival_rates[TaskScope.TASK_2])
        self.assertEqual(0.45, self.solver.service_rates[SystemScope.CLOUDLET][TaskScope.TASK_1])
        self.assertEqual(0.25, self.solver.service_rates[SystemScope.CLOUD][TaskScope.TASK_1])
        self.assertEqual(0.8, self.solver.t_setup)

    def test_validate_markovianity_rejects_non_exponential(self):
        bad_config = copy.deepcopy(self.config)
        bad_config["arrival"]["TASK_1"]["distribution"] = "DETERMINISTIC"
        with self.assertRaises(AssertionError):
            AnalyticalSolver(bad_config)

    def test_solve_builds_markov_chain(self):
        self.solver.solve()
        self.assertIsInstance(self.solver.markov_chain, MarkovChainAlgorithm1)
        self.assertIsNotNone(self.solver.states_probabilities)
        total = sum(self.solver.states_probabilities.values())
        self.assertAlmostEqual(1.0, total)

    def test_solve_populates_solution_metrics(self):
        self.solver.solve()
        solution = self.solver.solution

        # Global system throughput must equal the sum of arrival rates.
        x_sys_global = solution.performance_metrics.throughput[SystemScope.SYSTEM][TaskScope.GLOBAL]
        self.assertAlmostEqual(
            self.solver.arrival_rates[TaskScope.TASK_1] + self.solver.arrival_rates[TaskScope.TASK_2],
            x_sys_global,
        )

        # All population metrics must be non-negative.
        for sys in SystemScope:
            for tsk in TaskScope:
                self.assertGreaterEqual(solution.performance_metrics.population[sys][tsk], 0.0)

    def test_routing_probabilities_algorithm_1(self):
        self.solver.solve()
        routing = self.solver.routing_probabilities
        self.assertEqual(
            routing["routing_accepted_clt_1"],
            routing["routing_accepted_clt_2"],
        )
        self.assertEqual(0.0, routing["routing_accepted_clt_2_restarted"])

    def test_generate_report(self):
        self.solver.solve()
        report = self.solver.generate_report()

        self.assertEqual(6.0, report.get("arrival", "arrival_task_1_rate"))
        self.assertEqual(2, report.get("system/cloudlet", "n_servers"))
        self.assertEqual("ALGORITHM_1", report.get("system/cloudlet", "controller_algorithm"))
        self.assertIsNone(report.get("system/cloudlet", "threshold"))

        n_sys_global = report.get("statistics", "population_system_global_mean")
        self.assertIsNotNone(n_sys_global)
        self.assertGreaterEqual(n_sys_global, 0.0)

        for state in self.solver.states_probabilities:
            self.assertEqual(self.solver.states_probabilities[state], report.get("states probability", state))

    def test_solve_with_unrecognized_controller_algorithm_raises(self):
        self.solver.clt_controller_algorithm = None
        with self.assertRaises(ValueError):
            self.solver.solve()

    def test_compute_routing_probabilities_with_unrecognized_controller_algorithm_raises(self):
        self.solver.solve()
        self.solver.clt_controller_algorithm = None
        with self.assertRaises(ValueError):
            self.solver._AnalyticalSolver__compute_routing_probabilities()


class AnalyticalSolverAlgorithm2Test(unittest.TestCase):
    def setUp(self):
        self.config = _base_config(controller_algorithm="ALGORITHM_2", n_servers=2, threshold=1)
        self.solver = AnalyticalSolver(self.config)

    def test_init_parses_threshold(self):
        self.assertEqual(1, self.solver.clt_threshold)

    def test_solve_builds_markov_chain(self):
        self.solver.solve()
        self.assertIsInstance(self.solver.markov_chain, MarkovChainAlgorithm2)
        total = sum(self.solver.states_probabilities.values())
        self.assertAlmostEqual(1.0, total)

    def test_routing_probabilities_algorithm_2(self):
        self.solver.solve()
        routing = self.solver.routing_probabilities
        for value in routing.values():
            self.assertGreaterEqual(value, 0.0)

    def test_generate_report_includes_threshold(self):
        self.solver.solve()
        report = self.solver.generate_report()
        self.assertEqual(1, report.get("system/cloudlet", "threshold"))


if __name__ == "__main__":
    unittest.main()
