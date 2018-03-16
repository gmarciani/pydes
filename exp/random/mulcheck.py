"""
EXPERIMENT

Find suitable FP, MC, FP/MC multipliers for a multi-stream Lehmer pseudo-random generator.
Input: the modulus, should be prime.
Output: FP, MC, FP/MC multipliers and the best FP/MC multiplier, if exists.

Results (largest FP/MC multiplier):
    * 127 (8 bit modulus): 14
    * 32191 (16 bit modulus): 16095
    * 2147483647 (32 bit modulus):

Notes: results are stored in folder 'out'.
"""
from core.random.inspection import multiplier_check
from core.utils.report import SimpleReport
from os import path
from core.utils.logutils import get_logger

# Logging
logger = get_logger(__name__)


# Parameters (Default)
DEFAULT_MODULUS = 2147483647
DEFAULT_MULTIPLIER = 50812
DEFAULT_OUTDIR = "out/mulcheck"


def experiment(modulus, multiplier, outdir=DEFAULT_OUTDIR):

    filename = path.join(outdir, "mod{}_mul{}".format(modulus, multiplier))

    logger.info("MC Check for Multiplier {} Modulus {}".format(multiplier, modulus))
    is_mcm = multiplier_check.is_mc_multiplier(multiplier, modulus)

    logger.info("FP Check for Multiplier {} Modulus {}".format(multiplier, modulus))
    is_fpm = multiplier_check.is_fp_multiplier(multiplier, modulus)

    logger.info("FP/MC Check for Multiplier {} Modulus {}".format(multiplier, modulus))
    is_fpmcm = is_mcm and is_fpm

    # Report
    r = SimpleReport("MULTIPLIER CHECK")
    r.add("General", "Modulus", modulus)
    r.add("General", "Multiplier", multiplier)
    r.add("Result", "FP", is_fpm)
    r.add("Result", "MC", is_mcm)
    r.add("Result", "FP/MC", is_fpmcm)

    r.save_txt(filename + "_report.txt")

    print(r)


if __name__ == "__main__":
    modulus = 2147483647
    multipliers = [50812, 48271, 16807]

    for multiplier in multipliers:
        experiment(modulus=modulus, multiplier=multiplier, outdir=DEFAULT_OUTDIR)