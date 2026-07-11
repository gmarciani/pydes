import unittest

from pydes.core.rnd import rndf
from pydes.core.utils import mathutils


class MathUtilsTest(unittest.TestCase):
    def test_gcd(self):
        self.assertEqual(6, mathutils.gcd(48, 18))
        self.assertEqual(1, mathutils.gcd(7, 13))
        self.assertEqual(5, mathutils.gcd(0, 5))

    def test_is_prime(self):
        self.assertTrue(mathutils.is_prime(2))
        self.assertFalse(mathutils.is_prime(4))
        self.assertTrue(mathutils.is_prime(7))
        self.assertFalse(mathutils.is_prime(9))
        self.assertTrue(mathutils.is_prime(29))

    def test_are_coprime(self):
        self.assertTrue(mathutils.are_coprime(8, 15))
        self.assertFalse(mathutils.are_coprime(8, 4))

    def test_get_frequencies(self):
        sample = [0.5, 1.5, 2.5, 3.5]
        frequencies = mathutils.get_frequencies(sample, min=0, max=4, bins=4)
        self.assertEqual([1, 1, 1, 1], frequencies)

    def test_get_frequencies_bivariate(self):
        sample = [(0.5, 0.5), (1.5, 1.5), (2.5, 2.5), (3.5, 3.5)]
        frequencies = mathutils.get_frequencies_bivariate(sample, mn=0, mx=4, bins=4)
        self.assertEqual(
            [
                [1, 0, 0, 0],
                [0, 1, 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1],
            ],
            frequencies,
        )

    def test_chisquare_univariate(self):
        observed = [10, 20, 30]
        expected_values = [12, 18, 32]

        def expected(x):
            return expected_values[x]

        value = mathutils.chisquare_univariate(observed, expected)
        self.assertAlmostEqual(4 / 12 + 4 / 18 + 4 / 32, value, 6)

    def test_chisquare_bivariate(self):
        observed = [[10, 20], [30, 40]]
        expected_values = [[12, 18], [28, 42]]

        def expected(x1, x2):
            return expected_values[x1][x2]

        value = mathutils.chisquare_bivariate(observed, expected)
        self.assertAlmostEqual(4 / 12 + 4 / 18 + 4 / 28 + 4 / 42, value, 6)

    def test_covariance(self):
        sample = [(1, 2), (2, 4), (3, 6)]
        c = mathutils.covariance(sample)
        self.assertAlmostEqual(4 / 3, c, 6)

    def test_correlation_coefficient(self):
        sample = [(1, 2), (2, 4), (3, 6)]
        r = mathutils.correlation_coefficient(sample)
        self.assertAlmostEqual(1.0, r, 6)

    def test_linear_regression_line(self):
        sample = [(1, 2), (2, 4), (3, 6)]
        line = mathutils.linear_regression_line(sample)
        self.assertAlmostEqual(2.0, line(1), 4)
        self.assertAlmostEqual(4.0, line(2), 4)
        self.assertAlmostEqual(6.0, line(3), 4)

    def test_g_positive_branch(self):
        value = mathutils._g(1, 6, 13)
        self.assertEqual(6, value)

    def test_g_non_positive_branch(self):
        value = mathutils._g(2, 6, 13)
        self.assertEqual(12, value)

    def test_student(self):
        self.assertAlmostEqual(rndf.idfStudent(9, 0.95), 1.833, 3)
        self.assertAlmostEqual(rndf.idfStudent(9, 0.975), 2.262, 3)
        self.assertAlmostEqual(rndf.idfStudent(9, 0.995), 3.250, 3)

    def test_mean(self):
        sample = [1.051, 6.438, 2.646, 0.805, 1.505, 0.546, 2.281, 2.822, 0.414, 1.307]
        m = mathutils.mean(sample)
        self.assertAlmostEqual(m, 1.982, 3, "mean is not correct")

    def test_standard_deviation(self):
        sample = [1.051, 6.438, 2.646, 0.805, 1.505, 0.546, 2.281, 2.822, 0.414, 1.307]
        s = mathutils.standard_deviation(sample)
        self.assertAlmostEqual(s, 1.690, 3, "standard deviation is not correct.")

    def test_interval_estimation(self):
        sample = [1.051, 6.438, 2.646, 0.805, 1.505, 0.546, 2.281, 2.822, 0.414, 1.307]
        significance = 0.05
        lb, m, ub = mathutils.interval_estimation(sample, significance)
        self.assertAlmostEqual(lb, 1.982 - 1.274, 2, "lower bound not correct.")
        self.assertAlmostEqual(ub, 1.982 + 1.274, 2, "upper bound not correct.")
        self.assertAlmostEqual(m, 1.982, 2, "mean not correct.")

    def test_welford(self):
        stats = mathutils.WelfordStatistics()
        sample = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        for i in range(len(sample)):
            value = sample[i]
            stats.update(value)
            mean = mathutils.mean(sample[: i + 1])
            variance = mathutils.variance(sample[: i + 1])
            self.assertAlmostEqual(stats.get_mean(), mean, 2, "mean not correct.")
            self.assertAlmostEqual(stats.get_variance(), variance, 2, "variance not correct.")


if __name__ == "__main__":
    unittest.main()
