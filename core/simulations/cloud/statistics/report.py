from core.utils.report import SimpleReport as Report


def generate_report(sim):
    """
    Generate a full report about the given simulation.
    :param simulation: the simulation to generate the report from.
    :return: (SimpleReport) the report.
    """
    report = Report('SIMULATION')

    # Report - General
    report.add("general", "simulation_class", sim.__class__.__name__)
    report.add("general", "t_stop", sim.t_stop)
    report.add("general", "replica", sim.replica)
    report.add("general", "random_generator", sim.rndgen.__class__.__name__)
    report.add("general", "random_seed", sim.rndgen.get_initial_seed())

    # Report - Tasks
    for attr in sim.taskgen.__dict__:
        if not attr.startswith("__") and not attr.startswith("_") and not callable(getattr(sim.taskgen, attr)):
            report.add("tasks", attr, sim.taskgen.__dict__[attr])

    # Report - System
    report.add("system", "n_1", sim.system.n_1)
    report.add("system", "n_2", sim.system.n_2)
    report.add("system", "n_arrival_1", sim.system.n_arrival_1)
    report.add("system", "n_arrival_2", sim.system.n_arrival_2)
    report.add("system", "n_served_1", sim.system.n_served_1)
    report.add("system", "n_served_2", sim.system.n_served_2)

    # Report - System/Cloudlet
    for attr in sim.system.cloudlet.__dict__:
        if not attr.startswith("__") and not attr.startswith("_") and not callable(getattr(sim.system.cloudlet, attr)):
            report.add("system/cloudlet", attr, sim.system.cloudlet.__dict__[attr])

    # Report - System/Cloud
    for attr in sim.system.cloud.__dict__:
        if not attr.startswith("__") and not attr.startswith("_") and not callable(getattr(sim.system.cloud, attr)):
            report.add("system/cloud", attr, sim.system.cloud.__dict__[attr])

    return report