"""
EXPERIMENT

Find a suitable jumper for a multi-stream Lehmer pseudo-random generator.
Input: the modulus, should be prime.
Input: the multiplier, should be a FP/MC multiplier w.r.t. the modulus.
Input: the number of stream.
Output: the list of suitable jumpers, if exist.

Results (best jumper and jump size):
    * 127 (8 bit modulus) | 14 (FP/MC multiplier): (jsize: )
    * 32191 (16 bit modulus) | 16095 (FP/MC multiplier): (jsize: )
    * 2147483647 (32 bit modulus) | (FP/MC multiplier): (jsize: )

Notes: results are stored in folder 'out'.
"""
from core.random.inspection import jumper_finder
from core.utils.report import SimpleReport
from os import path
from core.utils.file_utils import save_list_of_pairs
from core.utils.logutils import get_logger

# Logging
logger = get_logger(__name__)

# Parameters (Default)
DEFAULT_MODULUS = 2147483647
DEFAULT_MULTIPLIER = 16807  # [16807, 48271, 50812]
DEFAULT_STREAMS = 256
DEFAULT_OUTDIR = "out"


def experiment(modulus, multiplier, streams, outdir=DEFAULT_OUTDIR):

    logger.info("Computing Jumpers for Modulus {} Multiplier {} Streams {}".format(modulus, multiplier, streams))

    filename = path.join(outdir, "mod{}_mul{}_str{}".format(modulus, multiplier, streams))

    jumpers = jumper_finder.find_jumpers(modulus, multiplier, streams)

    jmax = max(jumpers, key=lambda item:item[1])

    # Save raw data
    save_list_of_pairs(filename + ".csv", jumpers)

    # Report
    r = SimpleReport("JUMPER")
    r.add("General", "Modulus", modulus)
    r.add("General", "Multiplier", multiplier)
    r.add("General", "Streams", streams)
    r.add("Result", "Jumpers", len(jumpers))
    r.add("Result", "Best Jumper", jmax[0])
    r.add("Result", "Best Jump Size", jmax[1])

    r.save_txt(filename + "_report.txt")

    print(r)


if __name__ == "__main__":
    modulus = 2147483647
    multipliers = [50812, 48271, 16087]
    nstreams = [256]

    for multiplier in multipliers:
        for streams in nstreams:
            experiment(modulus=modulus, multiplier=multiplier, streams=streams, outdir=DEFAULT_OUTDIR)