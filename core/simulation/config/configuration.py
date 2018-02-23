import copy
import yaml

default_configuration = {

    "general": {
        "n_batch": 1,  # the number of batches
        "t_batch": 1000,  # the stop time for a batch (s) 1hour=3600, 1day=86400, 1week=604800, 1month=2.628e+6
        "confidence": 0.95,  # the level of confidence
        "random": {
            "generator": "MarcianiMultiStream",  # the class name of the random generator
            "seed": 123456789  # the initial seed for the random generator
        }
    },

    "tasks": {
        "arrival_rate_1": 3.25,  # the arrival rate for tasks of type 1 (tasks/s)
        "arrival_rate_2": 6.25  # the arrival rate for tasks of type 2 (tasks/s)
    },

    "system": {
        "cloudlet": {
            "service_rate_1": 0.45,  # the service rate for tasks of type 1 (tasks/s)
            "service_rate_2": 0.30,  # the service rate for tasks of type 2 (tasks/s)
            "n_servers": 20,  # the number of servers
            "threshold": 20,  # the occupancy threshold
            "server_selection": "ORDER"  # the server-selection rule
        },

        "cloud": {
            "service_rate_1": 0.25,  # the service rate for tasks of type 1 (tasks/s).
            "service_rate_2": 0.22,  # the service rate for tasks of type 2 (tasks/s).
            "t_setup_mean": 0.8  # the mean setup time to restart a task in the Cloud (s).
        }
    }
}


def get_default_configuration():
    """
    Get a copy of default configuration.
    :return: a copy of default configuration.
    """
    return copy.deepcopy(default_configuration)


def load_configuration(filename):
    """
    Load the configuration from a file.
    :param filename: (string) the file name.
    :return: (Configuration) the configuration.
    """
    with open(filename, "r") as config_file:
        config = yaml.load(config_file)
    return config


if __name__ == "__main__":
    # Creation
    config_1 = get_default_configuration()
    config_2 = get_default_configuration()

    # Equality check
    print("Config 1 equals Config 2 (before editing): {}".format(config_1 == config_2))
    config_2["general"]["t_stop"] = 25000
    print("Config 1 equals Config 2 (after editing): {}".format(config_1 == config_2))

