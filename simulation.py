from core.simulations.utils.cli import CmdParser
from core.simulations.cloud.config.configuration import default_configuration
from core.simulations.cloud.simulation import SimpleCloudSimulation as Simulation
import yaml
import os
import logging

# Configure logger
logger = logging.getLogger(__name__)


def configure():
    """
    Configure the simulation environment.
    :return: the configuration path and the environment configuration, as a dictionary
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
        config = default_configuration

    return config_path, config


if __name__ == "__main__":
    from core.simulations.cloud.stats.report import generate_report

    ##
    # CONFIGURATION
    ##
    try:
        config_path, config = configure()
    except Exception as exc:
        logger.error(exc)
        exit(1)

    logger.info("Configuration loaded: %s", config_path)

    logger.debug("Configuration: %s", config)

    ##
    # SIMULATION
    ##
    simulation = Simulation(config)
    simulation.run()

    ##
    # REPORT
    ##
    report = generate_report(simulation)
    logger.info("Report: %s", report)