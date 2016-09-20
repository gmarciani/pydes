"""
Test suite to run all demule unit tests at once.
"""

import unittest
from tests.unit import modulus_finder
from tests.unit import multiplier_finder
from tests.unit import jumper_finder


def main():
    suite = unittest.TestSuite()
    suite.addTest(modulus_finder.ModulusTest())
    suite.addTest(multiplier_finder.MultiplierTest())
    suite.addTest(jumper_finder.JumperTest())
    return suite


if __name__ == '__main__':
    main()