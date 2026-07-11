import unittest

from pydes.core.metrics.confidence_interval import get_interval_estimation
from pydes.core.rnd.rndf import idfStudent


class ConfidenceIntervalTest(unittest.TestCase):
    def test_samsize_greater_than_one(self):
        samsize = 10
        sdev = 2.0
        alpha = 0.05

        expected = idfStudent(samsize - 1, 1.0 - (alpha / 2)) * sdev / (samsize - 1) ** 0.5
        actual = get_interval_estimation(samsize, sdev, alpha)

        self.assertAlmostEqual(expected, actual, 10)

    def test_samsize_equal_to_one_returns_zero(self):
        self.assertEqual(0.0, get_interval_estimation(1, 2.0, 0.05))

    def test_samsize_less_than_one_returns_zero(self):
        self.assertEqual(0.0, get_interval_estimation(0, 2.0, 0.05))


if __name__ == "__main__":
    unittest.main()
