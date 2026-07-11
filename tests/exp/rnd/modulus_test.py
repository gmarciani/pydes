import os
import tempfile
import unittest

from pydes.exp.rnd import modulus


class ModulusRunTest(unittest.TestCase):
    def setUp(self):
        """
        The test setup.
        :return: None
        """
        self.outdir = tempfile.mkdtemp()

    def test_run_default_outdir(self):
        """
        Verify that run() finds the expected modulus for a small number of bits and
        stores the result under the default output directory naming convention.
        :return: None
        """
        modulus.run(8, self.outdir)

        filename = os.path.join(self.outdir, "mod8.txt")
        self.assertTrue(os.path.isfile(filename))

        with open(filename) as f:
            content = f.read()

        self.assertIn("MODULUS", content)
        self.assertIn("127", content)

    def test_run_uses_default_outdir_argument(self):
        """
        Verify that run() accepts the outdir as a positional/keyword argument and that the
        found modulus is the largest prime representable with the given number of bits.
        :return: None
        """
        modulus.run(bits=4, outdir=self.outdir)

        filename = os.path.join(self.outdir, "mod4.txt")
        self.assertTrue(os.path.isfile(filename))
        with open(filename) as f:
            content = f.read()
        self.assertIn("7", content)


if __name__ == "__main__":
    unittest.main()
