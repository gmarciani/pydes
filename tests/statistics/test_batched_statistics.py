import unittest
from core.stats.batch_means import BatchedMeasure


class BatchedStatistics(unittest.TestCase):

    def test_simple(self):
        """
        Test the calculation of mean and standard deviation.
        :return: None
        """
        metric = BatchedMeasure()

        t_clock = 0
        t_stop = 1000
        n_batch = 10
        t_batch = t_stop / n_batch
        curr_batch = 0

        expected_sample = 0
        while t_clock < t_stop:
            while curr_batch < n_batch and t_clock < t_batch * (curr_batch+1):
                expected_sample += 1
                metric.increment()
                self.assertEqual(expected_sample, metric.sample())
                t_clock += 1
            metric.register_batch()
            curr_batch += 1

        expected_mean = t_batch
        self.assertEqual(expected_mean, metric.mean())

        expected_sdev = 0
        self.assertEqual(expected_sdev, metric.sdev())