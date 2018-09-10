import copy
import yaml

from core.simulation.model.scope import TaskScope
from core.random.rndvar import Variate
from core.simulation.model.server_selection import SelectionRule
from core.simulation.simulation_mode import SimulationMode


_default_configuration = {

    "general": {
        #"mode": "PERFORMANCE_ANALYSIS",  # the simulation mode

        # Required for TRANSIENT_ANALYSIS
        #"t_stop": 3600,  # the stop time for the simulation (s) 1hour=3600, 1day=86400, 1week=604800, 1month=2.628e+6

        # Required for PERFORMANCE_ANALYSIS
        #"batches": 64,  # the number of batches
        #"batchdim": 512,  # the batch dimension
        #"t_tran": 0,  # the transient time

        "t_sample": 1,  # the sampling interval (sec)
        "confidence": 0.95,  # the level of confidence
        "random": {
            "generator": "MarcianiMultiStream",  # the class name of the random generator
            "seed": 123456789  # the initial seed for the random generator
        }
    },

    "arrival": {
        "TASK_1": {
            "distribution": "EXPONENTIAL",
            "parameters": {
                "r": 6.00  # the arrival rate for tasks of type 1 (tasks/s)
            }
        },
        "TASK_2": {
            "distribution": "EXPONENTIAL",
            "parameters": {
                "r": 6.25  # the arrival rate for tasks of type 2 (tasks/s)
            }
        }
    },

    "system": {
        "cloudlet": {
            "n_servers": 20,  # the number of servers
            "threshold": 20,  # the occupancy threshold
            "server_selection": "ORDER",  # the server-selection rule
            "service": {
                "TASK_1": {
                    "distribution": "EXPONENTIAL",
                    "parameters": {
                        "r": 0.45  # the service rate for tasks of type 1 (tasks/s)
                    }
                },
                "TASK_2": {
                    "distribution": "EXPONENTIAL",
                    "parameters": {
                        "r": 0.27  # the service rate for tasks of type 2 (tasks/s)
                    }
                }
            }
        },

        "cloud": {
            "service": {
                "TASK_1": {
                    "distribution": "EXPONENTIAL",
                    "parameters": {
                        "r": 0.25  # the service rate for tasks of type 1 (tasks/s)
                    }
                },
                "TASK_2": {
                    "distribution": "EXPONENTIAL",
                    "parameters": {
                        "r": 0.22  # the service rate for tasks of type 2 (tasks/s)
                    }
                }
            },
            "setup": {
                "TASK_1": {
                    "distribution": "DETERMINISTIC",
                    "parameters": {
                        "v": 0  # the value of the setup time to restart a task of type 1 in the Cloud (s).
                    }
                },
                "TASK_2": {
                    "distribution": "EXPONENTIAL",
                    "parameters": {
                        "m": 0.8  # the mean value of the setup time to restart a task 2 in the Cloud (s).
                    }
                }
            }
        }
    }
}


def get_default_configuration(simulation_mode):
    """
    Get a copy of default configuration.
    :param simulation_mode (SimulationMode) the simulation mode of execution.
    :return: a copy of default configuration.
    """
    config = copy.deepcopy(_default_configuration)

    # Add configuration specific to transient analysis
    if simulation_mode is SimulationMode.TRANSIENT_ANALYSIS:
        config["general"]["mode"] = "TRANSIENT_ANALYSIS"
        config["general"]["t_stop"] = 3600

    # Add configuration specific to performance analysis
    elif simulation_mode is SimulationMode.PERFORMANCE_ANALYSIS:
        config["general"]["mode"] = "PERFORMANCE_ANALYSIS"
        config["general"]["t_tran"] = 2000
        config["general"]["batches"] = 10
        config["general"]["batchdim"] = 100

    normalize(config)

    return config


def load_configuration(filename, norm=True):
    """
    Load the configuration from a file.
    :param filename: (string) the file name.
    :return: (Configuration) the configuration.
    """
    with open(filename, "r") as config_file:
        config = yaml.load(config_file)
    if norm:
        normalize(config)
    return config


def normalize(config):
    """
    Normalize the format of the configuration.
    :param config: the configuration.
    :return: None
    """
    config["general"]["mode"] = SimulationMode[config["general"]["mode"]]
    _normalize_random_config(config["arrival"])
    _normalize_random_config(config["system"]["cloudlet"]["service"])
    _normalize_random_config(config["system"]["cloud"]["service"])
    _normalize_random_config(config["system"]["cloud"]["setup"])
    config["system"]["cloudlet"]["server_selection"] = SelectionRule[config["system"]["cloudlet"]["server_selection"]]


def _normalize_random_config(entry):
    """
    Normalize the random entry.
    :param entry: the random entry.
    :return: None
    """
    for tsk in entry.keys():
        entry[tsk]["distribution"] = Variate[entry[tsk]["distribution"]]
        if entry[tsk]["distribution"] is Variate.EXPONENTIAL and "r" in entry[tsk]["parameters"]:
            entry[tsk]["parameters"]["m"] = 1.0 / entry[tsk]["parameters"]["r"]
            del entry[tsk]["parameters"]["r"]
        entry[TaskScope[tsk]] = entry.pop(tsk)


if __name__ == "__main__":

    # Transient Analysis
    config_1 = get_default_configuration(SimulationMode.TRANSIENT_ANALYSIS)
    print(config_1)

    # Performance Analysis
    config_2 = get_default_configuration(SimulationMode.PERFORMANCE_ANALYSIS)
    print(config_2)

