default_configuration = {
    "general": {
        "t_stop": 10000,
        "replica": 1,
        "random": {
            "generator": "MarcianiMultiStream",
            "seed": 123456789
        }
    },
    "cloudlet": {
        "n_servers": 10
    },
    "cloud": {
        "t_service_rate_1": 0.25,
        "t_service_rate_2": 0.35,
        "t_setup": 45
    }

}


if __name__ == "__main__":
    print("Default Configuration:", default_configuration)