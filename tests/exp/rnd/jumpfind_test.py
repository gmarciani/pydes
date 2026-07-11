import os
import tempfile
import unittest

from pydes.exp.rnd import jumpfind


class JumpfindRunTest(unittest.TestCase):
    def setUp(self):
        """
        The test setup.
        :return: None
        """
        self.outdir = tempfile.mkdtemp()
        self.modulus = 127
        self.multiplier = 3
        self.streams = 8

    def test_run(self):
        """
        Verify that run() finds the modulus-compatible jumpers for a small modulus/multiplier
        pair and stores both the raw pairs and the summary report.
        :return: None
        """
        jumpfind.run(self.modulus, self.multiplier, self.streams, self.outdir)

        base = os.path.join(self.outdir, "mod{}_mul{}_str{}".format(self.modulus, self.multiplier, self.streams))

        self.assertTrue(os.path.isfile(base + ".csv"))
        self.assertTrue(os.path.isfile(base + "_report.txt"))

        with open(base + ".csv") as f:
            rows = f.read().strip().splitlines()

        # At least one jumper found for this small modulus/multiplier pair.
        self.assertGreaterEqual(len(rows), 1)

        with open(base + "_report.txt") as f:
            report_content = f.read()

        self.assertIn("JUMPER", report_content)
        self.assertIn("Best Jumper", report_content)
        self.assertIn("Best Jump Size", report_content)


if __name__ == "__main__":
    unittest.main()
