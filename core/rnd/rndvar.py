"""
Generators of random variates.
"""

import math


def exponential(m, u):
    """
    Generates an Exponential random variate with average *m*.
    :param m: (float) average of the distribution; must be m > 0
    :param u: (float) random number in (0,1).
    :return: (float) the Exp(m) random variate.
    """
    return - m * math.log(1.0 - u)


def equilikely(a, b, u):
    """
    Generates an Equilikely random variate in *[a,b]*.
    :param a: (int) lower bound.
    :param b: (int) upper bound.
    :param u: (float) random number in (0,1).
    :return: (float) the Equilikely(a,b) random variate.
    """
    return a + int((b - a + 1)*u)


def uniform(a, b, u):
    """
    Generates a Uniform random variate in *(a,b)*.
    :param a: (float) lower bound.
    :param b: (float) upper bound.
    :param u: (float) random number in (0,1).
    :return: (float) the Uniform(a,b) random variate.
    """
    return a + (b - a) * u
