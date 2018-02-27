from core.statistics.batch_means import BatchedSampleStatistic, BatchedMeasure
from core.statistics.batch_means import BatchedSamplePathStatistic
from core.utils.csv_utils import save


class BatchStatistics:
    """
    The set of statistics for the simulation.
    """

    def __init__(self, t_batch=None):
        """
        Create a new set of statistics.
        """

        # Measures
        self.arrived = BatchedMeasure()
        self.completed = BatchedMeasure()
        self.switched = BatchedMeasure()
        self.service = BatchedMeasure()
        self.n = BatchedSampleStatistic()
        self.response = BatchedMeasure()
        self.throughput = BatchedMeasure()

        # Batch management
        self.n_batches = 0
        self.t_batch = t_batch

    def register_batch(self):
        """
        Register and close the current batch statistics.
        :return: None
        """
        # Compute derived metrics
        self.response.set_value(self.service.get_value() / self.completed.get_value())
        self.throughput.set_value(self.completed.get_value() / self.t_batch)

        # Register all metrics
        self.arrived.register_batch()
        self.completed.register_batch()
        self.switched.register_batch()
        self.service.register_batch()
        self.n.register_batch()
        self.response.register_batch()
        self.throughput.register_batch()

        self.n_batches += 1

    def discard_batch(self):
        """
        Discard the current batch statistics.
        :return: None
        """
        self.arrived.discard_batch()
        self.completed.discard_batch()
        self.switched.discard_batch()
        self.service.discard_batch()

        self.n.discard_batch()
        self.response.discard_batch()
        self.throughput.discard_batch()

    def save_csv(self, filename, append=False, skip_header=False, batch=None):
        """
        Save the current statistics as CSV.
        :param filename: (string) the filename.
        :param append: (bool) if True, append to an existing file.
        :param skip_header: (bool) if True, skip the CSV header.
        :param batch: (integer) the batch id. If None, all batches are saved.
        :return: None
        """
        header = ["batch", "arrived", "completed", "switched", "service", "n", "response", "throughput"]
        data = []
        rng_batches = range(self.n_batches) if batch is None else range(batch, batch+1)
        for b in rng_batches:
            sample = [
                b,
                self.arrived.get_value(b),
                self.completed.get_value(b),
                self.switched.get_value(b),
                self.service.get_value(b),
                self.n.get_value(b),
                self.response.get_value(b),
                self.throughput.get_value(b)
            ]
            data.append(sample)
        save(filename, header, data, append, skip_header)