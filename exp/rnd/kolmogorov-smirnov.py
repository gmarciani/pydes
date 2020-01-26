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

Results:
    * (2147483647, 16807): not good
    * (2147483647, 48271): good
    * (2147483647, 50812): good

Notes: results are stored in folder 'out' and can be visualized by running the Matlab script 'kolmogorov-smirnov.m'.
"""
from core.rnd.rndgen import MarcianiMultiStream
from core.rnd.randomness import kolmogorov_smirnov as test
from core.rnd.randomness import extremes
from core.utils.report import SimpleReport
from core.utils.csv_utils import save_csv
from os import path
from core.utils.logutils import get_logger

# Logging
logger = get_logger(__name__)

# Parameters (Default)
DEFAULT_OUTDIR = "out/kolmogorov-smirnov"


def experiment(g, test_name, test_params, outdir=DEFAULT_OUTDIR):

    logger.info("Kolmogorov-Smirnov Test ({}) for Modulus {} Multiplier {} Streams {} Jumper {}".
                format(tst, g.get_modulus(), g.get_multiplier(), g.get_nstreams(), g.get_jumper()))

    filename = path.join(outdir, "mod{}_mul{}"
                         .format(g.get_modulus(), g.get_multiplier(), g.get_nstreams(), g.get_jumper()))

    if test_name is "uniformity_u":
        raise NotImplementedError("Kolmogorov-Smirnov on {} is not yet implemented".format(test_name))
        #data = uniformity_univariate.statistics(generator, streams, samsize, bins)
    elif test_name is "uniformity_b":
        raise NotImplementedError("Kolmogorov-Smirnov on {} is not yet implemented".format(test_name))
        #data = uniformity_bivariate.statistics(generator, streams, samsize, bins)
    elif test_name is "extremes":
        chi_square_statistics = extremes.statistics(g, test_params["samsize"], test_params["bins"], test_params["d"])
    elif test_name is "runsup":
        raise NotImplementedError("Kolmogorov-Smirnov on {} is not yet implemented".format(test_name))
        #data = runsup.statistics(generator, streams, samsize, bins)
    elif test_name is "gap":
        raise NotImplementedError("Kolmogorov-Smirnov on {} is not yet implemented".format(test_name))
        #data = gap.statistics(generator, streams, samsize, bins, test_params["a"], test_params["b"])
    elif test_name is "permutation":
        raise NotImplementedError("Kolmogorov-Smirnov on {} is not yet implemented".format(test_name))
        #data = permutation.statistics(generator, streams, samsize, bins, test_params["t"])
    else:
        raise ValueError("{} is not a valid testname".format(test_name))

    save_csv(filename + ".csv", ["stream", "value"], chi_square_statistics, empty=True)

    # KS Statistic
    ks_distances = test.compute_ks_distances(chi_square_statistics, test_params["bins"])
    ks_statistic = test.compute_ks_statistic(ks_distances)
    ks_point = test.compute_ks_point(ks_distances)

    # KS Critical
    ks_critical_distance = test.compute_ks_critical_distance(streams, test_params["confidence"])

    # Result
    success = ks_statistic < ks_critical_distance

    # Report
    r = SimpleReport("TEST OF KOLMOGOROV-SMIRNOV")
    r.add("Generator", "Class", g.__class__.__name__)
    r.add("Generator", "Streams", g.get_nstreams())
    r.add("Generator", "Modulus", g.get_modulus())
    r.add("Generator", "Multiplier", g.get_multiplier())
    r.add("Generator", "Seed", g.get_initial_seed())
    r.add("Test Parameters", "ChiSquare Test", test_name)
    r.add("Test Parameters", "Sample Size", test_params["samsize"])
    r.add("Test Parameters", "Bins", test_params["bins"])
    r.add("Test Parameters", "Confidence", round(test_params["confidence"] * 100, 3))
    if test_name is "extremes":
        r.add("Test Parameters", "D", test_params["d"])
    elif test_name is "gap":
        r.add("Test Parameters", "A", test_params["a"])
        r.add("Test Parameters", "B", test_params["b"])
    elif test_name is "permutation":
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
        #("uniformity_u", dict(samsize=10000, bins=1000, confidence=0.95)),
        #("uniformity_b", dict(samsize=100000, bins=100, confidence=0.95)),
        "extremes": dict(samsize=10000, bins=1000, confidence=0.95, d=5),
        #("runsup", dict(samsize=14400, bins=6, confidence=0.95)),
        #("gap", dict(samsize=10000, bins=78, confidence=0.95, a=0.94, b=0.99)),
        #("permutation", dict(samsize=7200, bins=720, confidence=0.95, t=6))
    }

    for i in range(len(multipliers)):
        for tst, tst_params in tests.items():
            multiplier = multipliers[i]
            jumper = jumpers[i]
            generator = MarcianiMultiStream(modulus=modulus, multiplier=multiplier, jumper=jumper, streams=streams)
            experiment(generator, tst, tst_params, path.join(DEFAULT_OUTDIR, tst))