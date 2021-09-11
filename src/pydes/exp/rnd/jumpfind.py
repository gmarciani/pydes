"""
EXPERIMENT

Find a suitable jumper for a multi-stream Lehmer pseudo-random generator.
Input: the modulus, should be prime.
Input: the multiplier, should be a FP/MC multiplier w.r.t. the modulus.
Input: the number of stream.
Output: the list of suitable jumpers, if exist.

Notes: results are stored in folder 'out/jumpfind'.
"""
from os import path

from pydes.core.rnd.inspection import jumper_finder
from pydes.core.utils.file_utils import save_list_of_pairs
from pydes.core.utils.logutils import get_logger
from pydes.core.utils.report import SimpleReport

# Logging
logger = get_logger(__name__)

# Defaults
DEFAULT_MODULUS = 2147483647
DEFAULT_MULTIPLIER = 50812
DEFAULT_STREAMS = 256
DEFAULT_OUTDIR = "out/jumpfind"


def run(modulus, multiplier, streams, outdir=DEFAULT_OUTDIR):

    logger.info("Computing Jumpers for Modulus {} Multiplier {} Streams {}".format(modulus, multiplier, streams))

    filename = path.join(outdir, "mod{}_mul{}_str{}".format(modulus, multiplier, streams))

    jumpers = jumper_finder.find_jumpers(modulus, multiplier, streams)

    jmax = max(jumpers, key=lambda item: item[1])

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
            run(modulus=modulus, multiplier=multiplier, streams=streams, outdir=DEFAULT_OUTDIR)
