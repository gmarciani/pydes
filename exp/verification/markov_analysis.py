"""
MARKOV ANALYSIS: Generate the Markov Chain model of the system, according to settings in "markov_analysis.yaml"
Results are stored in "out/markov_analysis" and can be visualized running the Matlab Live Script "pmcsn.mlx"
"""

from core.simulation.model.config import load_configuration
from core.utils.logutils import ConsoleHandler
from core.simulation.model.scope import TaskScope
from core.markov import markovgen
import logging

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

    # Load configuration
    config = load_configuration(config_path, norm=False)

    # Validate configuration: Markovian assumption must hold true.
    assert config["arrival"][TaskScope.TASK_1.name]["distribution"] == "EXPONENTIAL"
    assert config["arrival"][TaskScope.TASK_2.name]["distribution"] == "EXPONENTIAL"
    assert config["system"]["cloudlet"]["service"][TaskScope.TASK_1.name]["distribution"] == "EXPONENTIAL"
    assert config["system"]["cloudlet"]["service"][TaskScope.TASK_2.name]["distribution"] == "EXPONENTIAL"
    assert config["system"]["cloud"]["service"][TaskScope.TASK_1.name]["distribution"] == "EXPONENTIAL"
    assert config["system"]["cloud"]["service"][TaskScope.TASK_2.name]["distribution"] == "EXPONENTIAL"

    # Load parameters
    clt_n_servers = config["system"]["cloudlet"]["n_servers"]
    clt_threshold = config["system"]["cloudlet"]["threshold"]
    arrival_1 = config["arrival"][TaskScope.TASK_1.name]["parameters"]["r"]
    arrival_2 = config["arrival"][TaskScope.TASK_2.name]["parameters"]["r"]
    clt_service_1 = config["system"]["cloudlet"]["service"][TaskScope.TASK_1.name]["parameters"]["r"]
    clt_service_2 = config["system"]["cloudlet"]["service"][TaskScope.TASK_2.name]["parameters"]["r"]
    cld_service_1 = config["system"]["cloud"]["service"][TaskScope.TASK_1.name]["parameters"]["r"]
    cld_service_2 = config["system"]["cloud"]["service"][TaskScope.TASK_2.name]["parameters"]["r"]
    t_setup = config["system"]["cloud"]["setup"][TaskScope.TASK_2.name]["parameters"]["m"]

    # Routing probabilities:
    #   - a_clt_1: accepted 1st class traffic in the Cloudlet.
    #   - a_clt_2: accepted 2nd class traffic in the Cloudlet.
    #   - r: restarted 2nd class traffic from the Cloudlet to the Cloud.
    #
    # As the calculus of these routing probabilities is heavy, you can specify them here to skip it.
    # If you want to compute them again, simply set them as None.
    a_clt_1 = 0.978326334857105
    a_clt_2 = 0.603529764734761
    r = 0.183573830264005

    #a_clt_1 = None
    #a_clt_2 = None
    #r = None

    # Quota of 2nd class tasks service time in Cloudlet lost before restart.
    # This value can be estimated leveraging the simulator.
    psi = 0.39077113824

    # Compute routing probabilities if not yet computed.
    if (a_clt_1 is None or a_clt_2 is None or r is None):
        MC = markovgen.generate_markov_chain(clt_n_servers, clt_threshold, arrival_1, arrival_2, clt_service_1, clt_service_2)
        states = MC.get_states()

        states_clt_1 = markovgen.compute_states_clt_1(states, clt_n_servers)
        states_clt_2 = markovgen.compute_states_clt_2(states, clt_n_servers, clt_threshold)
        states_clt_3 = markovgen.compute_states_clt_3(states, clt_n_servers, clt_threshold)

        solutions = markovgen.solve(MC)

        a_clt_1 = 0
        for state_clt_1 in states_clt_1:
            a_clt_1 += solutions[state_clt_1.pretty_str()]

        a_clt_2 = 0
        for state_clt_2 in states_clt_2:
            a_clt_2 += solutions[state_clt_2.pretty_str()]

        r = 0
        for state_clt_3 in states_clt_3:
            r += solutions[state_clt_3.pretty_str()]
        r *= (arrival_1/(arrival_1+arrival_2))

    # Report performance metrics

    # Routing Probabilities
    print("ROUTING PROBABILITIES")
    print("a_clt_1: ", a_clt_1)
    print("a_clt_2: ", a_clt_2)
    print("r: ", r)

    # Accepted Traffic
    lambda_clt_1 = a_clt_1 * arrival_1
    lambda_clt_2 = a_clt_2 * arrival_2
    lambda_cld_1 = (1 - a_clt_1) * arrival_1
    lambda_cld_2 = (1 - a_clt_2) * arrival_2

    print("ACCEPTED TRAFFIC")
    print("lambda_clt_1: ", lambda_clt_1)
    print("lambda_clt_2: ", lambda_clt_2)
    print("lambda_cld_1: ", lambda_cld_1)
    print("lambda_cld_2: ", lambda_cld_2)

    # Restarted Traffic
    lambda_p = r * (arrival_1 + arrival_2)

    print("RESTARTED TRAFFIC")
    print("lambda_p: ", lambda_p)

    # Performance Metrics: Cloudlet
    T_clt_1 = 1 / clt_service_1
    N_clt_1 = lambda_clt_1 * T_clt_1
    T_clt_2 = 1 / clt_service_2
    N_clt_2 = (lambda_clt_2 * T_clt_2) - (psi * lambda_p * T_clt_2)
    N_clt = N_clt_1 + N_clt_2
    T_clt = ((N_clt_1 / N_clt) * T_clt_1) + ((N_clt_2 / N_clt) * T_clt_2)
    X_clt_1 = lambda_clt_1
    X_clt_2 = lambda_clt_2 - lambda_p
    X_clt = lambda_clt_1 + lambda_clt_2 - lambda_p

    print("PERFORMANCE METRICS: CLOUDLET")
    print("T_clt_1: ", T_clt_1)
    print("N_clt_1: ", N_clt_1)
    print("T_clt_2: ", T_clt_2)
    print("N_clt_2: ", N_clt_2)
    print("N_clt: ", N_clt)
    print("T_clt: ", T_clt)
    print("X_clt_1: ", X_clt_1)
    print("X_clt_2: ", X_clt_2)
    print("X_clt: ", X_clt)

    # Performance Metrics: Cloud
    T_cld_1 = 1 / cld_service_1
    N_cld_1 = lambda_cld_1 * T_cld_1
    T_cld_2_np = 1 / cld_service_2
    N_cld_2_np = lambda_cld_2 * T_cld_2_np
    T_cld_2_p = T_cld_2_np + t_setup + (psi * T_clt_2)
    N_cld_2_p = lambda_p * T_cld_2_p
    N_cld_2 = N_cld_2_np + N_cld_2_p
    T_cld_2 = ((N_cld_2_np / N_cld_2) * T_cld_2_np) + ((N_cld_2_p / N_cld_2) * T_cld_2_p)
    N_cld = N_cld_1 + N_cld_2
    T_cld = ((N_cld_1 / N_cld) * T_cld_1) + ((N_cld_2 / N_cld) * T_cld_2)
    X_cld_1 = lambda_cld_1
    X_cld_2 = lambda_cld_2 + lambda_p
    X_cld = lambda_cld_1 + lambda_cld_2 + lambda_p

    print("PERFORMANCE METRICS: CLOUD")
    print("T_cld_1: ", T_cld_1)
    print("N_cld_1: ", N_cld_1)
    print("T_cld_2_np: ", T_cld_2_np)
    print("N_cld_2_np: ", N_cld_2_np)
    print("T_cld_2_p: ", T_cld_2_p)
    print("N_cld_2_p: ", N_cld_2_p)
    print("N_cld_2: ", N_cld_2)
    print("T_cld_2: ", T_cld_2)
    print("N_cld: ", N_cld)
    print("T_cld: ", T_cld)
    print("X_cld_1: ", X_cld_1)
    print("X_cld_2: ", X_cld_2)
    print("X_cld: ", X_cld)

    # Performance Metrics: System
    N_sys = N_clt + N_cld
    T_sys = ((N_clt / N_sys) * T_clt) + ((N_cld / N_sys) * T_cld)
    X_sys = X_clt + X_cld

    print("PERFORMANCE METRICS: SYSTEM")
    print("N_sys: ", N_sys)
    print("T_sys: ", T_sys)
    print("X_sys: ", X_sys)


if __name__ == "__main__":
    run()