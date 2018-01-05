"""
Collection of functions to check and generate multipliers w.r.t. moduluses.

A multiplier could be full-period (FP), modulus-compatible (MC), or both (FP/MC).
A valid multiplier sould be FP/MC.

Keep in mind the following table:

╔════════════╦════════════════════════════════════════════════╗
║            ║                      BITS                      ║
║            ╠═════╦═══════╦════════════╦═════════════════════╣
║            ║ 8   ║ 16    ║ 32         ║ 64                  ║
╠════════════╬═════╬═══════╬════════════╬═════════════════════╣
║ MODULUS    ║ 127 ║ 32479 ║ 2147483647 ║ 9223372036854775783 ║
╠════════════╬═════╬═══════╬════════════╬═════════════════════╣
║ MULTIPLIER ║ 14  ║ 16374 ║ 48271      ║                     ║
╚════════════╩═════╩═══════╩════════════╩═════════════════════╝
"""

import math
from core.utils import mathutils


def generate_fpmc_multipliers(multiplier, modulus):
    """
    Generate a list of FP/MC multipliers from the specified multiplier w.r.t
    the specified modulus.
    :param multiplier: must be a FP/MC multiplier w.r.t. modulus.
    :param modulus: a prime number
    :return: (List) FP/MC multipliers w.r.t modulus.
    """
    multipliers = []
    i = 1
    x = multiplier
    while x != 1:
        if is_mc_multiplier(multiplier, modulus) and mathutils.gcd(i, modulus - 1):
            multipliers.append(x)
        i += 1
        x = _g(x, multiplier, modulus)
    return multipliers


def generate_fp_multipliers(multiplier, modulus):
    """
    Generate a list of FP multipliers from the specified multiplier w.r.t
    the specified modulus.
    :param multiplier: must be a FP multiplier w.r.t. modulus.
    :param modulus: a prime number
    :return: (List) FP multipliers w.r.t modulus.
    """
    multipliers = []
    i = 1
    x = multiplier
    while x != 1:
        if mathutils.gcd(i, modulus - 1) == 1:
            multipliers.append(x)
            i += 1
            x = (multiplier * x) % modulus
    return multipliers


def is_fp_multiplier(multiplier, modulus):
    """
    Checks if multiplier is a FP multiplier w.r.t. modulus.
    :param multiplier: an integer in (0, modulus).
    :param modulus: a prime number.
    :return: True if multiplier is a FP multiplier w.r.t. modulus.
    """
    period = 1
    x = multiplier
    while x != 1:
        period += 1
        x = (multiplier * x) % modulus
    if period == (modulus - 1):
        return True
    else:
        return False


def is_mc_multiplier(multiplier, modulus):
    """
    Checks if multiplier is a MC multiplier w.r.t. modulus.
    :param multiplier: an integer in (0, modulus).
    :param modulus: a prime number.
    :return: True if multiplier is a MC multiplier w.r.t. modulus.
    """
    return (modulus % multiplier) < math.floor(modulus / multiplier)


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


def _test():
    """
    Tests the correctness of functions.
    :raise: RuntimeError: the specified function is not correct.
    """
    MODULUS = 32749
    MULTIPLIER = 16374

    if not is_fp_multiplier(MULTIPLIER, MODULUS):
        raise RuntimeError('The FP multiplier test is not well implemented')

    if not is_mc_multiplier(MULTIPLIER, MODULUS):
        raise RuntimeError('The MC multiplier test is not well implemented')


if __name__ == '__main__':
    _test()
