"""
MARKOV ANALYSIS: Generate the Markov Chain model of the system, according to settings in 'markov_analysis.yaml'
Results are stored in 'out/markov_analysis' and can be visualized running the Matlab Live Script 'pmcsn.mlx'
"""

from core.simulation.model.config import load_configuration
from core.utils.logutils import ConsoleHandler
from core.simulation.model.scope import TaskScope
from core.utils import markovutils
from core.utils import file_utils
import logging
import os
from sympy import *


# Configure logger
logging.basicConfig(level=logging.INFO, handlers=[ConsoleHandler(logging.INFO)])
logger = logging.getLogger(__name__)

# Configuration
CONFIG_PATH = "markov_analysis.yaml"

# Results
OUTDIR = "out/markov_analysis"


def run(config_path=CONFIG_PATH):
    """
    Execute the experiment.
    :param config_path: (string) the path of the configuration file.
    :return: None
    """
    config = load_configuration(config_path, norm=False)

    clt_n_servers = config["system"]["cloudlet"]["n_servers"]
    clt_threshold = config["system"]["cloudlet"]["threshold"]
    arrival_1 = config["arrival"][TaskScope.TASK_1.name]["parameters"]["r"]
    arrival_2 = config["arrival"][TaskScope.TASK_2.name]["parameters"]["r"]
    clt_service_1 = config["system"]["cloudlet"]["service"][TaskScope.TASK_1.name]["parameters"]["r"]
    clt_service_2 = config["system"]["cloudlet"]["service"][TaskScope.TASK_2.name]["parameters"]["r"]
    cld_service_1 = config["system"]["cloud"]["service"][TaskScope.TASK_1.name]["parameters"]["r"]
    cld_service_2 = config["system"]["cloud"]["service"][TaskScope.TASK_2.name]["parameters"]["r"]
    t_setup = config["system"]["cloud"]["setup"][TaskScope.TASK_2.name]["parameters"]["m"]

    logger.info("Launching Markov Chain generation with clt_n_servers={}, clt_threshold={}, arrival_1={}, arrival_2={}, clt_service_1={}, clt_service_2={}".format(
        clt_n_servers, clt_threshold, arrival_1, arrival_2, clt_service_1, clt_service_2
    ))

    MC = markovutils.generate_markov_chain(clt_n_servers, clt_threshold, arrival_1, arrival_2, clt_service_1, clt_service_2)
    states = MC.get_states()

    states_clt_1 = markovutils.compute_states_clt_1(states, clt_n_servers)
    states_clt_2 = markovutils.compute_states_clt_2(states, clt_n_servers, clt_threshold)
    states_clt_3 = markovutils.compute_states_clt_3(states, clt_n_servers, clt_threshold)

    solutions = markovutils.solve(MC)

    a_clt_1 = 0
    for state_clt_1 in states_clt_1:
        a_clt_1 += solutions[state_clt_1.pretty_str()]

    a_clt_2 = 0
    for state_clt_2 in states_clt_2:
        a_clt_2 += solutions[state_clt_2.pretty_str()]

    p = 0
    for state_clt_3 in states_clt_3:
        p += solutions[state_clt_3.pretty_str()]
    p *= (arrival_1/(arrival_1+arrival_2))

    print(a_clt_1)
    print(a_clt_2)
    print(p)



if __name__ == "__main__":
    run()