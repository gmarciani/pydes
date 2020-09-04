from types import SimpleNamespace
from core.utils.csv_utils import save_csv
from core.simulation.model.scope import SystemScope
from core.simulation.model.scope import TaskScope


NAN = float("nan")


class AnalyticalSolution:
    """
    The analytical solution.
    """

    def __init__(self):
        """
        Create a new analytical solution.
        """

        # Performance Metrics
        self.performance_metrics = SimpleNamespace(
            response={sys: {tsk: 0.0 for tsk in TaskScope} for sys in SystemScope},
            throughput={sys: {tsk: 0.0 for tsk in TaskScope} for sys in SystemScope},
            population={sys: {tsk: 0.0 for tsk in TaskScope} for sys in SystemScope},
            switched_ratio={sys: {tsk: 0.0 for tsk in TaskScope} for sys in SystemScope}
        )

    def save_csv(self, filename, append=False, skip_header=False):
        """
        Save the current analytical solution as CSV.
        :param filename: (string) the filename.
        :param append: (bool) if True, append to an existing file.
        :param skip_header: (bool) if True, skip the CSV header.
        :return: None
        """
        header = []
        solution = []

        for performance_metric in sorted(self.performance_metrics.__dict__):
            for sys in SystemScope:
                for tsk in TaskScope:
                    header.append("{}_{}_{}".format(performance_metric, sys.name.lower(), tsk.name.lower()))
                    solution.append(getattr(self.performance_metrics, performance_metric)[sys][tsk])

        data = [solution]

        save_csv(filename, header, data, append, skip_header)