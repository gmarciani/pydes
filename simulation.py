from core.simulations.common.cli import CmdParser
from core.simulations.cloud.config.configuration import get_default_configuration
from core.simulations.cloud.simulation import SimpleCloudSimulation as Simulation
import yaml
import os
import logging

# Configure logger
logger = logging.getLogger(__name__)


def configure():
    """
    Configure the simulation environment.
    :return: (cp, c, r), where *c* is the configuration path, *c* the environment configuration, as a dictionary and
    *r* is the number of replications.
    """
    args = CmdParser().parse_args()

    log_level = args.log or "INFO"

    logging.basicConfig(level=logging._nameToLevel[log_level])

    config_path = args.config or "simulation.yaml"

    if os.path.exists(config_path):
        with open(config_path, "r") as config_file:
            config = yaml.load(config_file)
    else:
        config_path = "default"
        config = get_default_configuration()

    replications = args.replications or 1

    return config_path, config, int(replications)


if __name__ == "__main__":
    from core.simulations.cloud.statistics.report import generate_report

    ##
    # CONFIGURATION
    ##
    try:
        config_path, config, replications = configure()
    except Exception as exc:
        logger.error(exc)
        exit(1)

    logger.info("Configuration loaded: %s", config_path)

    logger.debug("Configuration: %s", config)

    ##
    # SIMULATION
    ##
    for replication in range(replications):
        config["general"]["random"]["seed"] += replication
        logger.info("Initializing simulation (replication {} out of {})".format(replication+1, replications))
        simulation = Simulation(config)
        simulation.run()
        report = generate_report(simulation)
        logger.info("Report: %s", report)