from pydes.core.simulation.model.scope import SystemScope, TaskScope
from pydes.core.utils.csv_utils import read_csv

INDICES = ["population", "response", "throughput"]
# SYSTEM_SCOPES = [scope.name.lower() for scope in SystemScope]
SYSTEM_SCOPES = [scope.name.lower() for scope in [SystemScope.CLOUDLET, SystemScope.CLOUD, SystemScope.SYSTEM]]
TASK_SCOPES = [scope.name.lower() for scope in TaskScope]


def build_latex_table(analytical_result_path, simulation_result_path):
    """
    Generates the LateX table for simulation and analytical results.
    :param analytical_result_path: (string) the path of the analytical result file.
    :param simulation_result_path: (string) the path of the simulation result file.
    :return: (Report) validation report.
    """
    analytical_result = read_csv(analytical_result_path)[0]
    simulation_result = read_csv(simulation_result_path)[0]

    table = """
\hline
Measure & Theoretical & Experimental \\\\
\hline
"""

    for system_scope in SYSTEM_SCOPES:
        for index in INDICES:
            for task_scope in TASK_SCOPES:
                statistic = "{}_{}_{}".format(index, system_scope, task_scope)
                mean_key = "statistics_{}_mean".format(statistic)
                cint_key = "statistics_{}_cint".format(statistic)
                analytical_mean = float(analytical_result[mean_key])
                simulation_mean = float(simulation_result[mean_key])
                simulation_cint = float(simulation_result[cint_key])
                index_symbol = get_index_symbol(index, system_scope, task_scope)
                table += "${}$  & ${}$ & ${}\pm {}$ \\\\ \n".format(
                    index_symbol, analytical_mean, simulation_mean, simulation_cint
                )
        table += "\hline \n"

    return table


INDEX_SYMBOLS = {"population": "N_{{{}{}}}", "response": "T_{{{}{}}}", "throughput": "X_{{{}{}}}"}

SYSTEM_SCOPE_SYMBOLS = {
    SystemScope.SYSTEM.name.lower(): "sys",
    SystemScope.CLOUD.name.lower(): "cld",
    SystemScope.CLOUDLET.name.lower(): "clt",
}

TASK_SCOPE_SYMBOLS = {
    TaskScope.GLOBAL.name.lower(): "",
    TaskScope.TASK_1.name.lower(): ",1",
    TaskScope.TASK_2.name.lower(): ",2",
}


def get_index_symbol(index, system_scope, task_scope):
    return INDEX_SYMBOLS[index].format(SYSTEM_SCOPE_SYMBOLS[system_scope], TASK_SCOPE_SYMBOLS[task_scope])


if __name__ == "__main__":
    result_types = ["algorithm_1", "algorithm_2/threshold_5", "algorithm_2/threshold_20"]

    for result_type in result_types:
        analytical_result_path = "../../out/analytical_solution/{}/result.csv".format(result_type)
        simulation_result_path = "../../out/performance_analysis/{}/result.csv".format(result_type)
        latex_table = build_latex_table(analytical_result_path, simulation_result_path)
        print("RESULTS FOR:", result_type)
        print(latex_table)
