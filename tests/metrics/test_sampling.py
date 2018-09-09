import unittest
from core.metrics.stats import Sample
from core.simulation.model.scope import SystemScope
from core.simulation.model.scope import TaskScope


class SamplingTest(unittest.TestCase):

    def setUp(self):
        """
        The test setup.
        :return: None
        """
        self.sample = Sample(0)

        for counter in self.sample.counters.__dict__:
            for sys in SystemScope:
                for tsk in TaskScope:
                    getattr(self.sample.counters, counter)[sys][tsk] = hash(counter)

        for metric in self.sample.metrics.__dict__:
            for sys in SystemScope:
                for tsk in TaskScope:
                    getattr(self.sample.metrics, metric)[sys][tsk] = hash(metric)

        self.file_csv = "out/test_sample.csv"

    def test_save_csv(self):
        """
        Test the statistics saving to a CSV file.
        :return: None
        """
        hdr = ["time"]
        row = [0]

        for counter in sorted(self.sample.counters.__dict__):
            for sys in SystemScope:
                for tsk in TaskScope:
                    hdr.append("{}_{}_{}".format(counter, sys.name.lower(), tsk.name.lower()))
                    row.append(hash(counter))

        for metric in sorted(self.sample.metrics.__dict__):
            for sys in SystemScope:
                for tsk in TaskScope:
                    hdr.append("{}_{}_{}".format(metric, sys.name.lower(), tsk.name.lower()))
                    row.append(hash(metric))

        shdr = ",".join(map(str, hdr))
        srow = ",".join(map(str, row))
        expected = "{}\n{}\n".format(shdr, srow)

        self.sample.save_csv(self.file_csv)

        with open(self.file_csv, "r") as f:
            actual = f.read()

        self.assertEqual(expected, actual, "CSV file representation is not correct.")


if __name__ == "__main__":
    unittest.main()
