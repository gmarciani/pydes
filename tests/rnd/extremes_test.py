import unittest

from pydes.core.rnd.randomness import extremes
from pydes.core.rnd.rndgen import MarcianiMultiStream


class ExtremesTest(unittest.TestCase):
    def setUp(self):
        self.samsize = 200
        self.bins = 10
        self.d = 3

    def test_observations_produces_expected_totals(self):
        generator = MarcianiMultiStream(streams=4)

        observed = extremes.observations(generator, self.samsize, self.bins, self.d)

        self.assertEqual(len(observed), self.bins)
        self.assertEqual(sum(observed), self.samsize)
        for count in observed:
            self.assertGreaterEqual(count, 0)

    def test_compute_chisquare_statistic_zero_for_uniform_observed(self):
        observed = [self.samsize // self.bins] * self.bins

        chi = extremes._compute_chisquare_statistic(observed, self.samsize)

        self.assertAlmostEqual(chi, 0.0, places=6)

    def test_compute_chisquare_statistic_positive_for_skewed_observed(self):
        observed = [0] * (self.bins - 1) + [self.samsize]

        chi = extremes._compute_chisquare_statistic(observed, self.samsize)

        self.assertGreater(chi, 0.0)

    def test_critical_min_max(self):
        mn = extremes.critical_min(self.bins, 0.95)
        mx = extremes.critical_max(self.bins, 0.95)

        self.assertLess(mn, mx)

    def test_statistics_returns_one_result_per_stream(self):
        streams = 8
        generator = MarcianiMultiStream(streams=streams)

        data = extremes.statistics(generator, samsize=50, bins=self.bins, d=self.d)

        self.assertEqual(len(data), streams)
        for stream, chi in data:
            self.assertIn(stream, range(streams))
            self.assertGreaterEqual(chi, 0.0)

    def test_error_reports_theoretical_and_empirical_errors(self):
        streams = 32
        generator = MarcianiMultiStream(streams=streams)
        data = extremes.statistics(generator, samsize=50, bins=self.bins, d=self.d)
        mn = extremes.critical_min(self.bins, 0.95)
        mx = extremes.critical_max(self.bins, 0.95)

        error = extremes.error(data, mn, mx, 0.95)

        self.assertIn("err_thr", error)
        self.assertIn("err_emp", error)
        self.assertEqual(error["err_emp"], error["err_mn"] + error["err_mx"])


if __name__ == "__main__":
    unittest.main()
