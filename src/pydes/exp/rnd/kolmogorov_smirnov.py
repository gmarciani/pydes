"""
EXPERIMENTS

Kolmogorov-Smirnov Test of Randomness.

Input:
    * the multi-stream pseudo-rnd number generator, characterized by its modulus and multiplier.
    * the sample size (should be >= 10 * bins).
    * the number of bins (should be >= 1000).
    * the power (should be >= 2).
    * the confidence level (should be >= 0.95).

Output: the extreme behaviour of the generator for each of its stream.

Notes: results are stored in folder 'out/kolmogorov-smirnov'.
"""
from os import path

from core.rnd.randomness import extremes
from core.rnd.randomness import kolmogorov_smirnov as test
from core.rnd.rndgen import MarcianiMultiStream
from core.utils.csv_utils import save_csv
from core.utils.logutils import get_logger
from core.utils.report import SimpleReport

# Logging
logger = get_logger(__name__)

# Defaults
DEFAULT_MODULUS = 2147483647
DEFAULT_MULTIPLIER = 50812
DEFAULT_STREAMS = 256
DEFAULT_JUMPER = 29872
DEFAULT_GENERATOR = MarcianiMultiStream(
    modulus=DEFAULT_MODULUS, multiplier=DEFAULT_MULTIPLIER, jumper=DEFAULT_JUMPER, streams=DEFAULT_STREAMS
)
DEFAULT_TEST = "extremes"
DEFAULT_TEST_PARAMS = dict(samsize=10000, bins=1000, confidence=0.95, d=5)
DEFAULT_OUTDIR = "out/kolmogorov-smirnov"
SUPPORTED_TESTS = "extremes"


def run(g, test_name, test_params, outdir=DEFAULT_OUTDIR):

    logger.info(
        "Kolmogorov-Smirnov Test ({}) for Modulus {} Multiplier {} Streams {} Jumper {}".format(
            test_name, g.get_modulus(), g.get_multiplier(), g.get_nstreams(), g.get_jumper()
        )
    )

    filename = path.join(outdir, "mod{}_mul{}_str{}".format(g.get_modulus(), g.get_multiplier(), g.get_nstreams()))

    if test_name == "uniformity_u":
        raise NotImplementedError("Kolmogorov-Smirnov on {} is not yet implemented".format(test_name))
        # data = uniformity_univariate.statistics(generator, streams, samsize, bins)
    elif test_name == "uniformity_b":
        raise NotImplementedError("Kolmogorov-Smirnov on {} is not yet implemented".format(test_name))
        # data = uniformity_bivariate.statistics(generator, streams, samsize, bins)
    elif test_name == "extremes":
        chi_square_statistics = extremes.statistics(g, test_params["samsize"], test_params["bins"], test_params["d"])
    elif test_name == "runsup":
        raise NotImplementedError("Kolmogorov-Smirnov on {} is not yet implemented".format(test_name))
        # data = runsup.statistics(generator, streams, samsize, bins)
    elif test_name == "gap":
        raise NotImplementedError("Kolmogorov-Smirnov on {} is not yet implemented".format(test_name))
        # data = gap.statistics(generator, streams, samsize, bins, test_params["a"], test_params["b"])
    elif test_name == "permutation":
        raise NotImplementedError("Kolmogorov-Smirnov on {} is not yet implemented".format(test_name))
        # data = permutation.statistics(generator, streams, samsize, bins, test_params["t"])
    else:
        raise ValueError("{} is not a valid testname".format(test_name))

    save_csv(filename + ".csv", ["stream", "value"], chi_square_statistics, empty=True)

    # KS Statistic
    ks_distances = test.compute_ks_distances(chi_square_statistics, test_params["bins"])
    ks_statistic = test.compute_ks_statistic(ks_distances)
    ks_point = test.compute_ks_point(ks_distances)

    # KS Critical
    ks_critical_distance = test.compute_ks_critical_distance(g.get_nstreams(), test_params["confidence"])

    # Result
    success = ks_statistic < ks_critical_distance

    # Report
    r = SimpleReport("TEST OF KOLMOGOROV-SMIRNOV")
    r.add("Generator", "Class", g.__class__.__name__)
    r.add("Generator", "Streams", g.get_nstreams())
    r.add("Generator", "Modulus", g.get_modulus())
    r.add("Generator", "Multiplier", g.get_multiplier())
    r.add("Generator", "Jumper", g.get_jumper())
    r.add("Generator", "Seed", g.get_initial_seed())
    r.add("Test Parameters", "ChiSquare Test", test_name)
    r.add("Test Parameters", "Sample Size", test_params["samsize"])
    r.add("Test Parameters", "Bins", test_params["bins"])
    r.add("Test Parameters", "Confidence", round(test_params["confidence"] * 100, 3))
    if test_name == "extremes":
        r.add("Test Parameters", "D", test_params["d"])
    elif test_name == "gap":
        r.add("Test Parameters", "A", test_params["a"])
        r.add("Test Parameters", "B", test_params["b"])
    elif test_name == "permutation":
        r.add("Test Parameters", "T", test_params["t"])
    r.add("KS", "KS Statistic", round(ks_statistic, 3))
    r.add("KS", "KS Point X", round(ks_point, 3))
    r.add("KS", "KS Critical Distance", round(ks_critical_distance, 3))
    r.add("Result", "Success", success)

    r.save_txt(filename + "_report.txt")
    r.save_csv(filename + "_report.csv")

    logger.info("Report:\n{}".format(r))


if __name__ == "__main__":
    # Generator
    modulus = 2147483647
    multipliers = [50812, 48271, 16807]
    jumpers = [29872, 22925, 62091]
    streams = 256

    tests = {
        # ("uniformity_u", dict(samsize=10000, bins=1000, confidence=0.95)),
        # ("uniformity_b", dict(samsize=100000, bins=100, confidence=0.95)),
        "extremes": dict(samsize=10000, bins=1000, confidence=0.95, d=5),
        # ("runsup", dict(samsize=14400, bins=6, confidence=0.95)),
        # ("gap", dict(samsize=10000, bins=78, confidence=0.95, a=0.94, b=0.99)),
        # ("permutation", dict(samsize=7200, bins=720, confidence=0.95, t=6))
    }

    for i in range(len(multipliers)):
        for tst, tst_params in tests.items():
            multiplier = multipliers[i]
            jumper = jumpers[i]
            generator = MarcianiMultiStream(modulus=modulus, multiplier=multiplier, jumper=jumper, streams=streams)
            run(generator, tst, tst_params, path.join(DEFAULT_OUTDIR, tst))
