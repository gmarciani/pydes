default_configuration = {

    "general": {
        "t_stop": 10000,  # the stop time (s)
        "replica": 1,  # the number of simulation replica
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
            "n_servers": 20,  # the number of servers
            "service_rate_1": 0.45,  # the service rate for tasks of type 1 (tasks/s)
            "service_rate_2": 0.30,  # the service rate for tasks of type 2 (tasks/s)
            "threshold": 20  # the occupancy threshold
        },

        "cloud": {
            "service_rate_1": 0.25,  # the service rate for job of type 1 (tasks/s).
            "service_rate_2": 0.22,  # the service rate for job of type 2 (tasks/s).
            "t_setup_mean": 0.8  # the mean setup time to restart a task of type 2 in the Cloud (s).
        }
    }
}


if __name__ == "__main__":
    print("Default Configuration:", default_configuration)