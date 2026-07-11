import unittest

from pydes.core.rnd.randomness import kolmogorov_smirnov as ks


class KolmogorovSmirnovTest(unittest.TestCase):
    def setUp(self):
        self.bins = 10
        self.chisquares = [(0, 5.0), (1, 3.0), (2, 8.0), (3, 1.0)]

    def test_compute_ks_distances_returns_one_per_stream(self):
        distances = ks.compute_ks_distances(list(self.chisquares), self.bins)

        self.assertEqual(len(distances), len(self.chisquares))
        for chi, distance in distances:
            self.assertGreaterEqual(distance, 0.0)

    def test_compute_ks_distances_sorts_by_chisquare(self):
        distances = ks.compute_ks_distances(list(self.chisquares), self.bins)

        chis = [chi for chi, _ in distances]
        self.assertEqual(chis, sorted(chis))

    def test_compute_ks_statistic_is_the_maximum_distance(self):
        distances = ks.compute_ks_distances(list(self.chisquares), self.bins)

        statistic = ks.compute_ks_statistic(distances)

        self.assertEqual(statistic, max(distance for _, distance in distances))

    def test_compute_ks_point_is_chisquare_of_max_distance(self):
        distances = ks.compute_ks_distances(list(self.chisquares), self.bins)

        point = ks.compute_ks_point(distances)

        expected_chi = max(distances, key=lambda value: value[1])[0]
        self.assertEqual(point, expected_chi)

    def test_compute_ks_critical_distance_known_confidences(self):
        n = len(self.chisquares)
        for confidence in (0.90, 0.95, 0.975, 0.99):
            critical = ks.compute_ks_critical_distance(n, confidence)
            self.assertGreater(critical, 0.0)

    def test_compute_ks_critical_distance_raises_for_unknown_confidence(self):
        with self.assertRaises(KeyError):
            ks.compute_ks_critical_distance(len(self.chisquares), 0.5)


if __name__ == "__main__":
    unittest.main()
