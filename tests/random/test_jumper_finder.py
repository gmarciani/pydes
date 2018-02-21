import unittest
from core.random.inspection import jumper_finder


class JumperTest(unittest.TestCase):

    @unittest.skip("Test too expensive for this machine.")
    def test_find_jumper_8bit(self):
        """
        Verify the correctness of the jumper finder process, for 8bit modulus.
        :return: None
        """
        MODULUS = 127
        MULTIPLIER = 3
        STREAMS = 64
        JUMPER = 3
        JSIZE = 127

        jumper, jsize = jumper_finder.find_jumpers(MODULUS, MULTIPLIER, STREAMS)

        self.assertEqual(jumper, JUMPER, "Jumper (8 bit) not correct.")
        self.assertEqual(jsize, JSIZE, "Jump Size (8 bit) not correct.")

    @unittest.skip("Test too expensive for this machine.")
    def test_find_jumper_16bit(self):
        """
        Verify the correctness of the jumper finder process, for 16bit modulus.
        :return: None
        """
        MODULUS = 32479
        MULTIPLIER = 16374
        STREAMS = 128
        JUMPER = 32748
        JSIZE = 127

        jumper, jsize = jumper_finder.find_jumpers(MODULUS, MULTIPLIER, STREAMS)

        self.assertEqual(jumper, JUMPER, "Jumper (16 bit) not correct.")
        self.assertEqual(jsize, JSIZE, "Jump size (16 bit) not correct.")

    @unittest.skip("Test too expensive for this machine.")
    def test_find_jumper_32bit(self):
        """
        Verify the correctness of the jumper finder process, for 32bit modulus.
        :return: None
        """
        MODULUS = 2147483647
        MULTIPLIER = 48271
        STREAMS = 256
        JUMPER = 22925
        JSIZE = 127

        jumper, jsize = jumper_finder.find_jumpers(MODULUS, MULTIPLIER, STREAMS)

        self.assertEqual(jumper, JUMPER, "Jumper (32 bit) not correct.")
        self.assertEqual(jsize, JSIZE, "Jump size (32 bit) not correct.")

    @unittest.skip("Test too expensive for this machine.")
    def test_find_jumper_64bit(self):
        """
        Verify the correctness of the jumper finder process, for 64bit modulus.
        :return: None
        """
        MODULUS = 2147483647    # 9223372036854775783
        MULTIPLIER = 48271      # -
        STREAMS = 256
        JUMPER = 22925
        JSIZE = 127

        jumper, jsize = jumper_finder.find_jumpers(MODULUS, MULTIPLIER, STREAMS)

        self.assertEqual(jumper, JUMPER, "Jumper (64 bit) not correct.")
        self.assertEqual(jsize, JSIZE, "Jump size (64 bit) not correct.")


if __name__ == "__main__":
    unittest.main()