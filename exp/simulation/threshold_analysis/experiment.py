"""
Experiment: Evaluate system performance, according to settings in 'experiment_1.yaml'
Simulate the system model with N=20 and evaluate the system response time and the effective throughput
as a function of the threshold S.
Results are stored in 'experiment_1.csv' and can be viewed as plots running the Matlab script 'experiment_1.m'
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
RESULT_PATH = "result.csv"
THRESHOLDS = range(1, 21, 1)


if __name__ == "__main__":
    from time import sleep
    config = config = load_configuration(CONFIG_PATH)

    simulation_counter = 0
    simulation_max = len(THRESHOLDS)

    header_saved = False
    for threshold in THRESHOLDS:
        simulation_counter += 1
        config["system"]["cloudlet"]["threshold"] = threshold
        logger.info("Simulating {}/{} with threshold {}".format(simulation_counter, simulation_max, threshold))
        sleep(0.1)
        simulation = Simulation(config, "SIMULATION-THRESHOLD-{}".format(threshold))
        simulation.run()
        report = simulation.generate_report()
        report.save_csv(RESULT_PATH, skip_header=header_saved)
        header_saved = True
