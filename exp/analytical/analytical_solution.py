"""
ANALYTICAL SOLUTION: Solves the analytical model leveraging Markov Chains.
"""

from core.simulation.model.config import load_configuration
from core.analytical.analytical_solver import AnalyticalSolver
from core.utils.dictutils import merge
import logging
import os

# Configure logger
logger = logging.getLogger(__name__)

# Configuration
DEFAULT_CONFIG_PATH = "analytical_solution.yaml"

# Results
DEFAULT_OUTDIR = "out/analytical_solution"

DEFAULT_PARAMETERS = {}


def run(config_path=DEFAULT_CONFIG_PATH, outdir=DEFAULT_OUTDIR, parameters=DEFAULT_PARAMETERS):
    """
    Execute the experiment.
    :param config_path: (string) the path of the configuration file.
    :param outdir: (string) the path of output directory.
    :param parameters: (dict) parameters to overwrite.
    :return: None
    """

    # Load configuration
    config = merge(load_configuration(config_path, norm=False), parameters)

    logger.info("Launching analytical solver with configuration:\n{}".format(config))

    solver = AnalyticalSolver(config)

    solver.solve()

    report = solver.generate_report()

    print(report)
    report.save_txt(os.path.join(outdir, "result.txt"), append=True, empty=True)
    report.save_csv(os.path.join(outdir, "result.csv"), append=True, empty=True)

    markov_chain = solver.markov_chain
    print("Markov Chain / Transition Matrix\n\n{}".format(markov_chain.matrixs()))
    markov_chain.render_graph(os.path.join(outdir, "MarkovChain"))


if __name__ == "__main__":
    config_path = DEFAULT_CONFIG_PATH
    outdir = DEFAULT_OUTDIR
    parameters = DEFAULT_PARAMETERS

    run(config_path, outdir, parameters)