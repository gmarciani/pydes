"""
Experiment: Evaluate system performance, according to settings in 'experiment_1.yaml'
Results are stored in 'experiment_1.csv' and can be viewed as plots running the Matlab script 'experiment_1.m'
"""


from core.simulations.cloud.simulation import SimpleCloudSimulation as Simulation
import yaml

import os
import logging

# Configure logger
logger = logging.getLogger(__name__)


if __name__ == "__main__":
    from core.simulations.cloud.statistics.report import generate_report

    ##
    # CONFIGURATION
    ##
    config_path = "experiment_1.yaml"
    result_path = "experiment_1.csv"
    threshold_min = 13
    threshold_max = 20
    threshold_step = 1
    replications = 5
    logger_level = "INFO"

    logging.basicConfig(level=logger_level)

    logger.info("Configuration loaded: {}".format(config_path))

    if os.path.exists(config_path):
        with open(config_path, "r") as config_file:
            config = yaml.load(config_file)
    else:
        logger.fatal("Unrecognized configuration: {}".format(config_path))
        exit(1)

    thresholds = range(threshold_min, threshold_max, threshold_step)

    ##
    # SIMULATION
    ##
    simulation_id = 1
    simulations_tot = len(thresholds) * replications
    must_save_csv_headers = not os.path.exists(result_path)
    for threshold in thresholds:
        for replication in range(replications):
            config["system"]["cloudlet"]["threshold"] = threshold
            config["general"]["random"]["seed"] += simulation_id
            logger.info("Initializing simulation (threshold {} | replica {}/{} | simulation {}/{})"
                        .format(threshold, replication+1, replications, simulation_id, simulations_tot))
            simulation = Simulation(config, "SIMULATION-THRESHOLD-{}_{}".format(threshold, replication+1))
            simulation.run()
            logger.info("Generating report")
            report = generate_report(simulation)
            logger.info("Report: %s", report)
            if must_save_csv_headers:
                report.save_header_csv(result_path)
                must_save_csv_headers = False
            report.append_csv(result_path)
            simulation_id += 1