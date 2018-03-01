"""
PERFORMANCE ANALYSIS: Evaluate the system performance, according to settings in 'config.yaml'
Results are stored in 'result.csv' and can be visualized running the Matlab script 'result.m'
"""

from core.simulation.simulation import Simulation as Simulation
from core.simulation.config.configuration import load_configuration
from core.utils.logutils import ConsoleHandler
import os
import logging


# Configure logger
logging.basicConfig(level=logging.INFO, handlers=[ConsoleHandler(logging.INFO)])
logger = logging.getLogger(__name__)

# Configuration
CONFIG_PATH = "config.yaml"

# Results
OUTDIR = "out"
RESULT_PATH = "out/result.csv"
RESULT_BATCH_PATH = "out"

# Parameters
THRESHOLDS = range(1, 21, 1)


def run(config_path=CONFIG_PATH):
    """
    Execute the experiment.
    :param config_path: (string) the path of the configuration file.
    :return: None
    """
    config = load_configuration(config_path)

    simulation_counter = 0
    simulation_max = len(THRESHOLDS)

    logger.info("Launching performance analysis with t_stop={}, t_tran={}, n_batch={}, thresholds={}".format(
        config["general"]["t_stop"],
        config["general"]["t_tran"],
        config["general"]["n_batch"],
        THRESHOLDS
    ))

    for threshold in THRESHOLDS:
        simulation_counter += 1
        config["system"]["cloudlet"]["threshold"] = threshold
        logger.info("Simulating {}/{} with threshold {}".format(simulation_counter, simulation_max, threshold))
        outdir = "{}/{}".format(OUTDIR, threshold)
        simulation = Simulation(config, "SIMULATION-THRESHOLD-{}".format(threshold))
        simulation.run(outdir=outdir, show_progress=True)
        reportfile = os.path.join(outdir, "result.csv")
        simulation.generate_report().save_csv(reportfile, append=(simulation_counter > 1))


if __name__ == "__main__":
    run()