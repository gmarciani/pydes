"""
EXPERIMENT

Spectral Test of Randomness.

Input:
    * the pseudo-rnd number generator, characterized by its modulus and multiplier.
    * the sample size.
    * the interval [a,b].
    
Output: the distribution of rnd number within the specified interval.

Notes: results are stored in folder 'out' and can be visualized by running the Matlab script 'spectral.m'.

Results:
    * (2147483647, 16807): not good
    * (2147483647, 48271): good
    * (2147483647, 50812): good
"""
from core.rnd.rndgen import MarcianiSingleStream
from core.rnd.randomness import spectral as test
from core.utils.report import SimpleReport
from os import path
from core.utils.logutils import ConsoleHandler
from core.utils.logutils import get_logger

# Logging
logger = get_logger(__name__)


# Generator
DEFAULT_GENERATOR = MarcianiSingleStream()

# Sample size
DEFAULT_SAMSIZE = 100000

# Zoom interval
DEFAULT_INTERVAL = (0.0, 1.0)

# Directory for results
DEFAULT_OUTDIR = "out/spectral"


def experiment(g, samsize, interval, outdir):

    logger.info("Spectral Test for Modulus {} Multiplier {} Samsize {} Interval {}"
                .format(g.get_modulus(), g.get_multiplier(), samsize, interval))

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
    modulus = 2147483647
    multipliers = [50812] #[50812, 48271, 16807]
    samsize = modulus - 1
    interval = (0.0, 0.001)

    for i in range(len(multipliers)):
        multiplier = multipliers[i]
        generator = MarcianiSingleStream(modulus=modulus, multiplier=multiplier)
        experiment(generator, samsize, interval, DEFAULT_OUTDIR)
