"""
PERFORMANCE ANALYSIS: Evaluate the system performance, according to settings in 'config.yaml'
Results are stored in 'result.csv' and can be visualized running the Matlab script 'result.m'
"""

from core.simulation.simulation import Simulation as Simulation
from core.simulation.config.configuration import load_configuration
from core.utils.logutils import ConsoleHandler
import logging


# Configure logger
logging.basicConfig(level=logging.INFO, handlers=[ConsoleHandler(logging.INFO)])
logger = logging.getLogger(__name__)

# Configuration
CONFIG_PATH = "config.yaml"

# Results
RESULT_PATH = "out/result.csv"
RESULT_BATCH_PATH = "out/result_{}.csv"
THRESHOLDS = range(1, 21, 1)


if __name__ == "__main__":
    config = config = load_configuration(CONFIG_PATH)

    simulation_counter = 0
    simulation_max = len(THRESHOLDS)

    logger.info("Launching performance analysis with n_batch={}, t_batch={}, i_batch={}, thresholds={}".format(
        config["general"]["n_batch"],
        config["general"]["t_batch"],
        config["general"]["i_batch"],
        THRESHOLDS
    ))

    for threshold in THRESHOLDS:
        simulation_counter += 1
        config["system"]["cloudlet"]["threshold"] = threshold
        logger.info("Simulating {}/{} with threshold {}".format(simulation_counter, simulation_max, threshold))
        simulation = Simulation(config, "SIMULATION-THRESHOLD-{}".format(threshold))
        simulation.run(outfile=RESULT_BATCH_PATH.format(threshold), show_progress=True)
        simulation.generate_report().save_csv(RESULT_PATH, append=(simulation_counter > 1))
