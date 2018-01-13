from core.utils.report import SimpleReport as Report
import logging

# Configure logger
logger = logging.getLogger(__name__)


def generate_report(sim, float_prec=3):
    """
    Generate a full report about the given simulation.
    :param simulation: the simulation to generate the report from.
    :param float_prec: (int) the number of decimals for float values.
    :return: (SimpleReport) the report.
    """
    report = Report(sim.name)

    # Report - General
    report.add("general", "simulation_class", sim.__class__.__name__)
    report.add("general", "t_stop", sim.t_stop)
    report.add("general", "random_generator", sim.rndgen.__class__.__name__)
    report.add("general", "random_seed", sim.rndgen.get_initial_seed())

    # Report - Tasks
    report.add_all("tasks", sim.taskgen)

    # Report - System
    report.add("system", "n_1", sim.system.n_1)
    report.add("system", "n_2", sim.system.n_2)
    report.add("system", "n_arrival_1", sim.system.n_arrival_1)
    report.add("system", "n_arrival_2", sim.system.n_arrival_2)
    report.add("system", "n_served_1", sim.system.n_served_1)
    report.add("system", "n_served_2", sim.system.n_served_2)
    report.add("system", "throughput", round(sim.system.get_throughput(), float_prec))
    report.add("system", "response_time (mean)", round(sim.system.response_time.get_mean(), float_prec))
    report.add("system", "response_time (stddev)", round(sim.system.response_time.get_stddev(), float_prec))
    report.add("system", "utilization", round(sim.system.get_utilization(), float_prec))

    # Report - System/Cloudlet
    report.add_all("system/cloudlet", sim.system.cloudlet)

    # Report - System/Cloud
    report.add_all("system/cloud", sim.system.cloud)

    return report


