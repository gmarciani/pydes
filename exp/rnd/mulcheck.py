"""
EXPERIMENT

Check FP, MC, FP/MC constraints for multipliers for a multi-stream Lehmer pseudo-random generator.
Input: the modulus, should be prime, and the multiplier.
Output: FP, MC, FP/MC multipliers and the best FP/MC multiplier, if exists.

Notes: results are stored in folder 'out/mulcheck'.
"""
from os import path

from core.rnd.inspection import multiplier_check
from core.utils.logutils import get_logger
from core.utils.report import SimpleReport

# Logging
logger = get_logger(__name__)

# Defaults
DEFAULT_MODULUS = 2147483647
DEFAULT_MULTIPLIER = 50812
DEFAULT_OUTDIR = "out/mulcheck"


def run(modulus, multiplier, outdir=DEFAULT_OUTDIR):

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
        run(modulus=modulus, multiplier=multiplier, outdir=DEFAULT_OUTDIR)
