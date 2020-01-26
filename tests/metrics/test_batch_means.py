import unittest
from core.metrics.batch_means import BatchedMeasure
from random import randint
from statistics import mean, stdev
from copy import deepcopy


class BatchMeansTest(unittest.TestCase):

    def test_int(self):
        """
        Test the calculation of mean and standard deviation leveraging batch means on rnd integer samples.
        :return: None
        """

        # Creation
        metric = BatchedMeasure()

        # Settings
        desired_nbatch = 10
        desired_batchdim = 100

        precision = 5


        # Samples
        samples = []

        # Execution
        while metric.nbatch() < desired_nbatch:
            sample = randint(1, 1000)
            samples.append(sample)
            metric.add_sample(sample)
            if metric.curr_batchdim() == desired_batchdim:
                metric.register_batch()

        expected_samples = desired_nbatch * desired_batchdim
        expected_nbatch = desired_nbatch
        expected_curr_batchdim = 0
        expected_curr_value = samples[-1]

        expected_batches = []
        curr_batch = []
        for i in range(len(samples)):
            curr_batch.append(samples[i])
            if (i+1) % desired_batchdim == 0:
                expected_batches.append(deepcopy(curr_batch))
                curr_batch.clear()

        expected_batch_means = [mean(batch) for batch in expected_batches]
        expected_mean = mean(expected_batch_means)
        expected_sdev = stdev(expected_batch_means)

        self.assertEqual(expected_samples, len(samples))
        self.assertEqual(expected_nbatch, metric.nbatch())
        self.assertEqual(expected_curr_batchdim, metric.curr_batchdim())
        self.assertEqual(expected_curr_value, metric.get_value())
        self.assertEqual(len(expected_batch_means), len(metric.get_batch_means()))
        for i in range(len(expected_batch_means)):
            self.assertEqual(round(expected_batch_means[i], precision), round(metric.get_batch_means()[i], precision))
        self.assertEqual(round(expected_mean, precision), round(metric.mean(), precision))
        self.assertEqual(round(expected_sdev, precision), round(metric.sdev(), precision))