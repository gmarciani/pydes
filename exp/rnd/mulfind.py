"""
EXPERIMENT

Find suitable FP, MC, FP/MC multipliers for a multi-stream Lehmer pseudo-random generator.
Input: the modulus, should be prime.
Output: FP, MC, FP/MC multipliers and the smallest/largest FP/MC multiplier, if exists.

Notes: results are stored in folder 'out/mulfind'.
"""
from core.rnd.inspection import multiplier_check
from core.utils.report import SimpleReport
from core.utils.file_utils import save_list_of_numbers
from os import path
from core.utils.logutils import ConsoleHandler
from core.utils.logutils import get_logger

# Logging
logger = get_logger(__name__)

# Defaults
DEFAULT_MODULUS = 2147483647
DEFAULT_OUTDIR = "out/mulfind"


def run(modulus, outdir=DEFAULT_OUTDIR):

    filename = path.join(outdir, "mod{}".format(modulus))

    logger.info("Computing MC Multipliers for Modulus {}".format(modulus))
    mc_multipliers = multiplier_check.get_mc_multipliers(modulus)

    logger.info("Computing FP Multipliers for Modulus {}".format(modulus))
    fp_multipliers = multiplier_check.get_fp_multipliers(modulus)

    logger.info("Computing FP/MC Multipliers for Modulus {}".format(modulus))
    fpmc_multipliers = []
    for candidate in fp_multipliers:
        if candidate in mc_multipliers:
            fpmc_multipliers.append(candidate)

    logger.info("Computing smallest/largest FP/MC Multipliers for Modulus {}".format(modulus))
    smallest_fpmc_multiplier = min(fpmc_multipliers, default=None)
    largest_fpmc_multiplier = max(fpmc_multipliers, default=None)

    # Save raw data
    save_list_of_numbers(filename + "_mc.txt", mc_multipliers)
    save_list_of_numbers(filename + "_fp.txt", fp_multipliers)
    save_list_of_numbers(filename + "_fpmc.txt", fpmc_multipliers)

    # Report
    r = SimpleReport("MULTIPLIERS")
    r.add("General", "Modulus", modulus)
    r.add("Multipliers", "FP", len(fp_multipliers))
    r.add("Multipliers", "MC", len(mc_multipliers))
    r.add("Multipliers", "FP/MC", len(fpmc_multipliers))
    r.add("Multipliers (%)", "FP", round(100 * len(fp_multipliers) / (modulus - 1), 3))
    r.add("Multipliers (%)", "MC", round(100 * len(mc_multipliers) / (modulus - 1), 3))
    r.add("Multipliers (%)", "FP/MC", round(100 * len(fpmc_multipliers) / (modulus - 1), 3))
    r.add("Result", "Smallest FP/MC Multiplier", smallest_fpmc_multiplier)
    r.add("Result", "Largest FP/MC Multiplier", largest_fpmc_multiplier)

    r.save_txt(filename + "_report.txt")

    print(r)


if __name__ == "__main__":
    moduli = [401, 2147483647]

    for modulus in moduli:
        run(modulus=modulus, outdir=DEFAULT_OUTDIR)
