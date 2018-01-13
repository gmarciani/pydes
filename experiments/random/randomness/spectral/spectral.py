"""
Experiment: Spectral Test of Randomness.
"""

from core.random.rndgen import MarcianiMultiStream as RandomGenerator
from core.random.randomness import spectral as test
from core.utils.report import SimpleReport
from core.utils.file_utils import save_list_of_pairs
from os import path

# Generator
DEFAULT_GENERATOR = RandomGenerator()

# Test Parameters
DEFAULT_SAMSIZE = 100000

# Results directory
DEFAULT_OUTDIR = "out"


def experiment(generator, samsize, outdir):

    filename = path.join(outdir, "spectral_{}_{}_{}".format(generator.__class__.__name__, generator.get_initial_seed(), samsize))

    # Observations: [(u1, u2)]
    data = test.observations(DEFAULT_GENERATOR.rnd, DEFAULT_SAMSIZE)

    # Save raw data
    save_list_of_pairs(filename + "csv", data)

    # Report
    r = SimpleReport("SPECTRAL TEST")
    r.add("Generator", "Class", generator.__class__.__name__)
    r.add("Generator", "Seed", generator.get_initial_seed())
    r.add("Test Parameters", "Sample Size", samsize)

    r.save(filename + ".txt")

    print(r)

    # Plot
    #fig_filename = "{}.{}".format(filename, PLT_EXT)
    #test.plot(data, filename=fig_filename)

    # Plot (with zoom)
    #fig_filename = "{}-zoom.{}".format(filename, PLT_EXT)
    #test.plot(data, filename=fig_filename, zoom=(0.5, 0.6))


if __name__ == "__main__":
    experiment(DEFAULT_GENERATOR, DEFAULT_SAMSIZE, DEFAULT_OUTDIR)
