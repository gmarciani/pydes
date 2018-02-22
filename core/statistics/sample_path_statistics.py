from math import sqrt


class SimpleSamplePathStatistic:
    """
    A simple sample-path statistics calculator.
    It calculates:
        * sample-path mean
        * sample-path variance
        * sample-path standard deviation.
    """

    def __init__(self):
        """
        Create a new *SimpleStatisticsCalculator*.
        """
        self._n = 0  # the number of values
        self._time = 0.0  # the current time

        # statistics
        self._mean = 0.0  # the mean value
        self._variance = 0.0  # the variance

    def reset(self):
        """
        Reset statistics.
        :return: None
        """
        self._n = 0
        self._time = 0.0

        self._mean = 0.0
        self._variance = 0.0

    def add_value(self, value, t_now):
        """
        Add value to the statistics calculator.
        :param value: the value to add.
        :param t_now: the occurrence time.
        :return: None
        """
        self._n += 1
        t_prev = self._time
        self._time = t_now

        # update mean and variance, leveraging the Welford's algorithm
        delta_value = value - self._mean
        delta_time = t_now - t_prev
        self._variance += pow(delta_value, 2) * delta_time * t_prev / t_now
        self._mean += delta_value * delta_time / t_now

    def samsize(self):
        """
        Return the sample dimension.
        :return: (int) the sample dimension.
        """
        return self._n

    def time(self):
        """
        Return the sample last time.
        :return: (int) the sample last time.
        """
        return self._time

    def mean(self):
        """
        Return the sample-path mean.
        :return: (float) the sample-path mean.
        """
        return self._mean

    def var(self):
        """
        Return the sample-path variance.
        :return: (float) the sample-path variance.
        """
        return self._variance / self._time

    def sdev(self):
        """
        Return the sample-path standard deviation.
        :return: (float) the sample-path standard deviation.
        """
        return sqrt(self._variance / self._time)

    def __str__(self):
        """
        String representation.
        :return: the string representation.
        """
        sb = ["{attr}={value}".format(attr=attr, value=self.__dict__[attr]) for attr in self.__dict__ if
              not attr.startswith("__") and not callable(getattr(self, attr))]
        return "SamplePathStatistics({}:{})".format(id(self), ", ".join(sb))