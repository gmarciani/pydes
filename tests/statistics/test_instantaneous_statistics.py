import unittest
from core.simulation.model.statistics import InstantaneousStatistics
from core.simulation.model.scope import SystemScope
from core.simulation.model.scope import TaskScope


class InstantaneousStatisticsTest(unittest.TestCase):

    def setUp(self):
        """
        The test setup.
        :return: None
        """
        self.stat = InstantaneousStatistics(0)

        for metric in self.stat.metrics.__dict__:
            for sys in SystemScope:
                for tsk in TaskScope:
                    getattr(self.stat.metrics, metric)[sys][tsk] = hash(metric)

        self.file_csv = "out/test_instantaneous_statistics.csv"

    def test_save_csv(self):
        """
        Test the statistics saving to a CSV file.
        :return: None
        """
        hdr = ["time"]
        row = [0]

        for metric in sorted(self.stat.metrics.__dict__):
            for sys in SystemScope:
                for tsk in TaskScope:
                    hdr.append("{}_{}_{}".format(metric, sys.name.lower(), tsk.name.lower()))
                    row.append(hash(metric))

        shdr = ",".join(map(str, hdr))
        srow = ",".join(map(str, row))
        expected = "{}\n{}\n".format(shdr, srow)

        self.stat.save_csv(self.file_csv)

        with open(self.file_csv, "r") as f:
            actual = f.read()

        self.assertEqual(expected, actual, "CSV file representation is not correct.")


if __name__ == "__main__":
    unittest.main()
