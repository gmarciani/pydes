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
from core.utils.guiutils import print_progress
from core.utils.mathutils import _g


def get_fp_multipliers(modulus):
    """
    Generate a list of FP multipliers w.r.t the specified modulus.
    :param modulus: a prime number.
    :return: (List) FP multipliers w.r.t modulus.
    """
    fp_multipliers = []

    first_fpm = None
    for i in range(1, modulus):
        if is_fp_multiplier(i, modulus):
            first_fpm = i
            break
        print_progress(i, modulus)

    if first_fpm is not None:
        if first_fpm is 1:
            fp_multipliers.append(first_fpm)
        generated_fpm = generate_fp_multipliers(first_fpm, modulus)
        fp_multipliers.extend(generated_fpm)

    return fp_multipliers


def get_mc_multipliers(modulus):
    """
    Generate a list of MC multipliers w.r.t the specified modulus.
    :param modulus: a prime number.
    :return: (List) MC multipliers w.r.t modulus.
    """
    mc_multipliers = []
    for i in range(1, modulus):
        is_mcm = is_mc_multiplier(i, modulus)
        if is_mcm:
            mc_multipliers.append(i)
        print_progress(i, modulus)
    return mc_multipliers


def get_first_fp_multiplier(modulus):
    """
    Generate the first FP multiplier w.r.t the specified modulus.
    :param modulus: a prime number.
    :return: (int) the first FP multiplier w.r.t modulus, if exists; None, otherwise.
    """
    for i in range(1, modulus):
        if is_fp_multiplier(i, modulus):
            return i
    return None


def generate_fp_multipliers(multiplier, modulus):
    """
    Generate a list of FP multipliers from the specified multiplier w.r.t the specified modulus.
    :param multiplier: must be a FP multiplier w.r.t. modulus.
    :param modulus: a prime number.
    :return: (List) FP multipliers w.r.t modulus.
    """
    fp_multipliers = []
    i = 1
    x = multiplier
    while x != 1:
        if mathutils.are_coprime(i, modulus - 1):
            fp_multipliers.append(x)
        i += 1
        x = (multiplier * x) % modulus
    return fp_multipliers


def generate_fpmc_multipliers(multiplier, modulus):
    """
    Generate a list of FP/MC multipliers from the specified multiplier w.r.t the specified modulus.
    :param multiplier: must be a FP/MC multiplier w.r.t. modulus.
    :param modulus: a prime number.
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
    return period == (modulus - 1)


def is_mc_multiplier(multiplier, modulus):
    """
    Checks if multiplier is a MC multiplier w.r.t. modulus.
    :param multiplier: an integer in (0, modulus).
    :param modulus: a prime number.
    :return: True if multiplier is a MC multiplier w.r.t. modulus.
    """
    return (modulus % multiplier) < math.floor(modulus / multiplier)


def _test():
    """
    Tests the correctness of functions.
    :raise: RuntimeError: the specified function is not correct.
    """
    MODULUS = 32749
    MULTIPLIER = 16374

    if not is_fp_multiplier(MULTIPLIER, MODULUS):
        raise RuntimeError("Function is_fp_multiplier contains errors")

    if not is_mc_multiplier(MULTIPLIER, MODULUS):
        raise RuntimeError("Function is_mc_multiplier contains errors")

    MODULI = [2, 3, 5, 7, 11, 13]
    NUM_FPM = [1, 1, 2, 2, 4, 4]
    FIRST_FPM = [1, 2, 2, 3, 2, 2]
    for i in range(len(MODULI)):
        modulo = MODULI[i]
        expected_num_fpm = NUM_FPM[i]
        expected_first_fpm = FIRST_FPM[i]

        fp_multipliers = get_fp_multipliers(modulo)
        actual_num_fpm = len(fp_multipliers)
        actual_first_fpm = min(fp_multipliers, default=None)

        if actual_num_fpm != expected_num_fpm:
            raise RuntimeError(
                "Error: get_fp_multipliers | number of FP multipliers for {} should be {}, but are {})".format(
                    modulo, expected_num_fpm, actual_num_fpm ))

        if actual_first_fpm != expected_first_fpm:
            raise RuntimeError(
                "Error: get_fp_multipliers | first FP multiplier for {} should be {}, but are {})".format(
                    modulo, expected_first_fpm, actual_first_fpm))


if __name__ == '__main__':
    _test()
