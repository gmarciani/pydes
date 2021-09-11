from core.rnd.rndf import idfStudent
from math import sqrt


def get_interval_estimation(samsize, sdev, alpha):
    """
    Returns the interval estimation.
    :param samsize: (int) the sample size.
    :param sdev: (float) the sample standard deviation.
    :param alpha: (float) the significance.
    :return: (float) the interval gap.
    """
    if samsize > 1:
        return idfStudent(samsize - 1, 1.0 - (alpha / 2)) * sdev / sqrt(samsize - 1)
    else:
        return 0.0
