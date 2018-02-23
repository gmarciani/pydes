from core.simulation.model.task import Task
from core.simulation.model.scope import Scope

if __name__ == "__main__":
    d1 = {
        Scope.CLOUD: {
            Task.TASK_1: 0.1,
            Task.TASK_2: 0.1
        },
        Scope.CLOUDLET: {
            Task.TASK_1: 0.1,
            Task.TASK_2: 0.1
        },
        Scope.SYSTEM: {
            Task.TASK_1: 0.1,
            Task.TASK_2: 0.1
        }
    }

    d2 = {scope: {task: 0.1 for task in Task} for scope in Scope}

    print(d1 == d2)

    print("sum=", sum([v for v in [k2 for k2 in d2.values()]]))

    l1 = [1,2,3]
    l2 = [4,5,6]
    l3 = [1,2,3,4,5,6]

    l1.extend(l2)

    print(l1 == l3)