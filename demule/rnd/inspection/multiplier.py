from math import floor
from demule.utils.mathutils import gcd
from demule.rnd.custom.gfunc import g


def generate_fpmc_multipliers(multiplier, modulus):
    multipliers = []
    i = 1
    x = multiplier
    while x != 1:
        if is_mc_multiplier(multiplier, modulus) and gcd(i, modulus - 1):
            multipliers.append(x)
        i += 1
        x = g(x, multiplier, modulus)
    return multipliers


def generate_fp_multipliers(multiplier, modulus): # multiplier must be a full-period multiplier, modulus must be prime
    multipliers = []
    i = 1
    x = multiplier
    while x != 1:
        if gcd(i, modulus - 1) == 1:
            multipliers.append(x)
            i += 1
            x = (multiplier * x) % modulus
    return multipliers


def is_fp_multiplier(multiplier, modulus): # m must be prime
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
    return (modulus % multiplier) < floor(modulus / multiplier)