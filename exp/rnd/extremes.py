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

Notes: results are stored in folder 'out/extremes'.
"""
from os import path

from core.rnd.randomness import extremes as test
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
DEFAULT_SAMSIZE = 10000  # >=  10*BINS
DEFAULT_BINS = 1000  # >= 1000
DEFAULT_D = 5  # >= 2
DEFAULT_CONFIDENCE = 0.95  # >= 0.95
DEFAULT_OUTDIR = "out/extremes"


def run(g, samsize, bins, confidence, d, outdir):

    logger.info(
        "Extremes Test for Modulus {} Multiplier {} Streams {} Jumper {} Bins {} Samsize {} D {} Confidence {}".format(
            g.get_modulus(), g.get_multiplier(), g.get_nstreams(), g.get_jumper(), bins, samsize, d, confidence
        )
    )

    filename = path.join(outdir, "mod{}_mul{}_str{}".format(g.get_modulus(), g.get_multiplier(), g.get_nstreams()))

    # Statistics: [(stream_1, chi_1),(stream_2,chi_2),...,(stream_n,chi_n)]
    data = test.statistics(g, samsize, bins, d)
    save_csv(filename + ".csv", ["stream", "value"], data, empty=True)

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
    r.add("Generator", "Class", g.__class__.__name__)
    r.add("Generator", "Streams", g.get_nstreams())
    r.add("Generator", "Modulus", g.get_modulus())
    r.add("Generator", "Multiplier", g.get_multiplier())
    r.add("Generator", "Jumper", g.get_jumper())
    r.add("Generator", "Seed", g.get_initial_seed())
    r.add("Test Parameters", "Sample Size", samsize)
    r.add("Test Parameters", "Bins", bins)
    r.add("Test Parameters", "Confidence", round(confidence * 100, 3))
    r.add("Test Parameters", "D", d)
    r.add("Critical Bounds", "Lower Bound", mn)
    r.add("Critical Bounds", "Upper Bound", mx)
    r.add("Error", "Theoretical", "{} ({} %)".format(err["err_thr"], round(err["err_thr_perc"] * 100, 3)))
    r.add("Error", "Empirical", "{} ({} %)".format(err["err_emp"], round(err["err_emp_perc"] * 100, 3)))
    r.add("Error", "Empirical Lower Bound", "{} ({} %)".format(err["err_mn"], round(err["err_mn_perc"] * 100, 3)))
    r.add("Error", "Empirical Upper Bound", "{} ({} %)".format(err["err_mx"], round(err["err_mx_perc"] * 100, 3)))
    r.add("Result", "Suggested Confidence", round(sugg_confidence * 100, 3))
    r.add("Result", "Success", success)

    r.save_txt(filename + "_report.txt")
    r.save_csv(filename + "_report.csv")

    logger.info("Report:\n{}".format(r))


if __name__ == "__main__":
    modulus = 2147483647
    multipliers = [50812, 48271, 16807]
    jumpers = [29872, 22925, 62091]
    streams = 256
    bins = 1000
    samsize = 10 * bins
    d = 5
    confidence = 0.95

    for i in range(len(multipliers)):
        multiplier = multipliers[i]
        jumper = jumpers[i]
        generator = MarcianiMultiStream(modulus=modulus, multiplier=multiplier, jumper=jumper, streams=streams)
        run(generator, samsize, bins, confidence, d, DEFAULT_OUTDIR)
