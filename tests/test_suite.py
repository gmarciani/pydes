"""
Test suite to run all demule unit tests at once.
"""

import unittest

import modulus_finder
from tests import jumper_finder
from tests import multiplier_finder


def main():
    suite = unittest.TestSuite()
    suite.addTest(modulus_finder.ModulusTest())
    suite.addTest(multiplier_finder.MultiplierTest())
    suite.addTest(jumper_finder.JumperTest())
    return suite


if __name__ == '__main__':
    main()