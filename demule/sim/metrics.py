class NodeMetricTracker(object):
    """
    A dynamic metrics tracker for a single node.
    """
    def __init__(self, start=0.0):
        """
        Creates a new *NodeMetricTracker*.
        :param start: (float) optional, initialization time for the clock.
        """
        self._clock = start
        self.node = 0.0
        self.queue = 0.0
        self.service = 0.0

    def update(self, time, n):
        """
        Updates the metrics by tracking the quantities in time.
        :param time: (float) the time of the current update.
        :param n: (int) the number of jobs.
        """
        if n > 0:
            interval = (time - self._clock)
            self.node += interval * n
            self.queue += interval * (n - 1)
            self.service += interval
        self._clock = time

    def get_utilization(self):
        """
        Retrieves the utilization.
        :return: (float) the utilization.
        """
        return self.service / self._clock