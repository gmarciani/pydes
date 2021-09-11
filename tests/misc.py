from core.rnd.rndgen import MarcianiMultiStream
from core.rnd.rndvar import Variate
from core.simulation.model.scope import TaskScope

rndgen = MarcianiMultiStream()

rndparams = {
    TaskScope.TASK_1: {"distribution": "EXPONENTIAL", "distribution_params": {"m": 0.5}},
    TaskScope.TASK_2: {"distribution": "EXPONENTIAL", "distribution_params": {"m": 0.8}},
}

variates = {
    tsk: lambda u: Variate[rndparams[tsk]["distribution"]].vargen.generate(u=u, **rndparams[tsk]["distribution_params"])
    for tsk in TaskScope.concrete()
}


def get_service_time(tsk):
    return variates[tsk](u=rndgen)


if __name__ == "__main__":

    values = {tsk: [] for tsk in TaskScope.concrete()}

    for tsk in TaskScope.concrete():
        for i in range(10):
            t = get_service_time(tsk)
            values[tsk].append(t)
