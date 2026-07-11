import os
import tempfile
import unittest

from pydes.exp.rnd import mulfind


class MulfindRunTest(unittest.TestCase):
    def setUp(self):
        """
        The test setup.
        :return: None
        """
        self.outdir = tempfile.mkdtemp()
        self.modulus = 31

    def test_run(self):
        """
        Verify that run() computes FP, MC and FP/MC multipliers for a small modulus and
        stores the raw lists and the report.
        :return: None
        """
        mulfind.run(self.modulus, self.outdir)

        base = os.path.join(self.outdir, "mod{}".format(self.modulus))

        for suffix in ("_mc.txt", "_fp.txt", "_fpmc.txt", "_report.txt"):
            filename = base + suffix
            self.assertTrue(os.path.isfile(filename), "Missing expected output file {}".format(filename))

        with open(base + "_fpmc.txt") as f:
            fpmc_content = f.read().split()

        self.assertEqual(["3"], fpmc_content)

        with open(base + "_report.txt") as f:
            report_content = f.read()

        self.assertIn("MULTIPLIERS", report_content)
        self.assertIn("Smallest FP/MC Multiplier", report_content)
        self.assertIn("Largest FP/MC Multiplier", report_content)


if __name__ == "__main__":
    unittest.main()
