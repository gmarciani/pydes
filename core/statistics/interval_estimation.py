from core.random.rndf import idfStudent
from math import sqrt


def get_interval_exstimation(samsize, sdev, alpha):
    """
    Get the interval exstimation.
    :param samsize: (int) the sample size.
    :param sdev: (float) the sample standard deviation.
    :param alpha: (float) the significance.
    :return: (float) the interval gap.
    """
    return idfStudent(samsize - 1, 1.0 - (alpha / 2)) * sdev / sqrt(samsize -1)
