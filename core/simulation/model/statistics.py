from core.statistics.batch_means import BatchedSampleStatistic
from core.statistics.batch_means import BatchedSamplePathStatistic
from core.statistics.batch_means import BatchedMeasure


class SimulationStatistics:
    """
    The set of statistics for the simulation.
    """

    def __init__(self):
        """
        Create a new set of statistics.
        """
        self.n_completed = BatchedMeasure()
        self.t_service = BatchedMeasure()
        self.t_response = BatchedSampleStatistic()
        self.throughput = BatchedSamplePathStatistic()

    def close_batch(self):
        """
        Close the current batch statistics.
        :return: None
        """
        self.n_completed.close_batch()
        self.t_response.close_batch()
        self.throughput.close_batch()