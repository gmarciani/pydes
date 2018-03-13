from core.statistics.batch_means import BatchedMeasure
from types import SimpleNamespace
from core.utils.csv_utils import save
from core.simulation.model.scope import SystemScope
from core.simulation.model.scope import TaskScope


NAN = float("nan")


class InstantaneousStatistics:
    """
    The set of instantaneous statistics for the simulation.
    """

    def __init__(self, t_now):
        """
        Create a new set of instantaneous statistics.
        """
        self.time = t_now
        self.metrics = SimpleNamespace(
            arrived={sys: {tsk: 0 for tsk in TaskScope} for sys in SystemScope},
            completed={sys: {tsk: 0 for tsk in TaskScope} for sys in SystemScope},
            switched={sys: {tsk: 0 for tsk in TaskScope} for sys in SystemScope},
            service={sys: {tsk: 0 for tsk in TaskScope} for sys in SystemScope},
            population={sys: {tsk: 0 for tsk in TaskScope} for sys in SystemScope},
            response={sys: {tsk: 0 for tsk in TaskScope} for sys in SystemScope},
            response_switched={sys: {tsk: 0 for tsk in TaskScope} for sys in SystemScope},
            throughput={sys: {tsk: 0 for tsk in TaskScope} for sys in SystemScope}
        )

    def save_csv(self, filename, append=False, skip_header=False):
        """
        Save the current statistics as CSV.
        :param filename: (string) the filename.
        :param append: (bool) if True, append to an existing file.
        :param skip_header: (bool) if True, skip the CSV header.
        :return: None
        """
        header = ["time"]
        sample = [self.time]

        for metric in sorted(self.metrics.__dict__):
            for sys in SystemScope:
                for tsk in TaskScope:
                    header.append("{}_{}_{}".format(metric, sys.name.lower(), tsk.name.lower()))
                    sample.append(getattr(self.metrics, metric)[sys][tsk])

        data = [sample]

        save(filename, header, data, append, skip_header)


class SimulationStatistics:
    """
    The set of statistics for the simulation.
    """

    def __init__(self, t_batch=None):
        """
        Create a new set of statistics.
        """

        # Metrics
        self.metrics = SimpleNamespace(
            arrived={sys: {tsk: BatchedMeasure() for tsk in TaskScope} for sys in SystemScope},
            completed={sys: {tsk: BatchedMeasure() for tsk in TaskScope} for sys in SystemScope},
            switched={sys: {tsk: BatchedMeasure() for tsk in TaskScope} for sys in SystemScope},
            service={sys: {tsk: BatchedMeasure() for tsk in TaskScope} for sys in SystemScope},
            population={sys: {tsk: BatchedMeasure() for tsk in TaskScope} for sys in SystemScope},
            response={sys: {tsk: BatchedMeasure() for tsk in TaskScope} for sys in SystemScope},
            response_switched={sys: {tsk: BatchedMeasure() for tsk in TaskScope} for sys in SystemScope},
            throughput={sys: {tsk: BatchedMeasure() for tsk in TaskScope} for sys in SystemScope},
        )

        # Batch management
        self.n_batches = 0
        self.t_batch = t_batch

    def register_batch(self):
        """
        Register and close the current batch statistics.
        :return: None
        """
        # Compute derived metrics
        for sys in SystemScope:
            for tsk in TaskScope:
                self.metrics.response[sys][tsk].set_value(
                    self.metrics.service[sys][tsk].get_value() / self.metrics.completed[sys][tsk].get_value()
                    if self.metrics.completed[sys][tsk].get_value() > 0 else 0
                )
                self.metrics.throughput[sys][tsk].set_value(
                    self.metrics.completed[sys][tsk].get_value() / self.t_batch
                )

        # Register all metrics
        for metric in self.metrics.__dict__:
            for sys in SystemScope:
                for tsk in TaskScope:
                    getattr(self.metrics, metric)[sys][tsk].register_batch()

        self.n_batches += 1

    def discard_batch(self):
        """
        Discard the current batch statistics.
        :return: None
        """
        for metric in self.metrics.__dict__:
            for sys in SystemScope:
                for tsk in TaskScope:
                    getattr(self.metrics, metric)[sys][tsk].discard_batch()

    def sample(self, t_now):
        """
        Get sample statistics.
        :param t_now: (float) the current time.
        :return: the instantaneous statistics.
        """
        stat = InstantaneousStatistics(t_now)

        for metric in stat.metrics.__dict__:
            for sys in SystemScope:
                for tsk in TaskScope:
                    if metric == "response":
                        stat.metrics.response[sys][tsk] = \
                            stat.metrics.service[sys][tsk] / stat.metrics.completed[sys][tsk] \
                                if stat.metrics.completed[sys][tsk] > 0 else 0.0
                    elif metric == "throughput":
                        stat.metrics.throughput[sys][tsk] = \
                            stat.metrics.completed[sys][tsk] / t_now if t_now > 0 else 0.0
                    else:
                        getattr(stat.metrics, metric)[sys][tsk] = getattr(self.metrics, metric)[sys][tsk].sample()

        return stat

    def save_csv(self, filename, append=False, skip_header=False, batch=None):
        """
        Save the current statistics as CSV.
        :param filename: (string) the filename.
        :param append: (bool) if True, append to an existing file.
        :param skip_header: (bool) if True, skip the CSV header.
        :param batch: (integer) the batch id. If None, all batches are saved.
        :return: None
        """
        header = ["batch"]
        data = []
        rng_batches = range(self.n_batches) if batch is None else range(batch, batch+1)
        for b in rng_batches:
            sample = [b]
            for metric in sorted(self.metrics.__dict__):
                for sys in SystemScope:
                    for tsk in TaskScope:
                        header.append("{}_{}_{}".format(metric, sys.name.lower(), tsk.name.lower()))
                        sample.append(getattr(self.metrics, metric)[sys][tsk].get_value(b))
            data.append(sample)

        save(filename, header, data, append, skip_header)