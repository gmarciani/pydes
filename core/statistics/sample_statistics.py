from math import sqrt


class SimpleSampleStatistics:
    """
    A simple sample statistics calculator.
    It calculates:
        * sample mean
        * sample variance
        * sample standard deviation.
    """

    def __init__(self):
        """
        Create a new *SimpleStatisticsCalculator*.
        """
        self._n = 0  # the number of values

        # statistics
        self._mean = 0.0  # the mean value
        self._variance = 0.0  # the variance

    def reset(self):
        """
        Reset statistics.
        :return: (void)
        """
        self._n = 0
        self._mean = 0.0
        self._variance = 0.0

    def add_value(self, value):
        """
        Add value to the statistics calculator.
        :param value: the value to add.
        :return: (void)
        """
        self._n += 1

        # update mean and variance, leveraging the Welford's algorithm
        delta_value = value - self._mean
        self._variance += pow(delta_value, 2) * (self._n - 1) / self._n
        self._mean += delta_value / self._n

    def get_dimension(self):
        """
        Return the sample dimension.
        :return: (int) the sample dimension.
        """
        return self._n

    def get_mean(self):
        """
        Return the sample mean.
        :return: (float) the sample mean.
        """
        return self._mean

    def get_variance(self):
        """
        Return the sample variance.
        :return: (float) the sample variance.
        """
        return self._variance / self._n

    def get_stddev(self):
        """
        Return the sample standard deviation.
        :return: (float) the sample standard deviation.
        """
        return sqrt(self._variance / self._n)

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
    stats = SimpleSampleStatistics()
    print("Statistics 1:", stats)

    # Uniform
    print("Uniform")
    a = 0
    b = 10
    for i in range(n):
        stats.add_value(uniform(a, b, rndgen.rnd()))

    theoretical_mean = (a + b) / 2
    theoretical_stddev = (b-a) / sqrt(12)
    print("Mean: {} (theoretical: {})".format(stats.get_mean(), theoretical_mean))
    print("StdDev: {} (theoretical: {})".format(stats.get_stddev(), theoretical_stddev))

    stats.reset()

    # Equilikely
    print("Equilikely")
    a = 0
    b = 10
    for i in range(n):
        stats.add_value(equilikely(a, b, rndgen.rnd()))

    theoretical_mean = (a + b) / 2
    theoretical_stddev = sqrt((pow(b - a + 1, 2) - 1) / 12)
    print("Mean: {} (theoretical: {})".format(stats.get_mean(), theoretical_mean))
    print("StdDev: {} (theoretical: {})".format(stats.get_stddev(), theoretical_stddev))

    stats.reset()

    # Exponential
    print("Exponential")
    m = 1 / 0.35
    for i in range(n):
        stats.add_value(exponential(m, rndgen.rnd()))

    theoretical_mean = m
    theoretical_stddev = m
    print("Mean: {} (theoretical: {})".format(stats.get_mean(), theoretical_mean))
    print("StdDev: {} (theoretical: {})".format(stats.get_stddev(), theoretical_stddev))

    stats.reset()

    # Geometric
    print("Geometric")
    p = 0.75
    for i in range(n):
        stats.add_value(geometric(p, rndgen.rnd()))

    theoretical_mean = p / (1 - p)
    theoretical_stddev = sqrt(p) / (1 - p)
    print("Mean: {} (theoretical: {})".format(stats.get_mean(), theoretical_mean))
    print("StdDev: {} (theoretical: {})".format(stats.get_stddev(), theoretical_stddev))