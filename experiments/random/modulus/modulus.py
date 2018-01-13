"""
EXPERIMENT

Find a suitable modulus for a multi-stream Lehmer pseudo-random generator.
Input: number of bits to represent the modulus.
Output: the largest prime number that can be represented by k bits, i.e. less than or equal to 2^(k-1)-1.

Results:
    * 8 bits: 127
    * 16 bits: 32191
    * 32 bits: 2147483647

Notes: results are stored in folder 'out'.
"""
from core.random.inspection import modulus_finder
from core.utils.report import SimpleReport
from os import path

DEFAULT_BITS = 32


def experiment(bits):
    """
    Find a modulus for the given number of bits.
    :param bits: (int) number of bits; must be positive.
    """
    modulus = modulus_finder.find_modulus(bits)

    # Report
    r = SimpleReport("MODULUS")
    r.add("General", "Bits", bits)
    r.add("Result", "Modulus", modulus)
    r.save(path.join("out", "modulus_{}.txt".format(bits)))

    print(r)


if __name__ == "__main__":
    experiment(DEFAULT_BITS)