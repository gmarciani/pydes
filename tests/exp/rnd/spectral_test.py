import os
import tempfile
import unittest

from pydes.core.rnd.rndgen import MarcianiSingleStream
from pydes.exp.rnd import spectral


class SpectralRunTest(unittest.TestCase):
    def setUp(self):
        """
        The test setup.
        :return: None
        """
        self.outdir = tempfile.mkdtemp()
        self.modulus = 127
        self.multiplier = 3
        self.generator = MarcianiSingleStream(modulus=self.modulus, multiplier=self.multiplier)

    def test_run(self):
        """
        Verify that run() executes the spectral test of randomness with a tiny sample size
        and stores the raw observations plus the report (txt and csv).
        :return: None
        """
        samsize = 200
        interval = (0.0, 1.0)

        spectral.run(self.generator, samsize, interval, self.outdir)

        base = os.path.join(self.outdir, "mod{}_mul{}".format(self.modulus, self.multiplier))

        self.assertTrue(os.path.isfile(base + ".csv"))
        self.assertTrue(os.path.isfile(base + "_report.txt"))
        self.assertTrue(os.path.isfile(base + "_report.csv"))

        with open(base + ".csv") as f:
            csv_content = f.read()

        self.assertIn("u1,u2", csv_content)

        with open(base + "_report.txt") as f:
            report_content = f.read()

        self.assertIn("SPECTRAL TEST", report_content)
        self.assertIn("Sample Size", report_content)


if __name__ == "__main__":
    unittest.main()
