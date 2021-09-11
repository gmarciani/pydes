from types import SimpleNamespace

from pydes.core.simulation.model.scope import SystemScope, TaskScope
from pydes.core.utils.csv_utils import save_csv

NAN = float("nan")


class Sample:
    """
    The set of instantaneous sample.
    """

    def __init__(self, t_now):
        """
        Create a new set of instantaneous sample.
        """
        self.time = t_now

        # Counters
        self.counters = SimpleNamespace(
            arrived={sys: {tsk: 0 for tsk in TaskScope} for sys in SystemScope},
            completed={sys: {tsk: 0 for tsk in TaskScope} for sys in SystemScope},
            service={sys: {tsk: 0 for tsk in TaskScope} for sys in SystemScope},
            switched={sys: {tsk: 0 for tsk in TaskScope} for sys in SystemScope},
            switched_completed={sys: {tsk: 0 for tsk in TaskScope} for sys in SystemScope},
            switched_service={sys: {tsk: 0 for tsk in TaskScope} for sys in SystemScope},
            switched_service_lost={sys: {tsk: 0 for tsk in TaskScope} for sys in SystemScope},
            population_area={sys: {tsk: 0 for tsk in TaskScope} for sys in SystemScope},
        )

        # Performance Metrics
        self.performance_metrics = SimpleNamespace(
            response={sys: {tsk: 0.0 for tsk in TaskScope} for sys in SystemScope},
            throughput={sys: {tsk: 0.0 for tsk in TaskScope} for sys in SystemScope},
            population={sys: {tsk: 0.0 for tsk in TaskScope} for sys in SystemScope},
            switched_ratio={sys: {tsk: 0.0 for tsk in TaskScope} for sys in SystemScope},
            switched_response={sys: {tsk: 0.0 for tsk in TaskScope} for sys in SystemScope},
            service_lost={sys: {tsk: 0.0 for tsk in TaskScope} for sys in SystemScope},
        )

    def save_csv(self, filename, append=False, skip_header=False):
        """
        Save the current sample as CSV.
        :param filename: (string) the filename.
        :param append: (bool) if True, append to an existing file.
        :param skip_header: (bool) if True, skip the CSV header.
        :return: None
        """
        header = ["time"]
        sample = [self.time]

        for counter in sorted(self.counters.__dict__):
            for sys in SystemScope:
                for tsk in TaskScope:
                    header.append("{}_{}_{}".format(counter, sys.name.lower(), tsk.name.lower()))
                    sample.append(getattr(self.counters, counter)[sys][tsk])

        for performance_metric in sorted(self.performance_metrics.__dict__):
            for sys in SystemScope:
                for tsk in TaskScope:
                    header.append("{}_{}_{}".format(performance_metric, sys.name.lower(), tsk.name.lower()))
                    sample.append(getattr(self.performance_metrics, performance_metric)[sys][tsk])

        data = [sample]

        save_csv(filename, header, data, append, skip_header)


if __name__ == "__main__":
    s = Sample(0)

    s.counters.arrived[SystemScope.CLOUDLET][TaskScope.TASK_1] = 1
    s.counters.arrived[SystemScope.CLOUDLET][TaskScope.TASK_2] = 2
    s.counters.arrived[SystemScope.CLOUD][TaskScope.TASK_1] = 3
    s.counters.arrived[SystemScope.CLOUD][TaskScope.TASK_2] = 4

    for tsk in TaskScope.concrete():
        s.counters.arrived[SystemScope.SYSTEM][tsk] = sum(
            s.counters.arrived[sys][tsk] for sys in SystemScope.subsystems()
        )

    for tsk in TaskScope.concrete():
        print(s.counters.arrived[SystemScope.SYSTEM][tsk])
