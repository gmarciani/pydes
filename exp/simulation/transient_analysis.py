"""
TRANSIENT ANALYSIS: Evaluate the system transient phase, according to settings in 'config.yaml'
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
CONFIG_PATH = "transient_analysis.yaml"

# Results
OUTDIR = "out/transient_analysis"

# Parameters
REPLICATIONS = 5


def run(config_path=CONFIG_PATH, replications=REPLICATIONS):
    """
    Execute the experiment.
    :param config_path: (string) the path of the configuration file.
    :param replications: (int) the number of replications.
    :return: None
    """

    config = load_configuration(config_path)

    logger.info("Launching transient analysis with t_stop={}".format(config["general"]["t_stop"]))

    seed = 123456789

    for replication in range(0, replications):
        config["general"]["random"]["seed"] = seed
        logger.info("Launching replication {}/{} with seed {}".format(replication+1, replications, seed))
        outdir = "{}/seed_{}".format(OUTDIR, seed)
        simulation = Simulation(config, "SIMULATION-TRANSIENT-ANALYSIS")
        simulation.run(outdir=outdir, show_progress=True)
        seed = simulation.rndgen.get_seed()


if __name__ == "__main__":
    run()