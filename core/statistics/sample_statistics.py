from math import sqrt
import numpy as np


class SimpleSampleStatistics:
    """
    A simple sample statistics calculator.
    It calculates:
        * sample mean
        * sample variance
        * sample standard deviation.
    """

    def __init__(self):
        """
        Create a new *SimpleStatisticsCalculator*.
        """
        self._n = 0  # the number of values

        # statistics
        self._mean = 0.0  # the mean value
        self._variance = 0.0  # the variance

    def reset(self):
        """
        Reset statistics.
        :return: None
        """
        self._n = 0
        self._mean = 0.0
        self._variance = 0.0

    def add_value(self, value):
        """
        Add value to the statistics calculator.
        :param value: the value to add.
        :return: None
        """
        self._n += 1

        # update mean and variance, leveraging the Welford's algorithm
        delta_value = value - self._mean
        self._variance += pow(delta_value, 2) * (1.0 * (self._n - 1) / self._n)
        self._mean += delta_value / self._n

    def get_dimension(self):
        """
        Return the sample dimension.
        :return: (int) the sample dimension.
        """
        return self._n

    def get_mean(self):
        """
        Return the sample mean.
        :return: (float) the sample mean.
        """
        return self._mean

    def get_variance(self):
        """
        Return the sample variance.
        :return: (float) the sample variance.
        """
        return self._variance / self._n

    def get_sdev(self):
        """
        Return the sample standard deviation.
        :return: (float) the sample standard deviation.
        """
        return sqrt(self._variance / self._n)

    def __str__(self):
        """
        String representation.
        :return: the string representation.
        """
        sb = ["{attr}={value}".format(attr=attr, value=self.__dict__[attr]) for attr in self.__dict__ if
              not attr.startswith("__") and not callable(getattr(self, attr))]
        return "SampleStatistics({}:{})".format(id(self), ", ".join(sb))

    def __repr__(self):
        """
        String representation.
        :return: the string representation.
        """
        return self.__str__()