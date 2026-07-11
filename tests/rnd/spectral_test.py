import os
import shutil
import tempfile
import unittest

from pydes.core.rnd.randomness import spectral
from pydes.core.rnd.rndgen import MarcianiSingleStream
from pydes.core.utils.csv_utils import read_csv


class SpectralTest(unittest.TestCase):
    def setUp(self):
        self.outdir = tempfile.mkdtemp()
        self.generator = MarcianiSingleStream()

    def tearDown(self):
        shutil.rmtree(self.outdir, ignore_errors=True)

    def test_statistics_writes_observations_within_interval(self):
        # A wide interval keeps (almost) every pair, forcing at least one
        # in-loop flush (MAX_OBSERVATIONS_BEFORE_FLUSH == 10) plus the final
        # flush of the remaining buffered rows.
        filename = os.path.join(self.outdir, "sub", "out.csv")

        spectral.statistics(filename, self.generator, samsize=50, interval=(0.0, 1.0))

        rows = read_csv(filename)
        self.assertGreater(len(rows), 0)
        for row in rows:
            u1 = float(row["u1"])
            u2 = float(row["u2"])
            self.assertTrue(0.0 <= u1 <= 1.0)
            self.assertTrue(0.0 <= u2 <= 1.0)

    def test_statistics_skips_pairs_outside_narrow_interval(self):
        filename = os.path.join(self.outdir, "narrow.csv")

        spectral.statistics(filename, self.generator, samsize=50, interval=(0.4, 0.6))

        rows = read_csv(filename)
        for row in rows:
            u1 = float(row["u1"])
            u2 = float(row["u2"])
            self.assertTrue(0.4 <= u1 <= 0.6)
            self.assertTrue(0.4 <= u2 <= 0.6)


if __name__ == "__main__":
    unittest.main()
