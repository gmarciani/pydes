from core.statistics.batch_means import BatchedSampleStatistic
from core.statistics.batch_means import BatchedSamplePathStatistic
from core.utils.csv_utils import save

class BatchStatistics:
    """
    The set of statistics for the simulation.
    """

    def __init__(self):
        """
        Create a new set of statistics.
        """
        self.t_response = BatchedSampleStatistic()
        self.throughput = BatchedSamplePathStatistic()
        self.n_batches = 0

    def register_batch(self):
        """
        Register and close the current batch statistics.
        :return: None
        """
        self.t_response.register_batch()
        self.throughput.register_batch()
        self.n_batches += 1

    def discard_batch(self):
        """
        Discard the current batch statistics.
        :return: None
        """
        self.t_response.discard_batch()
        self.throughput.discard_batch()

    def save_csv(self, filename, skip_header=False, append=False):
        """
        Save the current statistics as CSV.
        :param filename: (string) the filename.
        :param skip_header: (bool) if True, skip the CSV header.
        :param append: (bool) if True, append to an existing file.
        :return: None
        """
        header = ["batch", "t_response", "throughput"]
        data = []
        for b in range(self.n_batches):
            sample = [b, self.t_response.get_batch_value(b), self.throughput.get_batch_value(b)]
            data.append(sample)
        save(filename, header, data, skip_header, append)