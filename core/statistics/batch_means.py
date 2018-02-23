from core.statistics.sample_path_statistics import SimpleSamplePathStatistic
from core.statistics.sample_statistics import SimpleSampleStatistic
from core.statistics.interval_estimation import get_interval_estimation
from statistics import mean, stdev
from abc import ABCMeta


class BatchedMeasure():
    """
    A batch mean measure.
    """

    def __init__(self):
        """
        Create a new batch means measure.
        """
        self.batch_means = []
        self.curr_value = 0

    def close_batch(self):
        """
        Close the current batch.
        :return: None
        """
        curr_batch_mean = self.curr_value
        self.batch_means.append(curr_batch_mean)
        self.curr_value = 0


class BatchedStatistic(metaclass=ABCMeta):
    """
    A batch mean statistic.
    """

    def __init__(self):
        """
        Create a new batch means statistic.
        """
        self.batch_means = []
        self.curr_statistic = None  # abstract attribute

    def get_batch_value(self, batch):
        """
        Get the value for the specified batch.
        :param batch: (int) the batch index.
        :return: the value for the specified batch.
        """
        return self.batch_means[batch]

    def register_batch(self):
        """
        Register and close the current batch.
        :return: None
        """
        curr_batch_mean = self.curr_statistic.mean()
        self.batch_means.append(curr_batch_mean)
        self.curr_statistic.reset()

    def discard_batch(self):
        """
        Discard the current batch.
        :return: None
        """
        self.curr_statistic.reset()

    def nbatch(self):
        """
        Retunr the total number of batches.
        :return: (int) the total number of batches.
        """
        return len(self.batch_means)

    def mean(self):
        """
        Return the mean value among all batch means.
        :return: (float) the mean value among all batches.
        """
        return mean(self.batch_means)

    def sdev(self):
        """
        Return the standard deviation among all batch means.
        :return: (float) the standard deviation among all batches.
        """
        return stdev(self.batch_means) if self.nbatch() > 1 else 0.0

    def cint(self, alpha):
        """
        Return the confidence interval.
        :param alpha: (float) the significance.
        :return: the confidence interval.
        """
        return get_interval_estimation(self.nbatch(), self.sdev(), alpha)


class BatchedSampleStatistic(BatchedStatistic):
    """
    A batch mean statistic with the running statistic as simple sample statistic.
    """

    def __init__(self):
        """
        Create a new batch mean statistic.
        """
        BatchedStatistic.__init__(self)
        self.curr_statistic = SimpleSampleStatistic()

    def add_sample(self, value):
        """
        Add a sample value to the current batch.
        :param value: the value to add.
        :return: None
        """
        self.curr_statistic.add_value(value)


class BatchedSamplePathStatistic(BatchedStatistic):
    """
    A batch mean statistic with the running statistic as sample path statistic.
    """

    def __init__(self):
        """
        Create a new batch mean statistic.
        """
        BatchedStatistic.__init__(self)
        self.curr_statistic = SimpleSamplePathStatistic()

    def add_sample(self, value, t_now):
        """
        Add a sample value to the current batch.
        :param value: the value to add.
        :param t_now: the time.
        :return: None
        """
        self.curr_statistic.add_value(value, t_now)