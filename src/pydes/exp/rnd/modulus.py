"""
EXPERIMENT

Find a suitable modulus for a multi-stream Lehmer pseudo-random generator.
Input: number of bits to represent the modulus.
Output: the largest prime number that can be represented by k bits, i.e. less than or equal to 2^(k-1)-1.

Notes: results are stored in folder 'out/modulus'.
"""
from os import path

from pydes.core.rnd.inspection import modulus_finder
from pydes.core.utils.logutils import get_logger
from pydes.core.utils.report import SimpleReport

# Logging
logger = get_logger(__name__)

# Defaults
DEFAULT_BITS = 32
DEFAULT_OUTDIR = "out/modulus"


def run(bits, outdir=DEFAULT_OUTDIR):
    """
    Find a modulus for the given number of bits.
    :param bits: (int) number of bits; must be positive.
    :param outdir: (str) path to the output directory.
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
    run(DEFAULT_BITS)
