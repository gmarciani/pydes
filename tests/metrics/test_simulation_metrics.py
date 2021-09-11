import unittest
from core.metrics.simulation_metrics import SimulationMetrics
from core.simulation.model.scope import SystemScope
from core.simulation.model.scope import TaskScope


class SimulationMetricsTest(unittest.TestCase):
    def setUp(self):
        self.simulation_metrics = SimulationMetrics(10)

        for metric in self.simulation_metrics.performance_metrics.__dict__:
            for sys in SystemScope:
                for tsk in TaskScope:
                    getattr(self.simulation_metrics.performance_metrics, metric)[sys][tsk].set_value(hash(metric))

        self.simulation_metrics.register_batch()

        for metric in self.simulation_metrics.performance_metrics.__dict__:
            for sys in SystemScope:
                for tsk in TaskScope:
                    getattr(self.simulation_metrics.performance_metrics, metric)[sys][tsk].set_value(
                        hash(metric), batch=0
                    )

        self.file_csv = "out/test_simulation_statistics.csv"

    def test_save_csv(self):
        """
        Test the statistics saving to a CSV file.
        :return: None
        """
        hdr = ["batch"]
        row = [0]

        for metric in sorted(self.simulation_metrics.performance_metrics.__dict__):
            for sys in SystemScope:
                for tsk in TaskScope:
                    hdr.append("{}_{}_{}".format(metric, sys.name.lower(), tsk.name.lower()))
                    row.append(hash(metric))
        shdr = ",".join(map(str, hdr))
        srow = ",".join(map(str, row))
        expected = "{}\n{}\n".format(shdr, srow)

        self.simulation_metrics.save_csv(self.file_csv)

        with open(self.file_csv, "r") as f:
            actual = f.read()

        self.assertEqual(expected, actual, "CSV file representation is not correct.")


if __name__ == "__main__":
    unittest.main()
