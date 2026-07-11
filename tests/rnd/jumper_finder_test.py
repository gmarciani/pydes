import unittest

from pydes.core.rnd.inspection import jumper_finder


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
        MODULUS = 2147483647  # 9223372036854775783
        MULTIPLIER = 48271  # -
        STREAMS = 256
        JUMPER = 22925
        JSIZE = 127

        jumper, jsize = jumper_finder.find_jumpers(MODULUS, MULTIPLIER, STREAMS)

        self.assertEqual(jumper, JUMPER, "Jumper (64 bit) not correct.")
        self.assertEqual(jsize, JSIZE, "Jump size (64 bit) not correct.")

    def test_find_jumpers_tiny_modulus(self):
        """
        Verify find_jumpers with a tiny modulus so the search completes instantly.
        """
        MODULUS = 31
        MULTIPLIER = 3
        STREAMS = 4

        jumpers = jumper_finder.find_jumpers(MODULUS, MULTIPLIER, STREAMS)

        self.assertTrue(len(jumpers) > 0)
        for jumper, jsize in jumpers:
            self.assertTrue(0 < jumper < MODULUS)
            self.assertTrue(1 <= jsize <= int((MODULUS + 1) / STREAMS))

    def test_find_jumper_tiny_modulus(self):
        """
        Verify find_jumper with a tiny modulus returns the first suitable jumper.
        """
        MODULUS = 31
        MULTIPLIER = 3
        STREAMS = 4

        jumper, jsize = jumper_finder.find_jumper(MODULUS, MULTIPLIER, STREAMS)

        jumpers = jumper_finder.find_jumpers(MODULUS, MULTIPLIER, STREAMS)
        self.assertEqual((jumper, jsize), jumpers[0])

    def test_find_jumper_returns_none_when_search_space_is_empty(self):
        """
        When streams is larger than modulus + 1, the search range is empty
        and find_jumper must return None.
        """
        MODULUS = 31
        MULTIPLIER = 3
        STREAMS = 100

        self.assertIsNone(jumper_finder.find_jumper(MODULUS, MULTIPLIER, STREAMS))
        self.assertEqual(jumper_finder.find_jumpers(MODULUS, MULTIPLIER, STREAMS), [])


if __name__ == "__main__":
    unittest.main()
