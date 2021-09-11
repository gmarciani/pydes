"""
VALIDATION: Evaluate the delta between the analytical result and the simulation one.
"""

from core.simulation import result_validator, result_printer
import logging
import os


# Logging
logger = logging.getLogger(__name__)

# Defaults
DEFAULT_ANALYTICAL_RESULT_PATH = "analytical_result.csv"
DEFAULT_SIMULATION_RESULT_PATH = "simulation_result.csv"
DEFAULT_OUTDIR = "out/validation"


def run(analytical_result_path, simulation_result_path, outdir=DEFAULT_OUTDIR):
    """
    Execute the experiment.
    :param analytical_result_path: (string) the path of the analytical result file.
    :param simulation_result_path: (string) the path of the simulation result file.
    :param outdir: (string) the path of the output directory.
    :return: None
    """

    logger.info(
        "Launching validation with configuration:\n{}".format(analytical_result_path, simulation_result_path, outdir)
    )

    report = result_validator.validate(analytical_result_path, simulation_result_path)

    report.save_txt(os.path.join(outdir, "result.txt"), append=False, empty=True)
    report.save_csv(os.path.join(outdir, "result.csv"), append=False, empty=True)

    print(report)

    latex_table = result_printer.build_latex_table(analytical_result_path, simulation_result_path)

    print(latex_table)


if __name__ == "__main__":
    analytical_result_path = DEFAULT_ANALYTICAL_RESULT_PATH
    simulation_result_path = DEFAULT_SIMULATION_RESULT_PATH
    outdir = DEFAULT_OUTDIR

    run(analytical_result_path, simulation_result_path, outdir)
