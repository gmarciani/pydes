"""
ANALYTICAL SOLUTION: Solves the analytical model leveraging Markov Chains, according to settings in
"analytical_solution.yaml"
Results are stored in "out/analytical_solution" and can be visualized running the Matlab Live Script "pmcsn.mlx"
"""

from core.simulation.model.config import load_configuration
from core.utils.logutils import ConsoleHandler
from core.analytical.analytical_solver import AnalyticalSolver
import logging
import os

# Configure logger
logging.basicConfig(level=logging.INFO, handlers=[ConsoleHandler(logging.INFO)])
logger = logging.getLogger(__name__)

# Configuration
CONFIG_PATH = "analytical_solution.yaml"

# Results
OUTDIR = "out/analytical_solution"


def run(config_path=CONFIG_PATH):
    """
    Execute the experiment.
    :param config_path: (string) the path of the configuration file.
    :return: None
    """

    # Load configuration
    config = load_configuration(config_path, norm=False)

    # Routing probabilities:
    #   - routing_a_clt_1: accepted 1st class traffic in the Cloudlet.
    #   - routing_a_clt_2: accepted 2nd class traffic in the Cloudlet.
    #   - routing_r: restarted 2nd class traffic from the Cloudlet to the Cloud.
    #
    # As the calculus of these routing probabilities is heavy, you can specify them here to skip it.
    # If you want to compute them again, simply set them as None.
    routing_a_clt_1 = 0.978326334857105
    routing_a_clt_2 = 0.603529764734761
    routing_r = 0.183573830264005

    # The average time lost by 2nd class tasks in Cloudlet.
    # This value can be estimated leveraging the simulator.
    t_lost_clt_2 = 1.47445

    solver = AnalyticalSolver(config)

    solver.solve(routing_a_clt_1=routing_a_clt_1, routing_a_clt_2=routing_a_clt_2, routing_r=routing_r, t_lost_clt_2=t_lost_clt_2)
    #solver.solve()

    reportfilecsv = os.path.join(OUTDIR, "result.csv")
    reportfiletxt = os.path.join(OUTDIR, "result.txt")
    report = solver.generate_report()
    report.save_txt(reportfiletxt, append=True, empty=True)
    report.save_csv(reportfilecsv, append=True, empty=True)

    print(report)


if __name__ == "__main__":
    run()