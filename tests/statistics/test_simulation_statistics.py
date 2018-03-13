import unittest
from core.simulation.model.statistics import SimulationStatistics
from core.simulation.model.scope import SystemScope
from core.simulation.model.scope import TaskScope


class SimulationStatisticsTest(unittest.TestCase):

    def setUp(self):
        """
        The test setup.
        :return: None
        """
        self.stat = SimulationStatistics(10)

        for metric in self.stat.metrics.__dict__:
            for sys in SystemScope:
                for tsk in TaskScope:
                    getattr(self.stat.metrics, metric)[sys][tsk].set_value(hash(metric))

        self.stat.register_batch()

        self.file_csv = "out/test_simulation_statistics.csv"

    def test_save_csv(self):
        """
        Test the statistics saving to a CSV file.
        :return: None
        """
        hdr = ["batch"]
        row = [0]

        for metric in sorted(self.stat.metrics.__dict__):
            for sys in SystemScope:
                for tsk in TaskScope:
                    hdr.append("{}_{}_{}".format(metric, sys.name.lower(), tsk.name.lower()))
                    if metric == "response":
                        value = self.stat.metrics.service[sys][tsk].get_value(batch=0) / self.stat.metrics.completed[sys][tsk].get_value(batch=0) \
                            if self.stat.metrics.completed[sys][tsk].get_value(batch=0) > 0 else 0
                    elif metric == "throughput":
                        value = self.stat.metrics.completed[sys][tsk].get_value(batch=0) / self.stat.t_batch
                    else:
                        value = hash(metric)
                    row.append(value)
        shdr = ",".join(map(str, hdr))
        srow = ",".join(map(str, row))
        expected = "{}\n{}\n".format(shdr, srow)

        self.stat.save_csv(self.file_csv)

        with open(self.file_csv, "r") as f:
            actual = f.read()

        self.assertEqual(expected, actual, "CSV file representation is not correct.")


if __name__ == "__main__":
    unittest.main()
