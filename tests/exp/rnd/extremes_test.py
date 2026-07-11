import os
import tempfile
import unittest

from pydes.core.rnd.rndgen import MarcianiMultiStream
from pydes.exp.rnd import extremes


class ExtremesRunTest(unittest.TestCase):
    def setUp(self):
        """
        The test setup.
        :return: None
        """
        self.outdir = tempfile.mkdtemp()
        self.modulus = 127
        self.multiplier = 3
        self.jumper = 9
        # Note: the number of streams must be large enough so that the theoretical error
        # (round((1 - confidence) * streams)) is not zero, otherwise a ZeroDivisionError
        # is raised downstream while computing the empirical/theoretical error ratio.
        self.streams = 20
        self.generator = MarcianiMultiStream(
            modulus=self.modulus, multiplier=self.multiplier, jumper=self.jumper, streams=self.streams
        )

    def test_run(self):
        """
        Verify that run() executes the extremes test of randomness with tiny sample size/bins
        and stores the raw chi-square statistics plus the report (txt and csv).
        :return: None
        """
        samsize = 100
        bins = 10
        confidence = 0.95
        d = 2

        extremes.run(self.generator, samsize, bins, confidence, d, self.outdir)

        base = os.path.join(self.outdir, "mod{}_mul{}_str{}".format(self.modulus, self.multiplier, self.streams))

        self.assertTrue(os.path.isfile(base + ".csv"))
        self.assertTrue(os.path.isfile(base + "_report.txt"))
        self.assertTrue(os.path.isfile(base + "_report.csv"))

        with open(base + ".csv") as f:
            rows = f.read().strip().splitlines()

        # header + one row per stream
        self.assertEqual(self.streams + 1, len(rows))

        with open(base + "_report.txt") as f:
            report_content = f.read()

        self.assertIn("TEST OF EXTREMES", report_content)
        self.assertIn("Success", report_content)


if __name__ == "__main__":
    unittest.main()
