import unittest
import tests.randomness.uniformity_univariate
import tests.randomness.extremes
import tests.randomness.runsup
import tests.randomness.gap
import tests.randomness.uniformity_bivariate
import tests.randomness.permutation


class RandomnessTests(unittest.TestCase):

    def test_uniformity_univariate(self):
        tests.randomness.uniformity_univariate.test()

    def test_extremes(self):
        tests.randomness.extremes.test()

    def test_runsup(self):
        tests.randomness.runsup.test()

    def test_gap(self):
        tests.randomness.gap.test()

    def test_uniformity_bivariate(self):
        tests.randomness.uniformity_bivariate.test()

    def test_permutation(self):
        tests.randomness.permutation.test()