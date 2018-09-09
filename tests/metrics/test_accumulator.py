import unittest
from core.metrics.accumulator import WelfordAccumulator
from random import randint
from statistics import mean, variance, stdev


class AccumulatorTest(unittest.TestCase):

    def test_mean_sdev_int_array(self):
        """
        Test the calculation of mean and standard deviation, using an array of random integer values.
        :return: None
        """

        n = 100000

        precision = 5

        err = 0.02

        # Creation

        accumulator = WelfordAccumulator()

        # Values
        values = []
        for _ in range(n):
            value = randint(1, 1000)
            values.append(value)
            accumulator.add_value(value)

        expected_mean = mean(values)
        expected_var = variance(values)
        expected_sdev = stdev(values)

        self.assertEqual(round(expected_mean, precision), round(accumulator.mean(), precision))
        self.assertLessEqual(abs(expected_var - accumulator.var()) / expected_var, err * expected_var)
        self.assertLessEqual(abs(expected_sdev - accumulator.sdev()) / expected_sdev, err * expected_sdev)