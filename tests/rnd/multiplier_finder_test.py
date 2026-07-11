import unittest

from pydes.core.rnd.inspection import multiplier_finder
from pydes.core.rnd.inspection.multiplier_check import is_fp_multiplier, is_mc_multiplier


class MultiplierTest(unittest.TestCase):
    @unittest.skip("Test too expensive for this machine.")
    def test_find_multiplier_8bit(self):
        """
        Verify the correctness of the multiplier finder process, for 8bit modulus.
        :return: None
        """
        MODULUS = 127
        MULTIPLIER = 3

        multiplier = multiplier_finder.find_multiplier(MODULUS)

        self.assertEqual(MULTIPLIER, multiplier, "Multiplier (8 bit) not correct.")

    @unittest.skip("Test too expensive for this machine.")
    def test_find_multiplier_16bit(self):
        """
        Verify the correctness of the multiplier finder process, for 16bit modulus.
        :return: None
        """
        MODULUS = 32749
        MULTIPLIER = 16374

        multiplier = multiplier_finder.find_multiplier(MODULUS)

        self.assertEqual(MULTIPLIER, multiplier, "Multiplier (16 bit) not correct.")

    @unittest.skip("Test too expensive for this machine.")
    def test_find_multiplier_32bit(self):
        """
        Verify the correctness of the multiplier finder process, for 32bit modulus.
        :return: None
        """
        MODULUS = 2147483647
        MULTIPLIER = 48271

        multiplier = multiplier_finder.find_multiplier(MODULUS)

        self.assertEqual(MULTIPLIER, multiplier, "Multiplier (32 bit) not correct.")

    @unittest.skip("Test too expensive for this machine.")
    def test_find_multiplier_64bit(self):
        """
        Verify the correctness of the multiplier finder process, for 64bit modulus.
        :return: None
        """
        MODULUS = 2147483647  # 9223372036854775783
        MULTIPLIER = 48271  # -

        multiplier = multiplier_finder.find_multiplier(MODULUS)

        self.assertEqual(MULTIPLIER, multiplier, "Multiplier (64 bit) not correct.")

    def test_find_multiplier_tiny_modulus(self):
        """
        Exercise the actual brute-force search logic with a tiny modulus so it
        completes near-instantly, instead of skipping it like the 8/16/32/64
        bit cases above.
        """
        MODULUS = 31
        MULTIPLIER = 3

        multiplier = multiplier_finder.find_multiplier(MODULUS)

        self.assertEqual(MULTIPLIER, multiplier, "Multiplier (tiny modulus) not correct.")
        self.assertTrue(is_fp_multiplier(multiplier, MODULUS))
        self.assertTrue(is_mc_multiplier(multiplier, MODULUS))

    def test_find_multiplier_tiny_modulus_few_threads(self):
        """
        Same as above, but with a small thread pool to exercise the loop
        that distributes the search range over fewer worker threads.
        """
        MODULUS = 127
        MULTIPLIER = 3

        multiplier = multiplier_finder.find_multiplier(MODULUS, threads=2)

        self.assertEqual(MULTIPLIER, multiplier, "Multiplier (tiny modulus, few threads) not correct.")


if __name__ == "__main__":
    unittest.main()
