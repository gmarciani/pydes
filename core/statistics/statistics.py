from math import pow,sqrt

class SimpleStatisticsCalculator:
    """
    A simple statistics calculator.
    """

    def __init__(self):
        """
        Create a new *SimpleStatisticsCalculator*.
        """
        self.n = 0  # the number of values

        # statistics
        self.mean = 0.0  # the mean value
        self.variance = 0.0  # the variance

    def add_value(self, value):
        """
        Add value to the statistics calculator.
        :param value: the value to add.
        :return: (void)
        """
        self.n += 1

        # update mean and variance, leveraging the Welford's algorithm
        d = value - self.mean
        self.variance = self.variance + d * d * (self.n - 1) / self.n
        self.mean = self.mean + d / self.n

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
    from core.rnd.rndgen import MarcianiMultiStream as RandomGenerator
    from core.rnd.rndvar import uniform

    rndgen = RandomGenerator(123456789)

    # Creation
    stats_1 = SimpleStatisticsCalculator()
    print("Statistics 1:", stats_1)

    a = 0
    b = 10
    for i in range(100):
        u = rndgen.rnd()
        value = uniform(a, b, u)
        stats_1.add_value(value)
        print("value: {} | mean: {} | variance: {}".format(value, stats_1.mean, stats_1.variance))

    theoretical_mean = (a + b) / 2
    theoretical_variance = (b-a) / sqrt(12)
    print("Mean: {} (theoretical: {})".format(stats_1.mean, theoretical_mean))
    print("Variance: {} (theoretical: {})".format(stats_1.variance, theoretical_variance))

    print("Statistics 1:", stats_1)