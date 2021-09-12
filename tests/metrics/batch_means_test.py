import unittest
from copy import deepcopy
from random import randint
from statistics import mean, stdev

from pydes.core.metrics.batch_means import BatchedMeasure

N_BATCH = 10
BATCH_DIM = 100
PRECISION = 10


class BatchMeansTest(unittest.TestCase):
    def setUp(self):
        self.metric = BatchedMeasure()
        self.samples = []
        while self.metric.nbatch() < N_BATCH:
            sample = randint(1, 1000)
            self.samples.append(sample)
            self.metric.add_sample(sample)
            if self.metric.curr_batchdim() == BATCH_DIM:
                self.metric.register_batch()

        assert len(self.samples) == N_BATCH * BATCH_DIM

    def test_batching(self):
        expected_nbatch = N_BATCH
        expected_curr_batchdim = 0
        expected_curr_value = self.samples[-1]

        self.assertEqual(expected_nbatch, self.metric.nbatch())
        self.assertEqual(expected_curr_batchdim, self.metric.curr_batchdim())
        self.assertEqual(expected_curr_value, self.metric.get_value())

    def test_batch_means(self):
        expected_batches = []
        curr_batch = []
        for i in range(len(self.samples)):
            curr_batch.append(self.samples[i])
            if (i + 1) % BATCH_DIM == 0:
                expected_batches.append(deepcopy(curr_batch))
                curr_batch.clear()

        expected_batch_means = [mean(batch) for batch in expected_batches]
        expected_mean = mean(expected_batch_means)
        expected_sdev = stdev(expected_batch_means)

        self.assertEqual(len(expected_batch_means), len(self.metric.get_batch_means()))
        for i in range(len(expected_batch_means)):
            self.assertEqual(
                round(expected_batch_means[i], PRECISION), round(self.metric.get_batch_means()[i], PRECISION)
            )
        self.assertEqual(round(expected_mean, PRECISION), round(self.metric.mean(), PRECISION))
        self.assertEqual(round(expected_sdev, PRECISION), round(self.metric.sdev(), PRECISION))
