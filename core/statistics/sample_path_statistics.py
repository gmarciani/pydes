from math import sqrt


class SimpleSamplePathStatistics:
    """
    A simple sample-path statistics calculator.
    It calculates:
        * sample-path mean
        * sample-path variance
        * sample-path standard deviation.
    """

    def __init__(self):
        """
        Create a new *SimpleStatisticsCalculator*.
        """
        self._n = 0  # the number of values
        self._time = 0.0  # the current time

        # statistics
        self._mean = 0.0  # the mean value
        self._variance = 0.0  # the variance

    def reset(self):
        """
        Reset statistics.
        :return: (void)
        """
        self._n = 0
        self._time = 0.0

        self._mean = 0.0
        self._variance = 0.0

    def add_value(self, value, t_now):
        """
        Add value to the statistics calculator.
        :param value: the value to add.
        :param t_now: the occurrence time.
        :return: (void)
        """
        self._n += 1
        t_prev = self._time
        self._time = t_now

        # update mean and variance, leveraging the Welford's algorithm
        delta_value = value - self._mean
        delta_time = t_now - t_prev
        self._variance += pow(delta_value, 2) * delta_time * t_prev / t_now
        self._mean += delta_value * delta_time / t_now

    def get_dimension(self):
        """
        Return the sample dimension.
        :return: (int) the sample dimension.
        """
        return self._n

    def get_time(self):
        """
        Return the sample last time.
        :return: (int) the sample last time.
        """
        return self._time

    def get_mean(self):
        """
        Return the sample-path mean.
        :return: (float) the sample-path mean.
        """
        return self._mean

    def get_variance(self):
        """
        Return the sample-path variance.
        :return: (float) the sample-path variance.
        """
        return self._variance / self._time

    def get_stddev(self):
        """
        Return the sample-path standard deviation.
        :return: (float) the sample-path standard deviation.
        """
        return sqrt(self._variance / self._time)

    def __str__(self):
        """
        String representation.
        :return: the string representation.
        """
        sb = ["{attr}='{value}'".format(attr=attr, value=self.__dict__[attr]) for attr in self.__dict__ if not attr.startswith("__") and not callable(getattr(self, attr))]
        return "Statistics({}:{})".format(id(self), ", ".join(sb))

    def __repr__(self):
        """
        String representation.
        :return: the string representation.
        """
        return self.__str__()


if __name__ == "__main__":
    from core.random.rndgen import MarcianiMultiStream as RandomGenerator
    from core.random.rndvar import uniform, equilikely, exponential, geometric

    rndgen = RandomGenerator(123456789)

    n = 10000

    # Creation
    stats = SimpleSamplePathStatistics()
    print("Statistics 1:", stats)

    # Uniform
    print("Uniform")
    a = 0
    b = 10
    for i in range(1, n):
        stats.add_value(uniform(a, b, rndgen.rnd()), i)

    theoretical_mean = (a + b) / 2
    theoretical_stddev = (b-a) / sqrt(12)
    print("Mean: {} (theoretical: {})".format(stats.get_mean(), theoretical_mean))
    print("StdDev: {} (theoretical: {})".format(stats.get_stddev(), theoretical_stddev))

    stats.reset()

    # Equilikely
    print("Equilikely")
    a = 0
    b = 10
    for i in range(1, n):
        stats.add_value(equilikely(a, b, rndgen.rnd()), i)

    theoretical_mean = (a + b) / 2
    theoretical_stddev = sqrt((pow(b - a + 1, 2) - 1) / 12)
    print("Mean: {} (theoretical: {})".format(stats.get_mean(), theoretical_mean))
    print("StdDev: {} (theoretical: {})".format(stats.get_stddev(), theoretical_stddev))

    stats.reset()

    # Exponential
    print("Exponential")
    m = 1 / 0.35
    for i in range(1, n):
        stats.add_value(exponential(m, rndgen.rnd()), i)

    theoretical_mean = m
    theoretical_stddev = m
    print("Mean: {} (theoretical: {})".format(stats.get_mean(), theoretical_mean))
    print("StdDev: {} (theoretical: {})".format(stats.get_stddev(), theoretical_stddev))

    stats.reset()

    # Geometric
    print("Geometric")
    p = 0.75
    for i in range(1, n):
        stats.add_value(geometric(p, rndgen.rnd()), i)

    theoretical_mean = p / (1 - p)
    theoretical_stddev = sqrt(p) / (1 - p)
    print("Mean: {} (theoretical: {})".format(stats.get_mean(), theoretical_mean))
    print("StdDev: {} (theoretical: {})".format(stats.get_stddev(), theoretical_stddev))