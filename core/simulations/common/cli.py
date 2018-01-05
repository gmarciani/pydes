import argparse

def CmdParser():
    parser = argparse.ArgumentParser(prog="Demule", description="A pythonic discrete-event simulation suite")
    parser.add_argument("simulation", help="Simulation name (default: cloud)")
    parser.add_argument("--config", help="Configuration file (default: simulation.yaml or default)")
    parser.add_argument("--replications", help="Number of replications (default: 1)")
    parser.add_argument("--log", help="Log level (default: INFO)")
    return parser