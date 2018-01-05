"""
Test suite to run all demule unit tests at once.
"""

import os
import sys

sys.path.append(os.path.abspath('.'))

import unittest
from tests import mathutils
from tests import rndgen
from tests import modulus_finder
from tests import jumper_finder
from tests import multiplier_finder
from tests import simulation_cloud


def suite():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTest(loader.loadTestsFromModule(mathutils))
    suite.addTest(loader.loadTestsFromModule(rndgen))
    suite.addTest(loader.loadTestsFromModule(modulus_finder))
    suite.addTest(loader.loadTestsFromModule(multiplier_finder))
    suite.addTest(loader.loadTestsFromModule(jumper_finder))
    suite.addTest(loader.loadTestsFromModule(simulation_cloud))

    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=3)
    result = runner.run(suite())