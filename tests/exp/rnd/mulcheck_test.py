import os
import tempfile
import unittest

from pydes.exp.rnd import mulcheck


class MulcheckRunTest(unittest.TestCase):
    def setUp(self):
        """
        The test setup.
        :return: None
        """
        self.outdir = tempfile.mkdtemp()

    def test_run_fpmc_multiplier(self):
        """
        Verify that run() correctly reports a multiplier that is both FP and MC.
        :return: None
        """
        modulus = 31
        multiplier = 3

        mulcheck.run(modulus, multiplier, self.outdir)

        filename = os.path.join(self.outdir, "mod{}_mul{}_report.txt".format(modulus, multiplier))
        self.assertTrue(os.path.isfile(filename))

        with open(filename) as f:
            content = f.read()

        self.assertIn("MULTIPLIER CHECK", content)
        self.assertIn("FP", content)
        self.assertIn("MC", content)

    def test_run_non_fpmc_multiplier(self):
        """
        Verify that run() correctly reports a multiplier that is not FP/MC.
        :return: None
        """
        modulus = 31
        multiplier = 2

        mulcheck.run(modulus, multiplier, self.outdir)

        filename = os.path.join(self.outdir, "mod{}_mul{}_report.txt".format(modulus, multiplier))
        self.assertTrue(os.path.isfile(filename))


if __name__ == "__main__":
    unittest.main()
