from core.random.inspection.multiplier_check import is_mc_multiplier
from core.utils.mathutils import _g
from core.utils.guiutils import print_progress


def find_jumpers(modulus, multiplier, streams):
    """
    Find all jumpers.
    :param modulus: (int) the modulus.
    :param multiplier: (int) the multiplier.
    :param streams: (int) the number of streams.
    :return: a list of all modulus compatible jumpers.
    """
    jumpers = []
    jsize_max = int((modulus + 1) / streams)
    jumper = 1
    for jsize in range(1, jsize_max+1):
        jumper = _g(jumper, multiplier, modulus)
        if is_mc_multiplier(jumper, modulus):
            jumpers.append((jumper, jsize))
        print_progress(jsize, jsize_max)
    return jumpers


def find_jumper(modulus, multiplier, streams):
    """
    Find a jumper.
    :param modulus: (int) the modulus.
    :param multiplier: (int) the multiplier.
    :param streams: (int) the number of streams.
    :return: a modulus compatible jumpers.
    """
    jsize_max = int((modulus + 1) / streams)
    jumper = 1
    for jsize in range(1, jsize_max+1):
        jumper = _g(jumper, multiplier, modulus)
        if is_mc_multiplier(jumper, modulus):
            return jumper, jsize
    return None