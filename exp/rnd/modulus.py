"""
EXPERIMENT

Find a suitable modulus for a multi-stream Lehmer pseudo-rnd generator.
Input: number of bits to represent the modulus.
Output: the largest prime number that can be represented by k bits, i.e. less than or equal to 2^(k-1)-1.

Results:
    * 8 bits: 127
    * 16 bits: 32191
    * 32 bits: 2147483647

Notes: results are stored in folder 'out'.
"""
from core.rnd.inspection import modulus_finder
from core.utils.report import SimpleReport
from os import path
from core.utils.logutils import get_logger

# Logging
logger = get_logger(__name__)

# Parameters (Default)
DEFAULT_BITS = 32
DEFAULT_OUTDIR = "out/modulus"


def experiment(bits, outdir=DEFAULT_OUTDIR):
    """
    Find a modulus for the given number of bits.
    :param bits: (int) number of bits; must be positive.
    """
    logger.info("Computing modulus for Bits {}".format(bits))

    filename = path.join(outdir, "mod{}.txt".format(bits))

    modulus = modulus_finder.find_modulus(bits)

    # Report
    r = SimpleReport("MODULUS")
    r.add("General", "Bits", bits)
    r.add("Result", "Modulus", modulus)
    r.save_txt(filename)

    print(r)


if __name__ == "__main__":
    experiment(DEFAULT_BITS)