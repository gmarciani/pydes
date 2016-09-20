import unittest
from demule.rnd.inspection import modulus_finder


class ModulusTest(unittest.TestCase):

    def test_find_jumper_8bit(self):
        BITS = 8
        MODULUS = 127

        modulus = modulus_finder.find_modulus(BITS)

        self.assertEqual(modulus, MODULUS, 'Modulus (8 bit) not correct.')

    def test_find_jumper_16bit(self):
        BITS = 16
        MODULUS = 32479

        modulus = modulus_finder.find_modulus(BITS)

        self.assertEqual(modulus, MODULUS, 'Modulus (16 bit) not correct.')

    @unittest.skip('Test too expensive for this machine.')
    def test_find_jumper_32bit(self):
        BITS = 32
        MODULUS = 2147483647

        modulus = modulus_finder.find_modulus(BITS)

        self.assertEqual(modulus, MODULUS, 'Modulus (32 bit) not correct.')

    @unittest.skip('Test too expensive for this machine.')
    def test_find_jumper_64bit(self):
        BITS = 64
        MODULUS = 9223372036854775783

        modulus = modulus_finder.find_modulus(BITS)

        self.assertEqual(modulus, MODULUS, 'Modulus (64 bit) not correct.')


if __name__ == '__main__':
    unittest.main()
