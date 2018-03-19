import unittest
from core.stats.sample_statistics import SimpleSampleStatistic
from core.random.rndgen import MarcianiMultiStream as RandomGenerator
from core.random.rndvar import uniform, equilikely, exponential, geometric
from math import sqrt


class SampleStatistics(unittest.TestCase):

    def test_mean_sdev(self):
        """
        Test the calculation of mean and standard deviation.
        :return: None
        """
        rndgen = RandomGenerator()

        n = 1000000

        err = 0.02

        # Creation
        stats = SimpleSampleStatistic()

        # Uniform
        a = 0
        b = 1
        for i in range(n):
            stats.add_value(uniform(a, b, rndgen.rnd()))

        th_mean = (a + b) / 2
        th_sdev = (b - a) / sqrt(12)
        self.assertLessEqual(abs(th_mean - stats.mean()) / th_mean, err * th_mean)
        self.assertLessEqual(abs(th_sdev - stats.sdev()) / th_sdev, err * th_sdev)

        stats.reset()

        # Equilikely
        a = 0
        b = 1
        for i in range(n):
            stats.add_value(equilikely(a, b, rndgen.rnd()))

        th_mean = (a + b) / 2
        th_sdev = sqrt((pow(b - a + 1, 2) - 1) / 12)
        self.assertLessEqual(abs(th_mean - stats.mean()) / th_mean, err * th_mean)
        self.assertLessEqual(abs(th_sdev - stats.sdev()) / th_sdev, err * th_sdev)

        stats.reset()

        # Exponential
        m = 1. / 0.35
        for i in range(n):
            stats.add_value(exponential(m, rndgen.rnd()))

        th_mean = m
        th_sdev = m
        self.assertLessEqual(abs(th_mean - stats.mean()) / th_mean, err * th_mean)
        self.assertLessEqual(abs(th_sdev - stats.sdev()) / th_sdev, err * th_sdev)