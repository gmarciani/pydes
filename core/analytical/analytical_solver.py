from core.analytical.analytical_solution import AnalyticalSolution
from core.simulation.model.scope import TaskScope
from core.utils.report import SimpleReport as Report
from core.rnd.rndvar import Variate
from core.simulation.model.scope import SystemScope
from core.simulation.model.controller import ControllerAlgorithm
from core.analytical.markov_chains import MarkovChainAlgorithm1, MarkovChainAlgorithm2
import logging

# Configure logger
logger = logging.getLogger(__name__)

CONTROLLER_ALGORITHM_TO_MARKOV_CHAIN = {
    ControllerAlgorithm.ALGORITHM_1: MarkovChainAlgorithm1,
    ControllerAlgorithm.ALGORITHM_2: MarkovChainAlgorithm2
}


class AnalyticalSolver:
    """
    A solver for the analytical model of the target system.
    """

    def __init__(self, config):
        """
        Creates a new analytical solver.
        :param config: (Configuration) the system configuration.
        """

        self.config = config
        self.markov_chain = None
        self.states_probabilities = None
        self.routing_probabilities = None
        self.solution = None

        self.__validate_markovianity()

        self.clt_n_servers = self.config["system"]["cloudlet"]["n_servers"]
        self.clt_controller_algorithm = ControllerAlgorithm[self.config["system"]["cloudlet"]["controller_algorithm"]]
        self.clt_threshold = self.config["system"]["cloudlet"]["threshold"] if self.clt_controller_algorithm is ControllerAlgorithm.ALGORITHM_2 else None

        self.arrival_rates = {tsk: self.config["arrival"][tsk.name]["parameters"]["r"] for tsk in TaskScope.concrete()}
        self.service_rates = {sys: {tsk: self.config["system"][sys.name.lower()]["service"][tsk.name]["parameters"]["r"] for tsk in TaskScope.concrete()} for sys in SystemScope.subsystems()}
        self.t_setup = self.config["system"]["cloud"]["setup"][TaskScope.TASK_2.name]["parameters"]["m"]

    def solve(self, t_lost_clt_2=None):
        """
        Solves the analytical model of the target system.
        :return: None
        """

        if self.clt_controller_algorithm is ControllerAlgorithm.ALGORITHM_1:
            self.markov_chain = MarkovChainAlgorithm1(self.clt_n_servers,
                                                      self.arrival_rates[TaskScope.TASK_1],
                                                      self.arrival_rates[TaskScope.TASK_2],
                                                      self.service_rates[SystemScope.CLOUDLET][TaskScope.TASK_1],
                                                      self.service_rates[SystemScope.CLOUDLET][TaskScope.TASK_2])
        elif self.clt_controller_algorithm is ControllerAlgorithm.ALGORITHM_2:
            self.markov_chain = MarkovChainAlgorithm2(self.clt_n_servers, self.clt_threshold,
                                                      self.arrival_rates[TaskScope.TASK_1],
                                                      self.arrival_rates[TaskScope.TASK_2],
                                                      self.service_rates[SystemScope.CLOUDLET][TaskScope.TASK_1],
                                                      self.service_rates[SystemScope.CLOUDLET][TaskScope.TASK_2])
        else:
            raise ValueError("Unrecognized controller algorithm: {}".format(self.clt_controller_algorithm))

        self.states_probabilities = self.markov_chain.solve()
        self.routing_probabilities = self.__compute_routing_probabilities()

        # Compute the average time lost by 2nd class tasks in Cloudlet (if not yet computed).
        factor_service_lost_clt_2 = 0.5
        T_lost_clt_2 = t_lost_clt_2 if t_lost_clt_2 is not None else factor_service_lost_clt_2 * (1.0 / self.service_rates[SystemScope.CLOUDLET][TaskScope.TASK_2])

        # Accepted Traffic
        lambda_clt_1 = self.routing_probabilities["routing_accepted_clt_1"] * self.arrival_rates[TaskScope.TASK_1]
        lambda_clt_2 = self.routing_probabilities["routing_accepted_clt_2"] * self.arrival_rates[TaskScope.TASK_2]
        lambda_cld_1 = (1.0 - self.routing_probabilities["routing_accepted_clt_1"]) * self.arrival_rates[TaskScope.TASK_1]
        lambda_cld_2 = (1.0 - self.routing_probabilities["routing_accepted_clt_2"]) * self.arrival_rates[TaskScope.TASK_2]

        # Restarted Traffic
        lambda_r = self.routing_probabilities["routing_accepted_clt_2_restarted"] * (self.arrival_rates[TaskScope.TASK_1] + self.arrival_rates[TaskScope.TASK_2])  # may be: routing_accepted_clt_2_restarted * (self.arrival_rates[TaskScope.TASK_2])

        # Tasks probabilities
        p_1 = self.arrival_rates[TaskScope.TASK_1] / (self.arrival_rates[TaskScope.TASK_1] + self.arrival_rates[TaskScope.TASK_2])
        p_2 = self.arrival_rates[TaskScope.TASK_2] / (self.arrival_rates[TaskScope.TASK_1] + self.arrival_rates[TaskScope.TASK_2])

        # Performance Metrics: Cloudlet
        N_clt_1 = sum(state.value[0] * self.states_probabilities[state.pretty_str()] for state in self.markov_chain.get_states())  #  may be: lambda_clt_1 * T_clt_1
        N_clt_2 = sum(state.value[1] * self.states_probabilities[state.pretty_str()] for state in self.markov_chain.get_states())  #  may be: (lambda_clt_2 * T_clt_2) - (lambda_r * T_lost_clt_2)
        N_clt = N_clt_1 + N_clt_2

        T_clt_1 = 1.0 / self.service_rates[SystemScope.CLOUDLET][TaskScope.TASK_1]
        T_clt_2 = 1.0 / self.service_rates[SystemScope.CLOUDLET][TaskScope.TASK_2]
        T_clt = ((N_clt_1 / N_clt) * T_clt_1) + ((N_clt_2 / N_clt) * T_clt_2)

        X_clt_1 = lambda_clt_1  #  may be: N_clt_1 / T_clt_1
        X_clt_2 = lambda_clt_2 - lambda_r  #  may be: N_clt_2 / T_clt_2
        X_clt = X_clt_1 + X_clt_2

        # Performance Metrics: Cloud
        T_cld_1 = 1.0 / self.service_rates[SystemScope.CLOUD][TaskScope.TASK_1]
        T_cld_2_np = 1.0 / self.service_rates[SystemScope.CLOUD][TaskScope.TASK_2]
        T_cld_2_p = T_cld_2_np + self.t_setup  # may be: T_cld_2_np + self.t_setup + T_lost_cld_2

        N_cld_1 = lambda_cld_1 * T_cld_1
        N_cld_2_np = lambda_cld_2 * T_cld_2_np
        N_cld_2_p = lambda_r * T_cld_2_p
        N_cld_2 = N_cld_2_np + N_cld_2_p
        N_cld = N_cld_1 + N_cld_2

        T_cld_2 = ((N_cld_2_np / N_cld_2) * T_cld_2_np) + ((N_cld_2_p / N_cld_2) * T_cld_2_p)
        T_cld = ((N_cld_1 / N_cld) * T_cld_1) + ((N_cld_2 / N_cld) * T_cld_2)

        X_cld_1 = lambda_cld_1
        X_cld_2 = lambda_cld_2 + lambda_r
        X_cld = X_cld_1 + X_cld_2

        # Performance Metrics: System
        N_sys = N_clt_1 + N_cld_1 + N_cld_1 + N_cld_2
        N_sys_1 = p_1 * N_sys
        N_sys_2 = p_2 * N_sys

        T_sys_1 = ((N_clt_1 / N_sys_1) * T_clt_1) + ((N_cld_1 / N_sys_1) * T_cld_1)
        T_sys_2 = ((N_clt_2 / N_sys_2) * T_clt_2) + ((N_cld_2 / N_sys_2) * T_cld_2)
        T_sys = ((N_sys_1 / N_sys) * T_sys_1) + ((N_sys_2 / N_sys) * T_sys_2)

        X_sys_1 = X_clt_1 + X_cld_1
        X_sys_2 = X_clt_2 + X_cld_2
        X_sys = X_sys_1 + X_sys_2

        self.solution = AnalyticalSolution()

        # System
        self.solution.performance_metrics.population[SystemScope.SYSTEM][TaskScope.TASK_1] = N_sys_1
        self.solution.performance_metrics.population[SystemScope.SYSTEM][TaskScope.TASK_2] = N_sys_2
        self.solution.performance_metrics.population[SystemScope.SYSTEM][TaskScope.GLOBAL] = N_sys
        self.solution.performance_metrics.response[SystemScope.SYSTEM][TaskScope.TASK_1] = T_sys_1
        self.solution.performance_metrics.response[SystemScope.SYSTEM][TaskScope.TASK_2] = T_sys_2
        self.solution.performance_metrics.response[SystemScope.SYSTEM][TaskScope.GLOBAL] = T_sys
        self.solution.performance_metrics.throughput[SystemScope.SYSTEM][TaskScope.TASK_1] = X_sys_1
        self.solution.performance_metrics.throughput[SystemScope.SYSTEM][TaskScope.TASK_2] = X_sys_2
        self.solution.performance_metrics.throughput[SystemScope.SYSTEM][TaskScope.GLOBAL] = X_sys

        # Cloudlet
        self.solution.performance_metrics.population[SystemScope.CLOUDLET][TaskScope.TASK_1] = N_clt_1
        self.solution.performance_metrics.population[SystemScope.CLOUDLET][TaskScope.TASK_2] = N_clt_2
        self.solution.performance_metrics.population[SystemScope.CLOUDLET][TaskScope.GLOBAL] = N_clt
        self.solution.performance_metrics.response[SystemScope.CLOUDLET][TaskScope.TASK_1] = T_clt_1
        self.solution.performance_metrics.response[SystemScope.CLOUDLET][TaskScope.TASK_2] = T_clt_2
        self.solution.performance_metrics.response[SystemScope.CLOUDLET][TaskScope.GLOBAL] = T_clt
        self.solution.performance_metrics.throughput[SystemScope.CLOUDLET][TaskScope.TASK_1] = X_clt_1
        self.solution.performance_metrics.throughput[SystemScope.CLOUDLET][TaskScope.TASK_2] = X_clt_2
        self.solution.performance_metrics.throughput[SystemScope.CLOUDLET][TaskScope.GLOBAL] = X_clt

        # Cloud
        self.solution.performance_metrics.population[SystemScope.CLOUD][TaskScope.TASK_1] = N_cld_1
        self.solution.performance_metrics.population[SystemScope.CLOUD][TaskScope.TASK_2] = N_cld_2
        self.solution.performance_metrics.population[SystemScope.CLOUD][TaskScope.GLOBAL] = N_cld
        self.solution.performance_metrics.response[SystemScope.CLOUD][TaskScope.TASK_1] = T_cld_1
        self.solution.performance_metrics.response[SystemScope.CLOUD][TaskScope.TASK_2] = T_cld_2
        self.solution.performance_metrics.response[SystemScope.CLOUD][TaskScope.GLOBAL] = T_cld
        self.solution.performance_metrics.throughput[SystemScope.CLOUD][TaskScope.TASK_1] = X_cld_1
        self.solution.performance_metrics.throughput[SystemScope.CLOUD][TaskScope.TASK_2] = X_cld_2
        self.solution.performance_metrics.throughput[SystemScope.CLOUD][TaskScope.GLOBAL] = X_cld

    def __compute_routing_probabilities(self):
        routing_probabilities = dict(
            routing_accepted_clt_1=0.0,
            routing_accepted_clt_2=0.0,
            routing_accepted_clt_2_restarted=0.0
        )

        states = self.markov_chain.get_states()

        if self.clt_controller_algorithm is ControllerAlgorithm.ALGORITHM_1:
            states_accepted_clt_1 = filter(lambda state: state.value[0] + state.value[1] < self.clt_n_servers, states)
            states_accepted_clt_2 = filter(lambda state: state.value[0] + state.value[1] < self.clt_n_servers, states)
            states_accepted_clt_2_restarted = []
        elif self.clt_controller_algorithm is ControllerAlgorithm.ALGORITHM_2:
            states_accepted_clt_1 = filter(lambda state: state.value[0] < self.clt_n_servers, states)
            states_accepted_clt_2 = filter(lambda state: state.value[0] + state.value[1] < self.clt_threshold, states)
            states_accepted_clt_2_restarted = filter(lambda state: state.value[0] + state.value[1] >= self.clt_threshold and state.value[1] > 0, states)
        else:
            raise ValueError("Unrecognized controller algorithm: {}".format(self.clt_controller_algorithm))

        # Probability to accept a task of type 1 into the Cloudlet
        for state_clt_1 in states_accepted_clt_1:
            routing_probabilities["routing_accepted_clt_1"] += self.states_probabilities[state_clt_1.pretty_str()]

        # Probability to accept a task of type 2 into the Cloudlet
        for state_clt_2 in states_accepted_clt_2:
            routing_probabilities["routing_accepted_clt_2"] += self.states_probabilities[state_clt_2.pretty_str()]

        # Probability to interrupt a task of type 2 from the Cloudlet and restart it into the Cloud
        for state_clt_2_restarted in states_accepted_clt_2_restarted:
            routing_probabilities["routing_accepted_clt_2_restarted"] += self.states_probabilities[state_clt_2_restarted.pretty_str()]
        routing_probabilities["routing_accepted_clt_2_restarted"] *= (self.arrival_rates[TaskScope.TASK_1] / (
                    self.arrival_rates[TaskScope.TASK_1] + self.arrival_rates[TaskScope.TASK_2]))

        return routing_probabilities

    def __validate_markovianity(self):
        assert self.config["arrival"][TaskScope.TASK_1.name]["distribution"] == "EXPONENTIAL"
        assert self.config["arrival"][TaskScope.TASK_2.name]["distribution"] == "EXPONENTIAL"
        assert self.config["system"][SystemScope.CLOUDLET.name.lower()]["service"][TaskScope.TASK_1.name]["distribution"] == "EXPONENTIAL"
        assert self.config["system"][SystemScope.CLOUDLET.name.lower()]["service"][TaskScope.TASK_2.name]["distribution"] == "EXPONENTIAL"
        assert self.config["system"][SystemScope.CLOUD.name.lower()]["service"][TaskScope.TASK_1.name]["distribution"] == "EXPONENTIAL"
        assert self.config["system"][SystemScope.CLOUD.name.lower()]["service"][TaskScope.TASK_2.name]["distribution"] == "EXPONENTIAL"

    # ==================================================================================================================
    # REPORT
    # ==================================================================================================================

    def generate_report(self):
        """
        Generate the solver report.
        :return: (SimpleReport) the solver report.
        """
        r = Report("ANALYTICAL-SOLUTION")

        # Report - Arrivals
        for tsk in TaskScope.concrete():
            r.add("arrival", "arrival_{}_dist".format(tsk.name.lower()), Variate.EXPONENTIAL.name)
            r.add("arrival", "arrival_{}_rate".format(tsk.name.lower()), self.arrival_rates[tsk])

        # Report - System/Cloudlet
        r.add("system/cloudlet", "n_servers", self.clt_n_servers)
        r.add("system/cloudlet", "controller_algorithm", self.clt_controller_algorithm.name)
        if self.clt_controller_algorithm is ControllerAlgorithm.ALGORITHM_2:
            r.add("system/cloudlet", "threshold", self.clt_threshold)
        for tsk in TaskScope.concrete():
            r.add("system/cloudlet", "service_{}_dist".format(tsk.name.lower()), Variate.EXPONENTIAL.name)
            r.add("system/cloudlet", "service_{}_rate".format(tsk.name.lower()), self.service_rates[SystemScope.CLOUDLET][tsk])

        # Report - System/Cloud
        for tsk in TaskScope.concrete():
            r.add("system/cloud", "service_{}_dist".format(tsk.name.lower()), Variate.EXPONENTIAL.name)
            r.add("system/cloud", "service_{}_rate".format(tsk.name.lower()), self.service_rates[SystemScope.CLOUD][tsk])

        r.add("system/cloud", "setup_{}_dist".format(TaskScope.TASK_2.name.lower()), Variate.EXPONENTIAL.name)
        r.add("system/cloud", "service_{}_param_m".format(TaskScope.TASK_2.name.lower()), self.t_setup)

        # Report - Statistics
        for performance_metric in sorted(self.solution.performance_metrics.__dict__):
            for sys in sorted(SystemScope, key=lambda x: x.name):
                for tsk in sorted(TaskScope, key=lambda x: x.name):
                    r.add("statistics", "{}_{}_{}_mean".format(performance_metric, sys.name.lower(), tsk.name.lower()),
                          getattr(self.solution.performance_metrics, performance_metric)[sys][tsk])

        # Report - States Probability
        for state in sorted(self.states_probabilities):
            r.add("states probability", state, self.states_probabilities[state])

        # Report - Routing Probability
        for probability, value in self.routing_probabilities.items():
            r.add("routing probability", probability, value)

        return r