"""
Test suite to run all demule unit tests at once.
"""

import os
import sys

sys.path.append(os.path.abspath('.'))

import unittest
from tests import modulus_finder
from tests import jumper_finder
from tests import multiplier_finder


def buildSuite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(modulus_finder.ModulusTest(), 'test'))
    return suite


if __name__ == '__main__':
    suite = buildSuite()
    runner = unittest.TextTestRunner()
    runner.run(suite)