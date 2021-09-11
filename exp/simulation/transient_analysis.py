"""
TRANSIENT ANALYSIS: Evaluate the system transient phase, according to settings in 'config.yaml'
Results are stored in 'result.csv' and can be visualized running the Matlab script 'pmcsn.mlx'
"""

from core.simulation.simulation import Simulation as Simulation
from core.simulation.model.config import load_configuration
from core.utils.dictutils import merge
import logging


# Logging
logger = logging.getLogger(__name__)

# Defaults
DEFAULT_CONFIG_PATH = "transient_analysis.yaml"
DEFAULT_OUTDIR = "out/transient_analysis"
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

    logger.info("Launching transient analysis with configuration:\n{}".format(config))

    replications = config["general"]["replications"]
    seed = config["general"]["random"]["seed"]

    for replication in range(0, replications):
        config["general"]["random"]["seed"] = seed
        outdir_replica = "{}/seed_{}".format(outdir, seed)
        logger.info("Launching replication {}/{} with seed {}".format(replication + 1, replications, seed))
        simulation = Simulation(config, "SIMULATION-TRANSIENT-ANALYSIS")
        simulation.run(outdir=outdir_replica, show_progress=True)
        seed = simulation.rndgen.get_seed()


if __name__ == "__main__":
    config_path = DEFAULT_CONFIG_PATH
    outdir = DEFAULT_OUTDIR
    parameters = DEFAULT_PARAMETERS

    run(config_path, outdir, parameters)
