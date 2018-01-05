import unittest
from core.random.inspection import multiplier_finder


class MultiplierTest(unittest.TestCase):

    def test_find_multiplier_8bit(self):
        MODULUS = 127
        MULTIPLIER = 3

        multiplier = multiplier_finder.find_multiplier(MODULUS)

        self.assertEqual(multiplier, MULTIPLIER, 'Multiplier (8 bit) not correct.')

    @unittest.skip('Test too expensive for this machine.')
    def test_find_multiplier_16bit(self):
        MODULUS = 32479
        MULTIPLIER = 16374

        multiplier = multiplier_finder.find_multiplier(MODULUS)

        self.assertEqual(multiplier, MULTIPLIER, 'Multiplier (16 bit) not correct.')

    @unittest.skip('Test too expensive for this machine.')
    def test_find_multiplier_32bit(self):
        MODULUS = 2147483647
        MULTIPLIER = 48271

        multiplier = multiplier_finder.find_multiplier(MODULUS)

        self.assertEqual(multiplier, MULTIPLIER, 'Multiplier (32 bit) not correct.')

    @unittest.skip('Test too expensive for this machine.')
    def test_find_multiplier_64bit(self):
        MODULUS = 2147483647    # 9223372036854775783
        MULTIPLIER = 48271      # -

        multiplier = multiplier_finder.find_multiplier(MODULUS)

        self.assertEqual(multiplier, MULTIPLIER, 'Multiplier (64 bit) not correct.')


if __name__ == '__main__':
    unittest.main()


