"""
EXPERIMENT

Spectral Test of Randomness.

Input:
    * the pseudo-rnd number generator, characterized by its modulus and multiplier.
    * the sample size.
    * the interval [a,b].

Output: the distribution of rnd number within the specified interval.

Notes: results are stored in folder 'out/spectral'.
"""
from os import path

from pydes.core.rnd.randomness import spectral as test
from pydes.core.rnd.rndgen import MarcianiSingleStream
from pydes.core.utils.logutils import get_logger
from pydes.core.utils.report import SimpleReport

# Logging
logger = get_logger(__name__)

# Defaults
DEFAULT_MODULUS = 2147483647
DEFAULT_MULTIPLIER = 50812
DEFAULT_GENERATOR = MarcianiSingleStream(modulus=DEFAULT_MODULUS, multiplier=DEFAULT_MULTIPLIER)
DEFAULT_SAMSIZE = DEFAULT_MODULUS - 1
DEFAULT_INTERVAL = (0.0, 0.001)
DEFAULT_OUTDIR = "out/spectral"


def run(g, samsize, interval, outdir):

    logger.info(
        "Spectral Test for Modulus {} Multiplier {} Samsize {} Interval {}".format(
            g.get_modulus(), g.get_multiplier(), samsize, interval
        )
    )

    filename = path.join(outdir, "mod{}_mul{}".format(g.get_modulus(), g.get_multiplier()))

    # Statistics: [(u1, u2),(u2,u3)...,(un-1,un)]
    test.statistics(filename + ".csv", g, samsize, interval)

    # Report
    r = SimpleReport("SPECTRAL TEST")
    r.add("Generator", "Class", g.__class__.__name__)
    r.add("Generator", "Modulus", g.get_modulus())
    r.add("Generator", "Multiplier", g.get_multiplier())
    r.add("Generator", "Seed", g.get_initial_seed())
    r.add("Test Parameters", "Sample Size", samsize)
    r.add("Test Parameters", "Interval", interval)

    r.save_txt(filename + "_report.txt")
    r.save_csv(filename + "_report.csv")

    logger.info("Report:\n{}".format(r))


if __name__ == "__main__":
    modulus = DEFAULT_MODULUS
    multiplier = DEFAULT_MULTIPLIER
    samsize = DEFAULT_SAMSIZE
    interval = DEFAULT_INTERVAL
    outdir = DEFAULT_OUTDIR

    generator = MarcianiSingleStream(modulus=modulus, multiplier=multiplier)
    run(generator, samsize, interval, outdir)
