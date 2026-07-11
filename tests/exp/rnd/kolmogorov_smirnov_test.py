import os
import tempfile
import unittest

from pydes.core.rnd.rndgen import MarcianiMultiStream
from pydes.exp.rnd import kolmogorov_smirnov


class KolmogorovSmirnovRunTest(unittest.TestCase):
    def setUp(self):
        """
        The test setup.
        :return: None
        """
        self.outdir = tempfile.mkdtemp()
        self.modulus = 127
        self.multiplier = 3
        self.jumper = 9
        self.streams = 20
        self.generator = MarcianiMultiStream(
            modulus=self.modulus, multiplier=self.multiplier, jumper=self.jumper, streams=self.streams
        )

    def test_run_extremes(self):
        """
        Verify that run() executes the Kolmogorov-Smirnov test on top of the extremes test with
        tiny parameters, and stores the raw statistics plus the report (txt and csv).
        :return: None
        """
        test_params = dict(samsize=100, bins=10, confidence=0.95, d=2)

        kolmogorov_smirnov.run(self.generator, "extremes", test_params, self.outdir)

        base = os.path.join(self.outdir, "mod{}_mul{}_str{}".format(self.modulus, self.multiplier, self.streams))

        self.assertTrue(os.path.isfile(base + ".csv"))
        self.assertTrue(os.path.isfile(base + "_report.txt"))
        self.assertTrue(os.path.isfile(base + "_report.csv"))

        with open(base + "_report.txt") as f:
            report_content = f.read()

        self.assertIn("TEST OF KOLMOGOROV-SMIRNOV", report_content)
        self.assertIn("KS Statistic", report_content)

    def test_run_unsupported_test_raises(self):
        """
        Verify that run() raises a ValueError for an unsupported test name.
        :return: None
        """
        with self.assertRaises(ValueError):
            kolmogorov_smirnov.run(self.generator, "not-a-test", {}, self.outdir)

    def test_run_not_implemented_test_raises(self):
        """
        Verify that run() raises a NotImplementedError for recognized-but-unimplemented test names.
        :return: None
        """
        for test_name in ("uniformity_u", "uniformity_b", "runsup", "gap", "permutation"):
            with self.assertRaises(NotImplementedError):
                kolmogorov_smirnov.run(self.generator, test_name, {}, self.outdir)


if __name__ == "__main__":
    unittest.main()
