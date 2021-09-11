from core.simulation.model.scope import SystemScope, TaskScope
from core.utils.csv_utils import read_csv
from core.utils.report import SimpleReport as Report
from core.simulation.model.controller import ControllerAlgorithm

INDICES = ["population", "response", "throughput"]
SYSTEM_SCOPES = [scope.name.lower() for scope in SystemScope]
TASK_SCOPES = [scope.name.lower() for scope in TaskScope]


def validate(analytical_result_path, simulation_result_path):
    """
    Validates the simulation result against the analytical result.
    :param analytical_result_path: (string) the path of the analytical result file.
    :param simulation_result_path: (string) the path of the simulation result file.
    :return: (Report) validation report.
    """
    analytical_result = read_csv(analytical_result_path)[0]
    simulation_result = read_csv(simulation_result_path)[0]

    __verify_model_settings(analytical_result, simulation_result)

    statistics_matching = {}
    statistics_not_matching = {}

    for index in INDICES:
        for system_scope in SYSTEM_SCOPES:
            for task_scope in TASK_SCOPES:
                statistic = "{}_{}_{}".format(index, system_scope, task_scope)
                mean_key = "statistics_{}_mean".format(statistic)
                cint_key = "statistics_{}_cint".format(statistic)
                analytical_mean = float(analytical_result[mean_key])
                simulation_mean = float(simulation_result[mean_key])
                simulation_cint = float(simulation_result[cint_key])
                simulation_lower_bound = simulation_mean - simulation_cint
                simulation_upper_bound = simulation_mean + simulation_cint
                delta = (analytical_mean - simulation_mean) / simulation_cint
                if simulation_lower_bound <= analytical_mean <= simulation_upper_bound:
                    statistics_matching[statistic] = delta
                else:
                    statistics_not_matching[statistic] = delta

    report = Report("VALIDATION-CLOUD-CLOUDLET")

    for item in sorted(statistics_matching.items(), key=lambda item: abs(item[1]), reverse=True):
        statistic = item[0]
        delta = item[1]
        mean_key = "statistics_{}_mean".format(statistic)
        cint_key = "statistics_{}_cint".format(statistic)
        analytical_mean = float(analytical_result[mean_key])
        simulation_mean = float(simulation_result[mean_key])
        simulation_cint = float(simulation_result[cint_key])
        simulation_lower_bound = simulation_mean - simulation_cint
        simulation_upper_bound = simulation_mean + simulation_cint

        report.add(
            "matching",
            statistic,
            "{} inside [{},{}] with {}% semi-interval distance from the simulation mean {}".format(
                analytical_mean, simulation_lower_bound, simulation_upper_bound, delta * 100, simulation_mean
            ),
        )

    for item in sorted(statistics_not_matching.items(), key=lambda item: abs(item[1]), reverse=True):
        statistic = item[0]
        delta = item[1]
        mean_key = "statistics_{}_mean".format(statistic)
        cint_key = "statistics_{}_cint".format(statistic)
        analytical_mean = float(analytical_result[mean_key])
        simulation_mean = float(simulation_result[mean_key])
        simulation_cint = float(simulation_result[cint_key])
        simulation_lower_bound = simulation_mean - simulation_cint
        simulation_upper_bound = simulation_mean + simulation_cint

        report.add(
            "not matching",
            statistic,
            "{} outside [{},{}] with {}% semi-interval distance from the simulation mean {}".format(
                analytical_mean, simulation_lower_bound, simulation_upper_bound, delta * 100, simulation_mean
            ),
        )

    return report


def __verify_model_settings(analytical_result, simulation_result):
    system_keys = [
        "arrival_arrival_task_1_dist",
        "arrival_arrival_task_1_rate",
        "arrival_arrival_task_2_dist",
        "arrival_arrival_task_2_rate",
        "system_cloudlet_service_task_1_dist",
        "system_cloudlet_service_task_1_rate",
        "system_cloudlet_service_task_2_dist",
        "system_cloudlet_service_task_2_rate",
        "system_cloud_service_task_1_dist",
        "system_cloud_service_task_1_rate",
        "system_cloud_service_task_2_dist",
        "system_cloud_service_task_2_rate",
        "system_cloud_setup_task_2_dist",
        "system_cloud_service_task_2_param_m",
        "system_cloudlet_n_servers",
        "system_cloudlet_controller_algorithm",
    ]

    if analytical_result["system_cloudlet_controller_algorithm"] == ControllerAlgorithm.ALGORITHM_2:
        system_keys.append("system_cloudlet_threshold")

    for k in system_keys:
        analytical_value = analytical_result[k]
        simulation_value = simulation_result[k]
        assert (
            analytical_value == simulation_value
        ), "System characteristics must be equal: difference found in key {} with analytical value {} and simulation value {}".format(
            k, analytical_value, simulation_value
        )


if __name__ == "__main__":
    analytical_result_path = "../../out/analytical_solution/algorithm_2/threshold_3/result.csv"
    simulation_result_path = "../../out/performance_analysis/algorithm_2/threshold_3/result.csv"

    report = validate(analytical_result_path, simulation_result_path)

    print(report)
