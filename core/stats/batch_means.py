from core.stats.sample_path_statistics import SimpleSamplePathStatistic
from core.stats.sample_statistics import SimpleSampleStatistic
from core.stats.interval_estimation import get_interval_estimation
from statistics import mean
from statistics import stdev


class BaseBatchedMeasure:
    """
    The base class for batched measures and sample statistics.
    """

    def __init__(self):
        """
        Create a new batch means measure.
        """
        self.batch_values = []
        self.curr_value = self.init_value()

    def init_value(self):
        """
        Initialize the value.
        :return: the initialized value.
        """
        return None

    def compute_batch_value(self):
        """
        Compute the current batch value from the current value.
        :return: the batch value.
        """
        return self.curr_value

    def reset_value(self):
        """
        Reset the current value.
        :return: None
        """
        self.curr_value = None

    def get_value(self, batch=None):
        """
        Get the value for the specified batch.
        :param batch: (int) the batch index (Default: current batch).
        :return: the value for the specified batch, or the current batch if not specified.
        """
        return self.batch_values[batch] if batch is not None else self.curr_value

    def set_value(self, value, batch=None):
        """
        Set the value for the specified or current batch.
        :param value: the value.
        :param batch: (int) the batch index (Default: current batch).
        :return: None
        """
        if batch is not None:
            self.batch_values[batch] = value
        else:
            self.curr_value = value

    def register_batch(self):
        """
        Register and close the current batch.
        :return: None
        """
        curr_batch_value = self.compute_batch_value()
        self.batch_values.append(curr_batch_value)
        self.reset_value()

    def discard_batch(self):
        """
        Discard the current batch.
        :return: None
        """
        self.reset_value()

    def nbatch(self):
        """
        Retunr the total number of batches.
        :return: (int) the total number of batches.
        """
        return len(self.batch_values)

    def mean(self):
        """
        Return the mean value among all batch means.
        :return: (float) the mean value among all batches.
        """
        return mean(self.batch_values)

    def sdev(self):
        """
        Return the standard deviation among all batch means.
        :return: (float) the standard deviation among all batches.
        """
        return stdev(self.batch_values) if self.nbatch() > 1 else 0.0

    def cint(self, alpha):
        """
        Return the confidence interval.
        :param alpha: (float) the significance.
        :return: the confidence interval.
        """
        return get_interval_estimation(self.nbatch(), self.sdev(), alpha)


class BatchedMeasure(BaseBatchedMeasure):
    """
    A batch mean measure.
    """

    def __init__(self):
        """
        Create a new batch means measure.
        """
        BaseBatchedMeasure.__init__(self)
        self.global_value = self.init_value()

    def init_value(self):
        """
        Initialize the value.
        :return: the initialized value.
        """
        return 0.0

    def compute_batch_value(self):
        """
        Compute the current batch value from the current value.
        :return: the batch value.
        """
        return self.curr_value

    def reset_value(self):
        """
        Reset the current value.
        :return: None
        """
        self.curr_value = 0.0

    def set_value(self, value, batch=None):
        """
        Set the value for the specified or current batch.
        :param value: the value.
        :param batch: (int) the batch index (Default: current batch).
        :return: None
        """
        if batch is not None:
            self.batch_values[batch] = value
        else:
            self.curr_value = value
            self.global_value = value

    def increment(self, value=1):
        """
        Add the value.
        :param value: the value (Default: 1).
        :return: None
        """
        self.curr_value += value
        self.global_value += value

    def decrement(self, value=1):
        """
        Substract the value.
        :param value: the value (Default: 1).
        :return: None
        """
        self.curr_value -= value
        self.global_value -= value

    def sample(self):
        """
        Return the global value.
        :return: the global value.
        """
        return self.global_value


class BatchedSampleMeasure(BaseBatchedMeasure):
    """
    A batch mean statistic with the running statistic as simple sample statistic.
    """

    def __init__(self):
        """
        Create a new batch mean statistic.
        """
        BaseBatchedMeasure.__init__(self)
        self.global_value = 0.0

    def init_value(self):
        """
        Initialize the value.
        :return: the initialized value.
        """
        return SimpleSampleStatistic()

    def compute_batch_value(self):
        """
        Compute the current batch value from the current value.
        :return: the batch value.
        """
        return self.curr_value.mean()

    def reset_value(self):
        """
        Reset the current value.
        :return: None
        """
        self.curr_value.reset()

    def add_sample(self, value):
        """
        Add a sample value to the current batch.
        :param value: the value to add.
        :return: None
        """
        self.curr_value.add_value(value)
        self.global_value = value

    def sample(self):
        """
        Return the global value.
        :return: the global value.
        """
        return self.curr_value.mean()


class BatchedSamplePathStatistic(BaseBatchedMeasure):
    """
    A batch mean statistic with the running statistic as sample path statistic.
    """

    def __init__(self):
        """
        Create a new batch mean statistic.
        """
        BaseBatchedMeasure.__init__(self)

    def init_value(self):
        """
        Initialize the value.
        :return: the initialized value.
        """
        return SimpleSamplePathStatistic()

    def compute_batch_value(self):
        """
        Compute the current batch value from the current value.
        :return: the batch value.
        """
        return self.curr_value.mean()

    def reset_value(self):
        """
        Reset the current value.
        :return: None
        """
        t_batch_start = self.curr_value.time()
        self.curr_value.reset(t_start=t_batch_start)

    def add_sample(self, value, t_now):
        """
        Add a sample value to the current batch.
        :param value: the value to add.
        :param t_now: the time.
        :return: None
        """
        self.curr_value.add_value(value, t_now)