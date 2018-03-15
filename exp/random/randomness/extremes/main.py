"""
EXPERIMENT

Extremes Test of Randomness.

Input: 
    * the multi-stream pseudo-random number generator, characterized by its modulus and multiplier.
    * the sample size (should be >= 10 * bins).
    * the number of bins (should be >= 1000).
    * the power (should be >= 2).
    * the confidence level (should be >= 0.95).

Output: the extreme behaviour of the generator for each of its stream.

Results:
    * (2147483647, 16807): not good
    * (2147483647, 48271): good
    * (2147483647, 50812): good

Notes: results are stored in folder 'out' and can be visualized by running the Matlab script 'extremes.m'.
"""
from core.random.rndgen import MarcianiMultiStream
from core.random.randomness import extremes as test
from core.utils.report import SimpleReport
from core.utils.file_utils import save_list_of_pairs
from os import path
from core.utils.logutils import ConsoleHandler
import logging

# Configure logger
logging.basicConfig(level=logging.INFO, handlers=[ConsoleHandler(logging.INFO)])
logger = logging.getLogger(__name__)

# Generator
DEFAULT_GENERATOR = MarcianiMultiStream()

# Test Parameters
DEFAULT_SAMSIZE = 10000  # >=  10*BINS
DEFAULT_BINS = 1000  # >= 1000
DEFAULT_D = 5  # >= 2
DEFAULT_CONFIDENCE = 0.95  # >= 0.95

# Directory for results
DEFAULT_OUTDIR = "out"


def experiment(generator, samsize, bins, confidence, d, outdir):

    filename = path.join(outdir, "extremes_sms{}_d{}".format(samsize, d))

    # Statistics: [(stream_1, chi_1),(stream_2,chi_2),...,(stream_n,chi_n)]
    data = test.statistics(generator, samsize, bins, d)
    save_list_of_pairs(filename + ".csv", data)

    # Critical Bounds
    mn = test.critical_min(bins, confidence)
    mx = test.critical_max(bins, confidence)

    # Theoretical/Empirical Error
    err = test.error(data, mn, mx, confidence)

    # Result
    success = err["err_emp"] <= err["err_thr"]
    sugg_confidence = 1 - err["err_emp_perc"]

    # Report
    r = SimpleReport("TEST OF EXTREMES")
    r.add("Generator", "Class", generator.__class__.__name__)
    r.add("Generator", "Streams", generator._streams)
    r.add("Generator", "Modulus", generator._modulus)
    r.add("Generator", "Multiplier", generator._multiplier)
    r.add("Generator", "Seed", generator._iseed)
    r.add("Test Parameters", "Sample Size", samsize)
    r.add("Test Parameters", "Bins", bins)
    r.add("Test Parameters", "Confidence", round(confidence * 100, 3))
    r.add("Test Parameters", "D", d)
    r.add("Critical Bounds", "Lower Bound", mn)
    r.add("Critical Bounds", "Upper Bound", mx)
    r.add("Error", "Theoretical",
          "{} ({} %)".format(err["err_thr"], round(err["err_thr_perc"] * 100, 3)))
    r.add("Error", "Empirical",
          "{} ({} %)".format(err["err_emp"], round(err["err_emp_perc"] * 100, 3)))
    r.add("Error", "Empirical Lower Bound",
          "{} ({} %)".format(err["err_mn"], round(err["err_mn_perc"] * 100, 3)))
    r.add("Error", "Empirical Upper Bound",
          "{} ({} %)".format(err["err_mx"], round(err["err_mx_perc"] * 100, 3)))
    r.add("Result", "Suggested Confidence", round(sugg_confidence * 100, 3))
    r.add("Result", "Success", success)

    r.save_txt(filename + "_report.txt")
    r.save_csv(filename + "_report.csv")

    print(r)


if __name__ == "__main__":
    modulus = 2147483647
    multipliers = [50812]  #[50812, 48271, 16807]
    jumpers = [29872]
    streams = 256
    bins = 1000
    samsize = 10 * bins
    d = 5
    confidence = 0.95

    for i in range(len(multipliers)):
        multiplier = multipliers[i]
        jumper = jumpers[i]
        logger.info("Extremes Test for multiplier {}".format(multiplier))
        generator = MarcianiMultiStream(modulus=modulus, multiplier=multiplier, jumper=jumper, streams=256)
        outdir = path.join("out", "mod{}_mul{}_str{}".format(modulus, multiplier, streams))
        experiment(generator, samsize, bins, confidence, d, outdir)