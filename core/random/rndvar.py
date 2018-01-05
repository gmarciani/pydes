"""
Generators of random variates.
"""

from math import log


def equilikely(a, b, u):
    """
    Generates an Equilikely random variate in *[a,b]*.
    Must be a < b.
    :param a: (int) lower bound.
    :param b: (int) upper bound.
    :param u: (float) random number in (0,1).
    :return: (float) the Equilikely(a,b) random variate.
    """
    return a + int((b - a + 1) * u)


def exponential(m, u):
    """
    Generates an Exponential random variate with average *m*.
    :param m: (float) average of the distribution; must be m > 0.0
    :param u: (float) random number in (0,1).
    :return: (float) the Exp(m) random variate.
    """
    return -m * log(1.0 - u)


def geometric(p, u):
    """
    Generates a Geometric random variate with parameter *p*.
    :param p: (float) parameter of the distribution; must be 0.0 < p < 1.0
    :param u: (float) random number in (0,1).
    :return: (float) the Geom(p) random variate.
    """
    return int(log(1.0 - u) / log(p))


def uniform(a, b, u):
    """
    Generates a Uniform random variate in *(a,b)*.
    Must be a < b.
    :param a: (float) lower bound.
    :param b: (float) upper bound.
    :param u: (float) random number in (0,1).
    :return: (float) the Uniform(a,b) random variate.
    """
    return a + (b - a) * u
