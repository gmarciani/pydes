from math import floor
from demule.common.mathutils import gcd


def generateFullPeriodModulusCompatibleMultipliers(multiplier, modulus):
    multipliers = []
    i = 1
    x = multiplier
    while x != 1:
        if isModulusCompatible(multiplier, modulus) and gcd(i, modulus - 1):
            multipliers.append(x)
        i += 1
        x = g(x, multiplier, modulus)
    return multipliers


def generateFullPeriodMultipliers(multiplier, modulus): # multiplier must be a full-period multiplier, modulus must be prime
    multipliers = []
    i = 1
    x = multiplier
    while x != 1:
        if gcd(i, modulus - 1) == 1:
            multipliers.append(x)
            i += 1
            x = (multiplier * x) % modulus
    return multipliers


def isFullPeriodMultiplier(multiplier, modulus): # m must be prime
    period = 1
    x = multiplier
    while x != 1:
        period += 1
        x = (multiplier * x) % modulus
    if period == (modulus - 1):
        return True
    else:
        return False


def isModulusCompatible(multiplier, modulus):
    return (modulus % multiplier) < floor(modulus / multiplier)