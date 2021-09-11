from types import SimpleNamespace

from pydes.core.metrics.batch_means import BatchedMeasure
from pydes.core.metrics.sampling import Sample
from pydes.core.simulation.model.scope import SystemScope, TaskScope
from pydes.core.utils.csv_utils import save_csv

NAN = float("nan")


class SimulationMetrics:
    """
    The manager of simulation metrics, i.e. simulation counters and performance metrics.
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
            switched_service_lost={sys: {tsk: 0 for tsk in TaskScope} for sys in SystemScope},
            population_area={sys: {tsk: 0 for tsk in TaskScope} for sys in SystemScope},
        )

        # Performance Metrics
        self.performance_metrics = SimpleNamespace(
            response={sys: {tsk: BatchedMeasure() for tsk in TaskScope} for sys in SystemScope},
            throughput={sys: {tsk: BatchedMeasure() for tsk in TaskScope} for sys in SystemScope},
            population={sys: {tsk: BatchedMeasure() for tsk in TaskScope} for sys in SystemScope},
            switched_ratio={sys: {tsk: BatchedMeasure() for tsk in TaskScope} for sys in SystemScope},
            switched_response={sys: {tsk: BatchedMeasure() for tsk in TaskScope} for sys in SystemScope},
            service_lost={sys: {tsk: BatchedMeasure() for tsk in TaskScope} for sys in SystemScope},
        )

        # Batch management
        self.n_samples = 0
        self.n_batches = 0
        self.curr_batchdim = 0
        self.target_batchdim = target_batchdim

    def sampling(self, t_now):
        """
        Registers a new batch sample and return sample values.
        :param t_now: (float) the current time.
        :return: (Sample) the instantaneous sample.
        """
        self._compute_global_counters(t_now)

        # Update performance metrics
        self._compute_performance_metrics(t_now)

        # Build the instantaneous sample
        sample = self.build_sample(t_now)

        self.n_samples += 1
        self.curr_batchdim += 1

        if self.curr_batchdim == self.target_batchdim:
            self._register_batch()
            self.n_batches += 1
            self.curr_batchdim = 0

        return sample

    def build_sample(self, t_now):
        """
        Builds the instantaneous sample for metrics.
        This is a snapshot of current metrics.
        :param t_now: (float) the current time.
        :return: (Sample) the instantaneous sample for metrics.
        """
        sample = Sample(t_now)

        # Sample counters and metrics
        for counter in sample.counters.__dict__:
            for sys in SystemScope:
                for tsk in TaskScope:
                    sample_value = getattr(self.counters, counter)[sys][tsk]
                    getattr(sample.counters, counter)[sys][tsk] = sample_value

        for performance_metric in sample.performance_metrics.__dict__:
            for sys in SystemScope:
                for tsk in TaskScope:
                    sample_value = getattr(self.performance_metrics, performance_metric)[sys][tsk].get_value()
                    getattr(sample.performance_metrics, performance_metric)[sys][tsk] = sample_value

        return sample

    def discard_data(self):
        """
        Discard all batch data.
        :return: None
        """
        for performance_metric in self.performance_metrics.__dict__:
            for sys in SystemScope:
                for tsk in TaskScope:
                    getattr(self.performance_metrics, performance_metric)[sys][tsk].discard_data()

        self.n_batches = 0
        self.curr_batchdim = 0
        self.n_samples = 0

    def _compute_global_counters(self, t_now):
        """
        Updates aggregated counters (e.g. system global counters) using task-scoped and subsystem-scoped counters
        (e.g. counter for task 1 in Cloudlet).
        :param t_now (float) the current time,
        :return: None
        """
        # Compute counters for each task class in system
        #   * arrived_system = arrived_cloudlet + arrived_cloud
        #   * completed_system = completed_cloudlet + completed_cloud
        #   * service_system = service_cloudlet + service_cloud
        #   * switched_system = switched_cloudlet
        #   * switched_completed_system = switched_completed_cloud
        #   * switched_service_system = switched_service_cloudlet + switched_service_cloud
        #   * switched_service_lost_system = switched_service_lost_cloudlet + switched_service_lost_cloud
        #   * population_area_system = population_area_cloudlet + population_area_lost_cloud
        for tsk in TaskScope.concrete():
            self.counters.arrived[SystemScope.SYSTEM][tsk] = sum(
                self.counters.arrived[sys][tsk] for sys in SystemScope.subsystems()
            )
            self.counters.completed[SystemScope.SYSTEM][tsk] = sum(
                self.counters.completed[sys][tsk] for sys in SystemScope.subsystems()
            )
            self.counters.service[SystemScope.SYSTEM][tsk] = sum(
                self.counters.service[sys][tsk] for sys in SystemScope.subsystems()
            )
            self.counters.switched[SystemScope.SYSTEM][tsk] = self.counters.switched[SystemScope.CLOUDLET][tsk]
            self.counters.switched_completed[SystemScope.SYSTEM][tsk] = self.counters.switched_completed[
                SystemScope.CLOUD
            ][tsk]
            self.counters.switched_service[SystemScope.SYSTEM][tsk] = sum(
                self.counters.switched_service[sys][tsk] for sys in SystemScope.subsystems()
            )
            self.counters.switched_service_lost[SystemScope.SYSTEM][tsk] = sum(
                self.counters.switched_service_lost[sys][tsk] for sys in SystemScope.subsystems()
            )
            self.counters.population_area[SystemScope.SYSTEM][tsk] = sum(
                self.counters.population_area[sys][tsk] for sys in SystemScope.subsystems()
            )

        # Compute counters for global tasks
        #   * arrived_global = arrived_task_1 + arrived_task_2
        #   * completed_global = completed_task_1 + completed_task_2
        #   * service_global = service_task_1 + service_task_2
        #   * switched_global = switched_task_1 + switched_task_2
        #   * switched_completed_global = switched_completed_task_1 + switched_completed_task_2
        #   * switched_service_global = switched_service_task_1 + switched_service_task_2
        #   * switched_service_lost_global = switched_service_lost_task_1 + switched_service_lost_task_2
        #   * population_area_global = population_area_task_1 + population_area_task_2
        for sys in SystemScope:
            self.counters.arrived[sys][TaskScope.GLOBAL] = sum(
                self.counters.arrived[sys][tsk] for tsk in TaskScope.concrete()
            )
            self.counters.completed[sys][TaskScope.GLOBAL] = sum(
                self.counters.completed[sys][tsk] for tsk in TaskScope.concrete()
            )
            self.counters.service[sys][TaskScope.GLOBAL] = sum(
                self.counters.service[sys][tsk] for tsk in TaskScope.concrete()
            )
            self.counters.switched[sys][TaskScope.GLOBAL] = sum(
                self.counters.switched[sys][tsk] for tsk in TaskScope.concrete()
            )
            self.counters.switched_completed[sys][TaskScope.GLOBAL] = sum(
                self.counters.switched_completed[sys][tsk] for tsk in TaskScope.concrete()
            )
            self.counters.switched_service[sys][TaskScope.GLOBAL] = sum(
                self.counters.switched_service[sys][tsk] for tsk in TaskScope.concrete()
            )
            self.counters.switched_service_lost[sys][TaskScope.GLOBAL] = sum(
                self.counters.switched_service_lost[sys][tsk] for tsk in TaskScope.concrete()
            )
            self.counters.population_area[sys][TaskScope.GLOBAL] = sum(
                self.counters.population_area[sys][tsk] for tsk in TaskScope.concrete()
            )

    def _compute_performance_metrics(self, t_now):
        """
        Updates performance metrics using counters values.
        The new updated values are used as batch samples.
        :param t_now (float) the current time.
        :return: None
        """
        # Compute performance metrics:
        #   * response = service / completed
        #   * throughput = completed / t_now
        #   * population = population_area / t_now
        #   * switched_ratio = switched / arrived
        #   * switched_response = switched_service / switched_completed
        #   * service_lost = switched_service_lost / switched
        for sys in SystemScope:
            for tsk in TaskScope:
                self.performance_metrics.response[sys][tsk].add_sample(
                    (self.counters.service[sys][tsk] / self.counters.completed[sys][tsk])
                    if self.counters.completed[sys][tsk] > 0
                    else 0.0
                )

                self.performance_metrics.throughput[sys][tsk].add_sample(self.counters.completed[sys][tsk] / t_now)

                self.performance_metrics.population[sys][tsk].add_sample(
                    self.counters.population_area[sys][tsk] / t_now
                )

                self.performance_metrics.switched_ratio[sys][tsk].add_sample(
                    (self.counters.switched[sys][tsk] / self.counters.arrived[sys][tsk])
                    if self.counters.arrived[sys][tsk] > 0
                    else 0.0
                )

                self.performance_metrics.switched_response[sys][tsk].add_sample(
                    (self.counters.switched_service[sys][tsk] / self.counters.switched_completed[sys][tsk])
                    if self.counters.switched_completed[sys][tsk] > 0
                    else 0.0
                )

                self.performance_metrics.service_lost[sys][tsk].add_sample(
                    (self.counters.switched_service_lost[sys][tsk] / self.counters.switched[sys][tsk])
                    if self.counters.switched[sys][tsk] > 0
                    else 0.0
                )

    def _register_batch(self):
        """
        Registers the current batch of all performance metrics.
        :return: None
        """
        for performance_metric in self.performance_metrics.__dict__:
            for sys in SystemScope:
                for tsk in TaskScope:
                    getattr(self.performance_metrics, performance_metric)[sys][tsk].register_batch()

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
        rng_batches = range(self.n_batches) if batch is None else range(batch, batch + 1)
        for b in rng_batches:
            sample = [b]
            for metric in sorted(self.performance_metrics.__dict__):
                for sys in SystemScope:
                    for tsk in TaskScope:
                        header.append("{}_{}_{}".format(metric, sys.name.lower(), tsk.name.lower()))
                        sample.append(getattr(self.performance_metrics, metric)[sys][tsk].get_value(b))
            data.append(sample)

        save_csv(filename, header, data, append, skip_header)
