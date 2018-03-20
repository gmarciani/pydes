from core.stats.batch_means import BatchedMeasure
from core.stats.batch_means import BatchedSampleMeasure
from types import SimpleNamespace
from core.utils.csv_utils import save_csv
from core.simulation.model.scope import SystemScope
from core.simulation.model.scope import TaskScope
from core.utils.logutils import get_logger


# Logging
logger = get_logger(__name__)


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
            # Counters
            arrived={sys: {tsk: 0.0 for tsk in TaskScope} for sys in SystemScope},
            completed={sys: {tsk: 0.0 for tsk in TaskScope} for sys in SystemScope},
            service={sys: {tsk: 0.0 for tsk in TaskScope} for sys in SystemScope},
            switched={sys: {tsk: 0.0 for tsk in TaskScope} for sys in SystemScope},
            switched_completed={sys: {tsk: 0.0 for tsk in TaskScope} for sys in SystemScope},
            switched_service={sys: {tsk: 0.0 for tsk in TaskScope} for sys in SystemScope},
            population={sys: {tsk: 0.0 for tsk in TaskScope} for sys in SystemScope},

            # Derived
            response={sys: {tsk: 0.0 for tsk in TaskScope} for sys in SystemScope},
            throughput={sys: {tsk: 0.0 for tsk in TaskScope} for sys in SystemScope},
            switched_ratio={sys: {tsk: 0.0 for tsk in TaskScope} for sys in SystemScope},
            switched_response={sys: {tsk: 0.0 for tsk in TaskScope} for sys in SystemScope},
            switched_throughput={sys: {tsk: 0.0 for tsk in TaskScope} for sys in SystemScope}
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

        save_csv(filename, header, data, append, skip_header)


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

            # Counters
            arrived={sys: {tsk: BatchedMeasure() for tsk in TaskScope} for sys in SystemScope},
            completed={sys: {tsk: BatchedMeasure() for tsk in TaskScope} for sys in SystemScope},
            service={sys: {tsk: BatchedMeasure() for tsk in TaskScope} for sys in SystemScope},
            switched={sys: {tsk: BatchedMeasure() for tsk in TaskScope} for sys in SystemScope},
            switched_completed={sys: {tsk: BatchedMeasure() for tsk in TaskScope} for sys in SystemScope},
            switched_service={sys: {tsk: BatchedMeasure() for tsk in TaskScope} for sys in SystemScope},
            population={sys: {tsk: BatchedSampleMeasure() for tsk in TaskScope} for sys in SystemScope},

            # Derived
            response={sys: {tsk: BatchedMeasure() for tsk in TaskScope} for sys in SystemScope},
            throughput={sys: {tsk: BatchedMeasure() for tsk in TaskScope} for sys in SystemScope},
            switched_ratio={sys: {tsk: BatchedMeasure() for tsk in TaskScope} for sys in SystemScope},
            switched_response={sys: {tsk: BatchedMeasure() for tsk in TaskScope} for sys in SystemScope},
            switched_throughput={sys: {tsk: BatchedMeasure() for tsk in TaskScope} for sys in SystemScope}
        )

        # Batch management
        self.n_batches = 0
        self.t_batch = t_batch

    def register_batch(self):
        """
        Register and close the current batch statistics.
        :return: None
        """
        # Compute counters and derived metrics
        self.compute_metrics()

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
        
        # Compute counters and derived metrics
        self.compute_metrics()
        
        # Sampling
        for metric in stat.metrics.__dict__:
            for sys in SystemScope:
                for tsk in TaskScope:
                    sample = getattr(self.metrics, metric)[sys][tsk].sample()
                    getattr(stat.metrics, metric)[sys][tsk] = sample
                    assert getattr(stat.metrics, metric)[sys][tsk] == sample

        return stat
    
    def compute_metrics(self):
        """
        Compute counters and derived metrics.
        :return: None
        """
        # Compute counters for SystemScope.SYSTEM
        #   * arrived_system = arrived_cloudlet + arrived_cloud
        #   * completed_system = completed_cloudlet + completed_cloud
        #   * service_system = service_cloudlet + service_cloud
        #   * switched_system = switched_cloudlet
        #   * switched_completed_system = switched_completed_cloud
        #   * switched_service_system = switched_service_cloud
        for tsk in TaskScope.concrete():
            self.metrics.arrived[SystemScope.SYSTEM][tsk].set_value(
                sum(self.metrics.arrived[sys][tsk].get_value() for sys in SystemScope.subsystems()))

            self.metrics.completed[SystemScope.SYSTEM][tsk].set_value(
                sum(self.metrics.completed[sys][tsk].get_value() for sys in SystemScope.subsystems()))

            self.metrics.service[SystemScope.SYSTEM][tsk].set_value(
                sum(self.metrics.service[sys][tsk].get_value() for sys in SystemScope.subsystems()))

            self.metrics.switched[SystemScope.SYSTEM][tsk].set_value(
                self.metrics.switched[SystemScope.CLOUD][tsk].get_value())

            self.metrics.switched_completed[SystemScope.SYSTEM][tsk].set_value(
                self.metrics.switched_completed[SystemScope.CLOUD][tsk].get_value())

            self.metrics.switched_service[SystemScope.SYSTEM][tsk].set_value(
                sum(self.metrics.switched_service[sys][tsk].get_value() for sys in SystemScope.subsystems()))

        # Compute counters for TaskScope.GLOBAL:
        #   * arrived_global = arrived_task_1 + arrived_task_2
        #   * completed_global = completed_task_1 + completed_task_2
        #   * service_global = service_task_1 + service_task_2
        #   * switched_global = switched_task_1 + switched_task_2
        #   * switched_completed_global = switched_completed_task_1 + switched_completed_task_2
        #   * switched_service_global = switched_service_task_1 + switched_service_task_2
        for sys in SystemScope:
            self.metrics.arrived[sys][TaskScope.GLOBAL].set_value(
                sum(self.metrics.arrived[sys][tsk].get_value() for tsk in TaskScope.concrete()))

            self.metrics.completed[sys][TaskScope.GLOBAL].set_value(
                sum(self.metrics.completed[sys][tsk].get_value() for tsk in TaskScope.concrete()))

            self.metrics.service[sys][TaskScope.GLOBAL].set_value(
                sum(self.metrics.service[sys][tsk].get_value() for tsk in TaskScope.concrete()))

            self.metrics.switched[sys][TaskScope.GLOBAL].set_value(
                sum(self.metrics.switched[sys][tsk].get_value() for tsk in TaskScope.concrete()))

            self.metrics.switched_completed[sys][TaskScope.GLOBAL].set_value(
                sum(self.metrics.switched_completed[sys][tsk].get_value() for tsk in TaskScope.concrete()))

            self.metrics.switched_service[sys][TaskScope.GLOBAL].set_value(
                sum(self.metrics.switched_service[sys][tsk].get_value() for tsk in TaskScope.concrete()))

        # Compute derived metrics:
        #   * response = service / completed
        #   * throughput = completed / t_batch
        #   * switched_ratio = switched / arrived
        #   * switched_response = switched_service / switched_completed
        #   * switched_throughput = switched_completed / t_batch
        for sys in SystemScope:
            for tsk in TaskScope:
                # TODO FARE CON WELFORD
                self.metrics.response[sys][tsk].set_value(
                    (self.metrics.service[sys][tsk].get_value() /
                    self.metrics.completed[sys][tsk].get_value())
                    if self.metrics.completed[sys][tsk].get_value() > 0 else 0)

                # TODO FARE CON completati / t_current
                self.metrics.throughput[sys][tsk].set_value(
                    self.metrics.completed[sys][tsk].get_value() / self.t_batch)

                # TODO INTERROTTI SU TUTTI GLI ARRIVATI
                self.metrics.switched_ratio[sys][tsk].set_value(
                    (self.metrics.switched[sys][tsk].get_value() /
                    self.metrics.arrived[sys][tsk].get_value())
                    if self.metrics.arrived[sys][tsk].get_value() > 0 else 0)

                # TODO fare con WELFORD
                self.metrics.switched_response[sys][tsk].set_value(
                    (self.metrics.switched_service[sys][tsk].get_value() /
                    self.metrics.switched_completed[sys][tsk].get_value())
                    if self.metrics.switched_completed[sys][tsk].get_value() > 0 else 0)

                self.metrics.switched_throughput[sys][tsk].set_value(
                    self.metrics.switched_completed[sys][tsk].get_value() / self.t_batch)

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
    s = InstantaneousStatistics(0)

    s.metrics.arrived[SystemScope.CLOUDLET][TaskScope.TASK_1] = 1
    s.metrics.arrived[SystemScope.CLOUDLET][TaskScope.TASK_2] = 2
    s.metrics.arrived[SystemScope.CLOUD][TaskScope.TASK_1] = 3
    s.metrics.arrived[SystemScope.CLOUD][TaskScope.TASK_2] = 4

    for tsk in TaskScope.concrete():
        s.metrics.arrived[SystemScope.SYSTEM][tsk] = sum(s.metrics.arrived[sys][tsk] for sys in SystemScope.subsystems())

    for tsk in TaskScope.concrete():
        print(s.metrics.arrived[SystemScope.SYSTEM][tsk])