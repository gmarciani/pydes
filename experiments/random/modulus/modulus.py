"""
EXPERIMENT

Find a suitable modulus for a multi-stream Lehmer pseudo-random generator.
Input: number of bits to represent the modulus.
"""
from core.random.inspection import modulus_finder
from core.utils.report import SimpleReport


DEFAULT_BITS = 8


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
    r.save("experiment_modulus_{}.txt".format(bits))

    print(r)


if __name__ == "__main__":
    experiment(DEFAULT_BITS)
    