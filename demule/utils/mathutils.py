"""
A collection of mathematical and statistical utilities.
"""

import math


def gcd(a, b):
    """
    Computes the greatest common divisor of a and b.
    :param a: (int) first term.
    :param b: (int) second term
    :return: (int) the greatest common divisor of a and b.
    """
    while b:
        a, b = b, a % b
    return a


def isprime(n):
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
    Computes the chi-square statistics for chi-square tests.
    :param observed: (List) array of observations.
    :param expected: (List) array of expected values.
    :param start: (int) index of array from where to start
    :return: (Float) the chi-square statistics.
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