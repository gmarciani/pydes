from core.metrics.accumulator import WelfordAccumulator
from core.metrics.measurement import Measure
from core.metrics.confidence_interval import get_interval_estimation
from statistics import mean
from statistics import stdev


class BatchedMeasure(Measure):
    """
    A measure that has an instantaneous value and computes:
        * mean
        * sdev
        * confidence interval at a given alpha level

    leveraging:
        * batch means method
        * Welford algorithm
    """

    def __init__(self, unit=None):
        """
        Creates a new batch means measure.
        :param unit (String) the measurement unit (Default: None).
        """
        Measure.__init__(self, unit)
        self._batch_means = []
        self._accumulator = WelfordAccumulator()

    def get_batch_means(self):
        """
        Returns the array of batch means.
        :return: the array of batch means.
        """
        return self._batch_means

    def clear(self):
        """
        Resets the measurement as if it is just created.
        :return: None
        """
        # Set the current value to 0.0
        self.set_value(0.0)

        # Discards all accumulated data
        self.discard_data()

    def discard_data(self):
        """
        Discards accumulated data, but retains the current value.
        :return:
        """
        # Reset the accumulator
        self._accumulator.reset()

        # Remove all batches
        self._batch_means.clear()

    def add_sample(self, value):
        """
        Sets the current value and adds this value as a batch sample.
        :param value: (numeric) the value to add as a sample.
        :return: None
        """
        Measure.set_value(self, value)
        self._accumulator.add_value(value)

    def register_batch(self):
        """
        Register and close the current batch.
        :return: None
        """
        # Compute the current batch mean
        curr_batch_mean = self._accumulator.mean()

        # Add the current batch mean to batch means
        self._batch_means.append(curr_batch_mean)

        # Reset the accumulator
        self._accumulator.reset()

    def nbatch(self):
        """
        Returns the total number of batches.
        :return: (int) the total number of batches.
        """
        return len(self._batch_means)

    def curr_batchdim(self):
        """
        Returns the number of samples in the current batch.
        :return: (int) the number of samples in the current batch.
        """
        return self._accumulator.samsize()

    def mean(self):
        """
        Return the mean value among all batch means.
        :return: (float) the mean value among all batches.
        """
        return mean(self._batch_means)

    def sdev(self):
        """
        Return the standard deviation among all batch means.
        :return: (float) the standard deviation among all batches.
        """
        return stdev(self._batch_means) if self.nbatch() > 1 else 0.0

    def cint(self, alpha):
        """
        Return the confidence interval.
        :param alpha: (float) the significance.
        :return: the confidence interval.
        """
        return get_interval_estimation(self.nbatch(), self.sdev(), alpha)
