import os
import unittest

from pydes.core.analytical.analytical_solution import AnalyticalSolution
from pydes.core.simulation.model.scope import SystemScope, TaskScope


class AnalyticalSolutionTest(unittest.TestCase):
    def setUp(self):
        self.solution = AnalyticalSolution()
        self.file_csv = "analytical_solution_test.csv"

    def tearDown(self):
        if os.path.exists(self.file_csv):
            os.remove(self.file_csv)

    def test_default_metrics_are_zero(self):
        for metric_name in ("response", "throughput", "population", "switched_ratio"):
            metric = getattr(self.solution.performance_metrics, metric_name)
            for sys in SystemScope:
                for tsk in TaskScope:
                    self.assertEqual(0.0, metric[sys][tsk])

    def test_metrics_are_independently_settable(self):
        self.solution.performance_metrics.response[SystemScope.CLOUDLET][TaskScope.TASK_1] = 2.5
        self.assertEqual(2.5, self.solution.performance_metrics.response[SystemScope.CLOUDLET][TaskScope.TASK_1])
        # Other entries are unaffected.
        self.assertEqual(0.0, self.solution.performance_metrics.response[SystemScope.CLOUDLET][TaskScope.TASK_2])
        self.assertEqual(0.0, self.solution.performance_metrics.throughput[SystemScope.CLOUDLET][TaskScope.TASK_1])

    def test_save_csv(self):
        self.solution.performance_metrics.response[SystemScope.SYSTEM][TaskScope.GLOBAL] = 1.5
        self.solution.performance_metrics.throughput[SystemScope.CLOUD][TaskScope.TASK_1] = 3.0

        self.solution.save_csv(self.file_csv)

        with open(self.file_csv, "r") as f:
            lines = f.read().splitlines()

        header = lines[0].split(",")
        row = lines[1].split(",")

        self.assertEqual(len(header), len(row))

        expected_columns = []
        for performance_metric in sorted(self.solution.performance_metrics.__dict__):
            for sys in SystemScope:
                for tsk in TaskScope:
                    expected_columns.append("{}_{}_{}".format(performance_metric, sys.name.lower(), tsk.name.lower()))
        self.assertEqual(expected_columns, header)

        idx = header.index("response_system_global")
        self.assertEqual("1.5", row[idx])

        idx = header.index("throughput_cloud_task_1")
        self.assertEqual("3.0", row[idx])

    def test_save_csv_append(self):
        self.solution.save_csv(self.file_csv)
        self.solution.save_csv(self.file_csv, append=True, skip_header=True)

        with open(self.file_csv, "r") as f:
            lines = f.read().splitlines()

        # One header line plus two data rows.
        self.assertEqual(3, len(lines))


if __name__ == "__main__":
    unittest.main()
