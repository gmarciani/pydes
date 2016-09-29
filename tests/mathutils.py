import unittest
from demule.utils import mathutils
from demule.utils import rvms


class MathUtilsTest(unittest.TestCase):

    def test_student(self):
        self.assertAlmostEqual(rvms.idfStudent(9, 0.95), 1.833, 3)
        self.assertAlmostEqual(rvms.idfStudent(9, 0.975), 2.262, 3)
        self.assertAlmostEqual(rvms.idfStudent(9, 0.995), 3.250, 3)

    def test_mean(self):
        sample = [1.051, 6.438, 2.646, 0.805, 1.505,
                  0.546, 2.281, 2.822, 0.414, 1.307]
        m = mathutils.mean(sample)
        self.assertAlmostEqual(m, 1.982, 3, 'mean is not correct')

    def test_standard_deviation(self):
        sample = [1.051, 6.438, 2.646, 0.805, 1.505,
                  0.546, 2.281, 2.822, 0.414, 1.307]
        s = mathutils.standard_deviation(sample)
        self.assertAlmostEqual(s, 1.690, 3, 'standard deviation is not correct.')

    def test_interval_estimation(self):
        sample = [1.051, 6.438, 2.646, 0.805, 1.505,
                  0.546, 2.281, 2.822, 0.414, 1.307]
        significance = 0.05
        lb, m, ub = mathutils.interval_estimation(sample, significance)
        self.assertAlmostEqual(lb, 1.982 - 1.274, 2, 'lower bound not correct.')
        self.assertAlmostEqual(ub, 1.982 + 1.274, 2, 'upper bound not correct.')
        self.assertAlmostEqual(m, 1.982, 2, 'mean not correct.')

    def test_welford(self):
        stats = mathutils.WelfordStatistics()
        sample = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        for i in range(len(sample)):
            value = sample[i]
            stats.update(value)
            mean = mathutils.mean(sample[:i + 1])
            variance = mathutils.variance(sample[:i + 1])
            self.assertAlmostEqual(stats.get_mean(), mean, 2,
                                   'mean not correct.')
            self.assertAlmostEqual(stats.get_variance(), variance, 2, 'variance not correct.')


if __name__ == '__main__':
    unittest.main()