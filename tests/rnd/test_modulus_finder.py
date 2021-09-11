import unittest
from core.rnd.inspection import modulus_finder


class ModulusTest(unittest.TestCase):
    def test_find_jumper_8bit(self):
        """
        Verify the correctness of the modulus finder process, for 8bit modulus.
        :return: None
        """
        BITS = 8
        MODULUS = 127

        modulus = modulus_finder.find_modulus(BITS)

        self.assertEqual(MODULUS, modulus, "Modulus (8 bit) not correct.")

    def test_find_jumper_16bit(self):
        """
        Verify the correctness of the modulus finder process, for 16bit modulus.
        :return: None
        """
        BITS = 16
        MODULUS = 32749

        modulus = modulus_finder.find_modulus(BITS)

        self.assertEqual(MODULUS, modulus, "Modulus (16 bit) not correct.")

    def test_find_jumper_32bit(self):
        """
        Verify the correctness of the modulus finder process, for 32bit modulus.
        :return: None
        """
        BITS = 32
        MODULUS = 2147483647

        modulus = modulus_finder.find_modulus(BITS)

        self.assertEqual(MODULUS, modulus, "Modulus (32 bit) not correct.")

    @unittest.skip("Test too expensive for this machine.")
    def test_find_jumper_64bit(self):
        """
        Verify the correctness of the modulus finder process, for 64bit modulus.
        :return: None
        """
        BITS = 64
        MODULUS = 9223372036854775783

        modulus = modulus_finder.find_modulus(BITS)

        self.assertEqual(MODULUS, modulus, "Modulus (64 bit) not correct.")


if __name__ == "__main__":
    unittest.main()
