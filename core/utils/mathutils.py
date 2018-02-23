"""
Utilities for math and statistics.
"""

import math
from _ignore.leemis import rvms


def gcd(a, b):
    """
    Computes the greatest common divisor of a and b.
    :param a: (int) first term.
    :param b: (int) second term.
    :return: (int) the greatest common divisor of a and b.
    """
    while b:
        a, b = b, a % b
    return a


def is_prime(n):
    """
    Checks if n is a prime number.
    :param n: (int) the number to check.
    :return: (Boolean) True if n is prime, False otherwise.
    """
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    max = n**0.5 + 1
    i = 3
    while i <= max:
        if n % i == 0:
            return False
        i += 2
    return True


def are_coprime(a, b):
    """
    Check if a and b are coprime numbers.
    :param a: (int) first term.
    :param b: (int) second term.
    :return: (Boolean) True if a and b are coprime; False, otherwise.
    """
    return gcd(a, b) == 1


def get_frequencies(sample, min, max, bins):
    """
    Computes the frequencies of a bounded sample.
    :param sample: (List(Float)) array of sample values.
    :param min: (Float) the lower bound.
    :param max: (Float) the upper bound.
    :param bins: (Int) the number of bins to divide the interval into.
    :return: (List[Int]) the list of frequencies in bins.
    """

    frequencies = []
    interval = max - min
    binsize = interval / bins

    for bin in range(0, bins):
        frequencies.append(0)

    for value in sample:
        bin = math.floor(value / binsize)
        frequencies[bin] += 1

    return frequencies


def get_frequencies_bivariate(sample, min, max, bins):
    """
    Computes the frequencies of a bounded bivariate sample.
    :param sample: (List((Float,Float)) array of bivariate sample values.
    :param min: (Float) the lower bound.
    :param max: (Float) the upper bound.
    :param bins: (Int) the number of bins to divide the interval into.
    :return: (List[Int]) the list of frequencies in bins.
    """

    frequencies = []
    interval = max -min
    binsize = interval / bins

    for bin1 in range(0, bins):
        frequencies.append([])
        for bin2 in range(0, bins):
            frequencies[bin1].append(0)

    for values in sample:
        bin1 = math.floor(values[0] / binsize)
        bin2 = math.floor(values[1] / binsize)
        frequencies[bin1][bin2] += 1

    return frequencies


def chisquare_univariate(observed, expected, start=0):
    """
    Computes the chi-square statistic for chi-square tests.
    :param observed: (List) array of observations.
    :param expected: (List) array of expected values.
    :param start: (int) index of array from where to start
    :return: (Float) the chi-square statistic.
    """
    K = len(observed)
    value = 0
    for x in range(start, K):
        value += ((observed[x] - expected(x)) ** 2) / expected(x)
    return value


def chisquare_bivariate(observed, expected, start=0):
    """
    Computes the chi-square statistics for bivariate chi-square tests.
    :param observed: (List) array of observations.
    :param expected: (List) array of expected values.
    :param start: (int) index of array from where to start
    :return: (Float) the chi-square statistics.
    """

    K = len(observed)
    value = 0
    for x1 in range(start, K):
        for x2 in range(start, K):
            value += ((observed[x1][x2] - expected(x1, x2)) ** 2) / expected(x1, x2)
    return value


def mean(sample):
    """
    Computes the mean for the univariate sample.
    :param sample: (list(float)) univariate sample.
    :return: (float) the mean.
    """
    return sum(sample) / len(sample)


def variance(sample):
    """
    Computes the variance for the univariate sample.
    :param sample: (list(float)) univariate sample.
    :return: (float) the variance.
    """
    m = mean(sample)
    return sum([(u - m) ** 2 for u in sample]) / len(sample)


def standard_deviation(sample):
    """
    Computes the standard deviation for sample.
    :param sample: (list(float)) univariate sample.
    :return: (float) the standard deviation.
    """
    return math.sqrt(variance(sample))


def covariance(sample):
    """
    Computes the covariance for the bivariate sample.
    :param sample: (list(tuple(float,float)) bivariate sample.
    :return: (float) the covariance.
    """
    sample_u = [value[0] for value in sample]
    sample_v = [value[1] for value in sample]
    mean_u = mean(sample_u)
    mean_v = mean(sample_v)
    return sum([(value[0] - mean_u) * (value[1] - mean_v) for value in sample]) / len(sample)


def correlation_coefficient(sample):
    """
    Computes the correlation coefficient for the bivariate sample.
    :param sample: (list(tuple(float,float)) bivariate sample.
    :return: (float) the correlation coefficient.
    """
    sample_u = [value[0] for value in sample]
    sample_v = [value[1] for value in sample]
    c = covariance(sample)
    deviation_u = standard_deviation(sample_u)
    deviation_v = standard_deviation(sample_v)
    return c / (deviation_u * deviation_v)


def linear_regression_line(sample):
    """
    Computes the linear regression line function for the bivariate sample.
    :param sample: (list(tuple(float,float)) bivariate sample.
    :return: (lambda) the linear regression line function f(u), where u is the
    first component of the bivariate sample.
    """
    sample_u = [value[0] for value in sample]
    sample_v = [value[1] for value in sample]
    mean_u = mean(sample_u)
    mean_v = mean(sample_v)
    variance_u = variance(sample_u)
    variance_v = variance(sample_v)
    c = covariance(sample)
    theta = 0.5 * math.atan2(variance_u - variance_v, 2 * c)

    def line(u): return (u - mean_u) * math.tan(theta) + mean_v

    return line


def interval_estimation(sample, significance):
    """
    Computes the confidence interval for the sample.
    :param sample: (list(float)) univariate sample.
    :param significance: (float) significance in (0,1).
    :return: (float,float,float) the lower bound, the mean and the upper bound.
    """
    samsize = len(sample)
    m = mean(sample)
    s = standard_deviation(sample)
    t = rvms.idfStudent(samsize - 1, 1 - significance / 2)
    i = t * s / math.sqrt(samsize - 1)
    return m - i, m, m + i


class WelfordStatistics(object):

    def __init__(self):
        self._i = 0
        self._mean = 0.0
        self._variance = 0.0

    def update(self, value):
        self._i += 1
        self._variance += ((self._i - 1) / self._i) * math.pow(value - self._mean, 2)
        self._mean += (1 / self._i) * (value - self._mean)

    def get_mean(self):
        return self._mean

    def get_variance(self):
        return self._variance / self._i


def _g(x, multiplier, modulus):
    """
    An implementation of the G function that avoids overflows.
    :param x: (int) the current state of the generator.
    :param multiplier: (int) a valid multiplier w.r.t. modulus.
    :param modulus: (int) a prime number.
    :return: (int) the next state of the generator.
    """
    q = int(modulus / multiplier)
    r = int(modulus % multiplier)
    t = int(multiplier * (x % q) - r * int(x / q))
    if t > 0:
        return int(t)
    else:
        return int(t + modulus)
