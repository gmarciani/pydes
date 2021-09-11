"""
PERFORMANCE ANALYSIS: Evaluate the system performance, according to settings in 'config.yaml'
Results are stored in 'result.csv' and can be visualized running the Matlab script 'result.m'
"""

import logging
import os

from pydes.core.simulation.model.config import load_configuration
from pydes.core.simulation.simulation import Simulation as Simulation
from pydes.core.utils.dictutils import merge

# Logging
logger = logging.getLogger(__name__)

# Defaults
DEFAULT_CONFIG_PATH = "performance_analysis.yaml"
DEFAULT_OUTDIR = "out/performance_analysis"
DEFAULT_PARAMETERS = {}


def run(config_path=DEFAULT_CONFIG_PATH, outdir=DEFAULT_OUTDIR, parameters=DEFAULT_PARAMETERS):
    """
    Execute the experiment.
    :param config_path: (string) the path of the configuration file.
    :param outdir: (string) the path of the output directory.
    :param parameters: (dict) parameters to overwrite.
    :return: None
    """

    config = merge(load_configuration(config_path), parameters)

    logger.info("Launching performance analysis with configuration:\n{}".format(config))

    simulation = Simulation(config)
    simulation.run(outdir=outdir, show_progress=True)
    reportfilecsv = os.path.join(outdir, "result.csv")
    reportfiletxt = os.path.join(outdir, "result.txt")
    report = simulation.generate_report()
    report.save_txt(reportfiletxt, append=False, empty=True)
    report.save_csv(reportfilecsv, append=False, empty=True)


if __name__ == "__main__":
    config_path = DEFAULT_CONFIG_PATH
    outdir = DEFAULT_OUTDIR
    parameters = DEFAULT_PARAMETERS

    run(config_path, outdir, parameters)
