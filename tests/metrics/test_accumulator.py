import unittest
from core.metrics.accumulator import WelfordAccumulator
from random import randint
import numpy as np
import scipy.stats
from math import sqrt

SAMPLE_SIZE = 1000000
PRECISION = 10
ERROR = 0.000015
CONFIDENCE = 0.95


class AccumulatorTest(unittest.TestCase):
    def setUp(self):
        self.accumulator = WelfordAccumulator()
        self.values = []
        for _ in range(SAMPLE_SIZE):
            value = randint(1, 1000)
            self.values.append(value)
            self.accumulator.add_value(value)

    def test_mean(self):
        expected_mean = np.mean(self.values)
        actual_mean = self.accumulator.mean()
        print("expected_mean:", expected_mean)
        print("actual_mean:", actual_mean)
        self.assertEqual(round(expected_mean, PRECISION), round(actual_mean, PRECISION))

    def test_var(self):
        expected_var = np.var(self.values)
        actual_var = self.accumulator.var()
        print("expected_var:", expected_var)
        print("actual_var:", actual_var)
        self.assertLessEqual(abs(expected_var - actual_var) / expected_var, ERROR)

    def test_sdev(self):
        expected_sdev = sqrt(np.var(self.values))
        actual_sdev = self.accumulator.sdev()
        print("expected_sdev:", expected_sdev)
        print("actual_sdev:", actual_sdev)
        self.assertLessEqual(abs(expected_sdev - actual_sdev) / expected_sdev, ERROR)

    def test_cint(self):
        expected_cint = scipy.stats.sem(self.values) * scipy.stats.t.ppf((1 + CONFIDENCE) / 2.0, len(self.values) - 1)
        actual_cint = self.accumulator.cint(1 - CONFIDENCE)
        print("expected_cint:", expected_cint)
        print("actual_cint:", actual_cint)
        self.assertLessEqual(abs(expected_cint - actual_cint) / expected_cint, ERROR)
