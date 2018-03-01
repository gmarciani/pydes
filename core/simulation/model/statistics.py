from core.statistics.batch_means import BatchedSampleStatistic, BatchedMeasure
from core.utils.csv_utils import save


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
        self.arrived = 0
        self.completed = 0
        self.switched = 0
        self.service = 0.0
        self.population = 0.0
        self.response = 0.0
        self.throughput = 0.0

    def save_csv(self, filename, append=False, skip_header=False):
        """
        Save the current statistics as CSV.
        :param filename: (string) the filename.
        :param append: (bool) if True, append to an existing file.
        :param skip_header: (bool) if True, skip the CSV header.
        :return: None
        """
        header = ["time", "arrived", "completed", "switched", "service", "population", "response", "throughput"]
        data = []

        sample = [
            self.time,
            self.arrived,
            self.completed,
            self.switched,
            self.service,
            self.population,
            self.response,
            self.throughput
        ]

        data.append(sample)
        save(filename, header, data, append, skip_header)


class SimulationStatistics:
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
        self.population = BatchedSampleStatistic()
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
        if self.completed.get_value() > 0:
            self.response.set_value(self.service.get_value() / self.completed.get_value())
        else:
            self.response.set_value(0)

        self.throughput.set_value(self.completed.get_value() / self.t_batch)

        # Register all metrics
        self.arrived.register_batch()
        self.completed.register_batch()
        self.switched.register_batch()
        self.service.register_batch()
        self.population.register_batch()
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

        self.population.discard_batch()
        self.response.discard_batch()
        self.throughput.discard_batch()

    def sample(self, t_now):
        """
        Get sample statistics.
        :param t_now: (float) the current time.
        :return: the instantaneous statistics.
        """
        s = InstantaneousStatistics(t_now)
        s.arrived = self.arrived.sample()
        s.completed = self.completed.sample()
        s.switched = self.switched.sample()
        s.service = self.service.sample()
        s.population = self.population.sample()
        s.response = s.service / s.completed if s.completed > 0 else 0.0
        s.throughput = s.completed / t_now if t_now > 0 else 0.0

        return s

    def save_csv(self, filename, append=False, skip_header=False, batch=None):
        """
        Save the current statistics as CSV.
        :param filename: (string) the filename.
        :param append: (bool) if True, append to an existing file.
        :param skip_header: (bool) if True, skip the CSV header.
        :param batch: (integer) the batch id. If None, all batches are saved.
        :return: None
        """
        header = ["batch", "arrived", "completed", "switched", "service", "population", "response", "throughput"]
        data = []
        rng_batches = range(self.n_batches) if batch is None else range(batch, batch+1)
        for b in rng_batches:
            sample = [
                b,
                self.arrived.get_value(b),
                self.completed.get_value(b),
                self.switched.get_value(b),
                self.service.get_value(b),
                self.population.get_value(b),
                self.response.get_value(b),
                self.throughput.get_value(b)
            ]
            data.append(sample)
        save(filename, header, data, append, skip_header)