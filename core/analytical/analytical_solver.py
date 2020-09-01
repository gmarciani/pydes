from core.analytical.analytical_solution import AnalyticalSolution
from core.utils.logutils import ConsoleHandler
from core.simulation.model.scope import TaskScope
from core.utils.report import SimpleReport as Report
from core.rnd.rndvar import Variate
from core.simulation.model.scope import SystemScope
from core.simulation.model.controller import ControllerAlgorithm
from core.markov import markovgen
import logging

# Configure logger
logging.basicConfig(level=logging.INFO, handlers=[ConsoleHandler(logging.INFO)])
logger = logging.getLogger(__name__)


class AnalyticalSolver:
    """
    A solver for the analytical model of the target system.
    """

    def __init__(self, config):
        """
        Creates a new anaytical solver.
        :param config: (Configuration) the system configuration.
        """
        # Validate configuration: Markovian assumption must holds true.
        assert config["arrival"][TaskScope.TASK_1.name]["distribution"] == "EXPONENTIAL"
        assert config["arrival"][TaskScope.TASK_2.name]["distribution"] == "EXPONENTIAL"
        assert config["system"]["cloudlet"]["service"][TaskScope.TASK_1.name]["distribution"] == "EXPONENTIAL"
        assert config["system"]["cloudlet"]["service"][TaskScope.TASK_2.name]["distribution"] == "EXPONENTIAL"
        assert config["system"]["cloud"]["service"][TaskScope.TASK_1.name]["distribution"] == "EXPONENTIAL"
        assert config["system"]["cloud"]["service"][TaskScope.TASK_2.name]["distribution"] == "EXPONENTIAL"

        self.config = config

        # Dimensions
        self.clt_n_servers = self.config["system"]["cloudlet"]["n_servers"]
        self.clt_controller_algorithm = self.config["system"]["cloudlet"]["controller_algorithm"]
        if self.clt_controller_algorithm is ControllerAlgorithm.ALGORITHM_1:
            self.clt_threshold = None
        else:
            self.clt_threshold = self.config["system"]["cloudlet"]["threshold"]

        # Arrivals
        self.arrival_rates = {tsk: self.config["arrival"][tsk.name]["parameters"]["r"] for tsk in TaskScope.concrete()}
        self.service_rates = {sys: {tsk: self.config["system"][sys.name.lower()]["service"][tsk.name]["parameters"]["r"] for tsk in TaskScope.concrete()} for sys in SystemScope.subsystems()}
        self.t_setup = self.config["system"]["cloud"]["setup"][TaskScope.TASK_2.name]["parameters"]["m"]

        self.markov_chain = None
        self.solution = None

    def solve(self, routing_a_clt_1=None, routing_a_clt_2=None, routing_r=None, t_lost_clt_2=None):
        """
        Solves the analytical model of the target system.
        :param config: (Configuration) the system configuration.
        :param routing_a_clt_1: (float) the routing probability of accepted tasks 1 in Cloudlet.
        :param routing_a_clt_2: (float) the routing probability of accepted tasks 2 in Cloudlet.
        :param routing_r: (float) the routing probability of restarted tasks 2 in Cloud.
        :param t_lost_clt_2: (float) the average time lost by tasks 2 in Cloudlet.
        :return: None
        """

        # Compute routing probabilities (if not yet computed).
        if routing_a_clt_1 is None or routing_a_clt_2 is None or routing_r is None:
            self.markov_chain = markovgen.generate_markov_chain(self.clt_n_servers, self.clt_threshold,
                                                 self.arrival_rates[TaskScope.TASK_1],
                                                 self.arrival_rates[TaskScope.TASK_2],
                                                 self.service_rates[SystemScope.CLOUDLET][TaskScope.TASK_1],
                                                 self.service_rates[SystemScope.CLOUDLET][TaskScope.TASK_2])
            states = self.markov_chain.get_states()

            states_clt_1 = markovgen.compute_states_clt_1(states, self.clt_n_servers)
            states_clt_2 = markovgen.compute_states_clt_2(states, self.clt_n_servers, self.clt_threshold)
            states_clt_3 = markovgen.compute_states_clt_3(states, self.clt_n_servers, self.clt_threshold)

            solutions = markovgen.solve(self.markov_chain)

            routing_a_clt_1 = 0
            for state_clt_1 in states_clt_1:
                routing_a_clt_1 += solutions[state_clt_1.pretty_str()]

            routing_a_clt_2 = 0
            for state_clt_2 in states_clt_2:
                routing_a_clt_2 += solutions[state_clt_2.pretty_str()]

            routing_r = 0
            for state_clt_3 in states_clt_3:
                routing_r += solutions[state_clt_3.pretty_str()]
            routing_r *= (self.arrival_rates[TaskScope.TASK_1] / (self.arrival_rates[TaskScope.TASK_1] + self.arrival_rates[TaskScope.TASK_2]))

        # Compute the average time lost by 2nd class tasks in Cloudlet (if not yet computed).
        T_lost_clt_2 = t_lost_clt_2 if t_lost_clt_2 is not None else 0.5 * (1.0 / self.service_rates[SystemScope.CLOUDLET][TaskScope.TASK_2])

        # Accepted Traffic
        lambda_clt_1 = routing_a_clt_1 * self.arrival_rates[TaskScope.TASK_1]
        lambda_clt_2 = routing_a_clt_2 * self.arrival_rates[TaskScope.TASK_2]
        lambda_cld_1 = (1.0 - routing_a_clt_1) * self.arrival_rates[TaskScope.TASK_1]
        lambda_cld_2 = (1.0 - routing_a_clt_2) * self.arrival_rates[TaskScope.TASK_2]

        # Restarted Traffic
        lambda_r = routing_r * (self.arrival_rates[TaskScope.TASK_1] + self.arrival_rates[TaskScope.TASK_2])

        # Performance Metrics: Cloudlet
        T_clt_1 = 1.0 / self.service_rates[SystemScope.CLOUDLET][TaskScope.TASK_1]
        N_clt_1 = lambda_clt_1 * T_clt_1
        T_clt_2 = 1.0 / self.service_rates[SystemScope.CLOUDLET][TaskScope.TASK_2]
        N_clt_2 = (lambda_clt_2 * T_clt_2) - (lambda_r * T_lost_clt_2)
        N_clt = N_clt_1 + N_clt_2
        T_clt = ((N_clt_1 / N_clt) * T_clt_1) + ((N_clt_2 / N_clt) * T_clt_2)
        X_clt_1 = lambda_clt_1
        X_clt_2 = lambda_clt_2 - lambda_r
        X_clt = lambda_clt_1 + lambda_clt_2 - lambda_r

        # Performance Metrics: Cloud
        T_cld_1 = 1.0 / self.service_rates[SystemScope.CLOUD][TaskScope.TASK_1]
        N_cld_1 = lambda_cld_1 * T_cld_1
        T_cld_2_np = 1.0 / self.service_rates[SystemScope.CLOUD][TaskScope.TASK_2]
        N_cld_2_np = lambda_cld_2 * T_cld_2_np
        T_cld_2_p = T_cld_2_np + self.t_setup # TODO WARNING maybe we should add T_lost_cld_2
        N_cld_2_p = lambda_r * T_cld_2_p
        N_cld_2 = N_cld_2_np + N_cld_2_p
        T_cld_2 = ((N_cld_2_np / N_cld_2) * T_cld_2_np) + ((N_cld_2_p / N_cld_2) * T_cld_2_p)
        N_cld = N_cld_1 + N_cld_2
        T_cld = ((N_cld_1 / N_cld) * T_cld_1) + ((N_cld_2 / N_cld) * T_cld_2)
        X_cld_1 = lambda_cld_1
        X_cld_2 = lambda_cld_2 + lambda_r
        X_cld = lambda_cld_1 + lambda_cld_2 + lambda_r

        # Performance Metrics: System
        N_sys_1 = N_clt_1 + N_cld_1
        N_sys_2 = N_cld_1 + N_cld_2
        N_sys = N_clt + N_cld
        T_sys_1 = ((N_clt_1 / N_sys) * T_clt_1) + ((N_cld_1 / N_sys) * T_cld_1)
        T_sys_2 = ((N_clt_2 / N_sys) * T_clt_2) + ((N_cld_2 / N_sys) * T_cld_2)
        T_sys = ((N_clt / N_sys) * T_clt) + ((N_cld / N_sys) * T_cld)
        X_sys_1 = X_clt_1 + X_cld_1
        X_sys_2 = X_clt_2 + X_cld_2
        X_sys = X_sys_1 + X_sys_2

        #logger.info("routing_a_clt_1 = %f" % routing_a_clt_1)
        #logger.info("routing_a_clt_2 = %f" % routing_a_clt_2)
        #logger.info("routing_r = %f" % routing_r)
        #logger.info("T_lost_clt_2 = %f" % T_lost_clt_2)

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
        r.add("system/cloudlet", "controller_algorithm", self.clt_controller_algorithm)
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

        return r