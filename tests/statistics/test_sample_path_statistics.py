import unittest
from core.stats.sample_path_statistics import SimpleSamplePathStatistic
from core.random.rndgen import MarcianiMultiStream as RandomGenerator
from core.random.rndvar import uniform, equilikely, exponential, geometric
from math import sqrt


class SamplePathStatistics(unittest.TestCase):

    def test_mean_sdev(self):
        """
        Test the calculation of mean and standard deviation.
        :return: None
        """
        rndgen = RandomGenerator()

        n = 1000000

        err = 0.02

        # Creation
        stats = SimpleSamplePathStatistic()

        # Uniform
        a = 0
        b = 1
        for i in range(1, n):
            stats.add_value(uniform(a, b, rndgen.rnd()), i)

        th_mean = (a + b) / 2
        th_sdev = (b - a) / sqrt(12)
        self.assertLessEqual(abs(th_mean - stats.mean()) / th_mean, err * th_mean)
        self.assertLessEqual(abs(th_sdev - stats.sdev()) / th_sdev, err * th_sdev)

        stats.reset()

        # Equilikely
        a = 0
        b = 1
        for i in range(1, n):
            stats.add_value(equilikely(a, b, rndgen.rnd()), i)

        th_mean = (a + b) / 2
        th_sdev = sqrt((pow(b - a + 1, 2) - 1) / 12)
        self.assertLessEqual(abs(th_mean - stats.mean()) / th_mean, err * th_mean)
        self.assertLessEqual(abs(th_sdev - stats.sdev()) / th_sdev, err * th_sdev)

        stats.reset()

        # Exponential
        m = 1 / 0.35
        for i in range(1, n):
            stats.add_value(exponential(m, rndgen.rnd()), i)

        th_mean = m
        th_sdev = m
        self.assertLessEqual(abs(th_mean - stats.mean()) / th_mean, err * th_mean)
        self.assertLessEqual(abs(th_sdev - stats.sdev()) / th_sdev, err * th_sdev)

    def test_throughput(self):
        """
        Check the calculation of throughput.
        :return:
        """
        rndgen = RandomGenerator()

        n = 1000000

        t_clock = 0.0
        n_served_1 = 0
        n_served_2 = 0

        throughput_path = SimpleSamplePathStatistic()
        for i in range(n):
            t_clock += rndgen.rnd()
            if rndgen.rnd() < 0.5:
                n_served_1 += 1
                throughput_path.add_value(n_served_1, t_clock)
            else:
                n_served_2 += 1
                throughput_path.add_value(n_served_2, t_clock)

        throughput_raw = (n_served_1 + n_served_2) / t_clock

        print("throughput (raw):", throughput_raw)
        print("throughput (path):", throughput_path.mean())
