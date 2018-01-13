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
from core.utils.file_utils import save_list_of_numbers
from os import path


DEFAULT_MODULUS = 2147483647


def experiment(modulus):
    print("Computing MC Multipliers")
    mc_multipliers = multiplier_check.get_mc_multipliers(modulus)

    print("Computing FP Multipliers")
    fp_multipliers = multiplier_check.get_fp_multipliers(modulus)

    print("Computing FP/MC Multipliers")
    fpmc_multipliers = []
    for candidate in fp_multipliers:
        if candidate in mc_multipliers:
            fpmc_multipliers.append(candidate)

    print("Computing largest FP/MC Multiplier")
    largest_fpmc_multiplier = max(fpmc_multipliers, default=None)

    # Save raw data
    save_list_of_numbers(path.join("out", "multiplier_fp_{}.txt".format(modulus)), mc_multipliers)
    save_list_of_numbers(path.join("out", "multiplier_mc_{}.txt".format(modulus)), fp_multipliers)
    save_list_of_numbers(path.join("out", "multiplier_fpmc_{}.txt".format(modulus)), fpmc_multipliers)

    # Report
    r = SimpleReport("MULTIPLIERS")
    r.add("General", "Modulus", modulus)
    r.add("Multipliers", "FP", len(fp_multipliers))
    r.add("Multipliers", "MC", len(mc_multipliers))
    r.add("Multipliers", "FP/MC", len(fpmc_multipliers))
    r.add("Multipliers (%)", "FP", round(100 * len(fp_multipliers) / (modulus - 1), 3))
    r.add("Multipliers (%)", "MC", round(100 * len(mc_multipliers) / (modulus - 1), 3))
    r.add("Multipliers (%)", "FP/MC", round(100 * len(fpmc_multipliers) / (modulus - 1), 3))
    r.add("Result", "Largest FP/MC Multiplier", largest_fpmc_multiplier)

    r.save(path.join("out", "multiplier_{}.txt".format(modulus)))

    print(r)


if __name__ == "__main__":
    experiment(401)