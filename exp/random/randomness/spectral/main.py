"""
EXPERIMENT

Spectral Test of Randomness.

Input:
    * the pseudo-random number generator, characterized by its modulus and multiplier.
    * the sample size.
    * the interval [a,b].
    
Output: the distribution of random number within the specified interval.

Notes: results are stored in folder 'out' and can be visualized by running the Matlab script 'spectral.m'.

Results:
    * (2147483647, 16807): not good
    * (2147483647, 48271): good
    * (2147483647, 50812): good
"""
from core.random.rndgen import MarcianiSingleStream
from core.random.randomness import spectral as test
from core.utils.report import SimpleReport
from os import path


# Generator
DEFAULT_GENERATOR = MarcianiSingleStream()

# Sample size
DEFAULT_SAMSIZE = 100000

# Zoom interval
DEFAULT_INTERVAL = (0.0, 1.0)

# Directory for results
DEFAULT_OUTDIR = "out"


def experiment(generator, samsize, interval, outdir):

    filename = path.join(outdir, "spectral_{}".format(samsize))

    # Statistics: [(u1, u2),(u2,u3)...,(un-1,un)]
    test.statistics(filename + ".csv", generator, samsize, interval)

    # Report
    r = SimpleReport("SPECTRAL TEST")
    r.add("Generator", "Class", generator.__class__.__name__)
    r.add("Generator", "Modulus", generator._modulus)
    r.add("Generator", "Multiplier", generator._multiplier)
    r.add("Generator", "Seed", generator._iseed)
    r.add("Test Parameters", "Sample Size", samsize)
    r.add("Test Parameters", "Interval", interval)

    r.save(filename + "_report.txt")
    r.save_csv(filename + "_report.csv")

    print(r)


if __name__ == "__main__":
    modulus = 2147483647
    multipliers = [16807, 48271, 50812]
    samsize = modulus - 1
    interval = (0.0, 0.001)

    for i in range(len(multipliers)):
        multiplier = multipliers[i]
        print("Spectral Test: {}".format(multiplier))
        generator = MarcianiSingleStream(modulus=modulus, multiplier=multiplier)
        outdir = path.join(DEFAULT_OUTDIR, "mod{}_mul{}".format(modulus, multiplier))
        experiment(generator, samsize, interval, outdir)
