from core.metrics.batch_means import BatchedMeasure
from core.metrics.sampling import Sample
from types import SimpleNamespace
from core.utils.csv_utils import save_csv
from core.simulation.model.scope import SystemScope
from core.simulation.model.scope import TaskScope


NAN = float("nan")


class SimulationStatistics:
    """
    The set of statistics for the simulation.
    """

    def __init__(self, target_batchdim):
        """
        Create a new set of statistics.
        :param target_batchdim: (int) the desired batch dimension (Default: infinite)
        """

        # Counters
        self.counters = SimpleNamespace(
            arrived={sys: {tsk: 0 for tsk in TaskScope} for sys in SystemScope},
            completed={sys: {tsk: 0 for tsk in TaskScope} for sys in SystemScope},
            service={sys: {tsk: 0 for tsk in TaskScope} for sys in SystemScope},
            switched={sys: {tsk: 0 for tsk in TaskScope} for sys in SystemScope},
            switched_completed={sys: {tsk: 0 for tsk in TaskScope} for sys in SystemScope},
            switched_service={sys: {tsk: 0 for tsk in TaskScope} for sys in SystemScope},
            level_x={sys: {tsk: 0 for tsk in TaskScope} for sys in SystemScope},
            level_l={sys: {tsk: 0 for tsk in TaskScope} for sys in SystemScope}
        )

        # Performance Metrics
        self.metrics = SimpleNamespace(
            response={sys: {tsk: BatchedMeasure() for tsk in TaskScope} for sys in SystemScope},
            throughput={sys: {tsk: BatchedMeasure() for tsk in TaskScope} for sys in SystemScope},
            switched_ratio={sys: {tsk: BatchedMeasure() for tsk in TaskScope} for sys in SystemScope},
            switched_response={sys: {tsk: BatchedMeasure() for tsk in TaskScope} for sys in SystemScope},
            switched_service_lost={sys: {tsk: BatchedMeasure() for tsk in TaskScope} for sys in SystemScope},
            population={sys: {tsk: BatchedMeasure() for tsk in TaskScope} for sys in SystemScope},
            utilization={sys: {tsk: BatchedMeasure() for tsk in TaskScope} for sys in SystemScope}
        )

        # Batch management
        self.n_samples = 0
        self.n_batches = 0
        self.curr_batchdim = 0
        self.target_batchdim = target_batchdim

    def sample(self, t_now):
        """
        Registers a new sample in batch statistics and return sample values.
        :param t_now: (float) the current time.
        :return: the instantaneous statistics.
        """
        # Compute counters
        self._compute_counters(t_now)
        # Compute aggregated counters and performance metrics.
        # Computed values are added as sample in batches.
        self._compute_metrics(t_now)

        sample = Sample(t_now)

        # Sample counters and metrics
        for counter in sample.counters.__dict__:
            for sys in SystemScope:
                for tsk in TaskScope:
                    sample_value = getattr(self.counters, counter)[sys][tsk]
                    getattr(sample.counters, counter)[sys][tsk] = sample_value

        for metric in sample.metrics.__dict__:
            for sys in SystemScope:
                for tsk in TaskScope:
                    sample_value = getattr(self.metrics, metric)[sys][tsk].sample()
                    getattr(sample.metrics, metric)[sys][tsk] = sample_value

        self.n_samples += 1
        self.curr_batchdim += 1

        if self.curr_batchdim == self.target_batchdim:
            self._close_batch(t_now)
            self.n_batches += 1
            self.curr_batchdim = 0

        return sample

    def _close_batch(self, t_now):
        """
        Register and close the current batch metrics.
        :param t_now: (float) the current time.
        :return: None
        """

        # Register all metrics
        for metric in self.metrics.__dict__:
            for sys in SystemScope:
                for tsk in TaskScope:
                    getattr(self.metrics, metric)[sys][tsk].register_batch()

    def discard_data(self):
        """
        Discard the current batch statistics.
        :return: None
        """
        for metric in self.metrics.__dict__:
            for sys in SystemScope:
                for tsk in TaskScope:
                    getattr(self.metrics, metric)[sys][tsk].discard_data()

        self.n_batches = 0
        self.curr_batchdim = 0

    def _compute_counters(self, t_now):
        """
        Compute aggregated counters, i.e. aggregated counters for global tasks and system scope.
        :param t_now (float) the current time,
        :return: None
        """
        # Compute counters for SystemScope.SYSTEM
        #   * arrived_system = arrived_cloudlet + arrived_cloud
        #   * completed_system = completed_cloudlet + completed_cloud
        #   * service_system = service_cloudlet + service_cloud
        #   * switched_system = switched_cloudlet (or switched_cloud, as they are equal)
        #   * switched_completed_system = switched_completed_cloud
        #   * switched_service_system = switched_service_cloudlet + switched_service_cloud
        for tsk in TaskScope.concrete():
            self.counters.arrived[SystemScope.SYSTEM][tsk] = sum(self.counters.arrived[sys][tsk] for sys in SystemScope.subsystems())
            self.counters.completed[SystemScope.SYSTEM][tsk] = sum(self.counters.completed[sys][tsk] for sys in SystemScope.subsystems())
            self.counters.service[SystemScope.SYSTEM][tsk] = sum(self.counters.service[sys][tsk] for sys in SystemScope.subsystems())
            self.counters.switched[SystemScope.SYSTEM][tsk] = self.counters.switched[SystemScope.CLOUDLET][tsk]
            self.counters.switched_completed[SystemScope.SYSTEM][tsk] = self.counters.switched_completed[SystemScope.CLOUD][tsk]
            self.counters.switched_service[SystemScope.SYSTEM][tsk] = sum(self.counters.switched_service[sys][tsk] for sys in SystemScope.subsystems())

        # Compute counters for TaskScope.GLOBAL:
        #   * arrived_global = arrived_task_1 + arrived_task_2
        #   * completed_global = completed_task_1 + completed_task_2
        #   * service_global = service_task_1 + service_task_2
        #   * switched_global = switched_task_1 + switched_task_2
        #   * switched_completed_global = switched_completed_task_1 + switched_completed_task_2
        #   * switched_service_global = switched_service_task_1 + switched_service_task_2
        for sys in SystemScope:
            self.counters.arrived[sys][TaskScope.GLOBAL] = sum(self.counters.arrived[sys][tsk] for tsk in TaskScope.concrete())
            self.counters.completed[sys][TaskScope.GLOBAL] =  sum(self.counters.completed[sys][tsk] for tsk in TaskScope.concrete())
            self.counters.service[sys][TaskScope.GLOBAL] = sum(self.counters.service[sys][tsk] for tsk in TaskScope.concrete())
            self.counters.switched[sys][TaskScope.GLOBAL] = sum(self.counters.switched[sys][tsk] for tsk in TaskScope.concrete())
            self.counters.switched_completed[sys][TaskScope.GLOBAL] = sum(self.counters.switched_completed[sys][tsk] for tsk in TaskScope.concrete())
            self.counters.switched_service[sys][TaskScope.GLOBAL] = sum(self.counters.switched_service[sys][tsk] for tsk in TaskScope.concrete())

    def _compute_metrics(self, t_now):
        """
        Compute performance metrics leveraging counters values.
        :param t_now (float) the current time,
        :return: None
        """
        # Compute performance metrics:
        #   * response = service / completed
        #   * throughput = completed / t_now
        #   * switched_ratio = switched / arrived
        #   * switched_response = switched_service / switched_completed
        #   * switched_service_lost = switched_service / switched
        #   * population = level_x / t_now
        #   * utilization = level_l / t_now
        #t_now_shifted = t_now - self.t_batch_start
        #if t_now_shifted < 0:
        #    raise RuntimeError("t_now={} t_batch_start={} t_now_shifted={}".format(t_now, self.t_batch_start, t_now_shifted))
        for sys in SystemScope:
            for tsk in TaskScope:
                self.metrics.response[sys][tsk].set_value(
                    (self.counters.service[sys][tsk] / self.counters.completed[sys][tsk])
                    if self.counters.completed[sys][tsk] > 0 else 0)

                self.metrics.throughput[sys][tsk].set_value(
                    self.counters.completed[sys][tsk] / t_now)

                self.metrics.switched_ratio[sys][tsk].set_value(
                    (self.counters.switched[sys][tsk] / self.counters.arrived[sys][tsk])
                    if self.counters.arrived[sys][tsk] > 0 else 0)

                self.metrics.switched_response[sys][tsk].set_value(
                    (self.counters.switched_service[sys][tsk] / self.counters.switched_completed[sys][tsk])
                    if self.counters.switched_completed[sys][tsk] > 0 else 0)

                if sys is SystemScope.CLOUDLET:
                    self.metrics.switched_service_lost[sys][tsk].set_value(
                        (self.counters.switched_service[sys][tsk] / self.counters.switched[sys][tsk])
                        if self.counters.switched[sys][tsk] > 0 else 0)

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

        save_csv(filename, header, data, append, skip_header)


if __name__ == "__main__":
    s = Sample(0)

    s.metrics.arrived[SystemScope.CLOUDLET][TaskScope.TASK_1] = 1
    s.metrics.arrived[SystemScope.CLOUDLET][TaskScope.TASK_2] = 2
    s.metrics.arrived[SystemScope.CLOUD][TaskScope.TASK_1] = 3
    s.metrics.arrived[SystemScope.CLOUD][TaskScope.TASK_2] = 4

    for tsk in TaskScope.concrete():
        s.metrics.arrived[SystemScope.SYSTEM][tsk] = sum(s.metrics.arrived[sys][tsk] for sys in SystemScope.subsystems())

    for tsk in TaskScope.concrete():
        print(s.metrics.arrived[SystemScope.SYSTEM][tsk])