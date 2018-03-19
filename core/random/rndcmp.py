"""
A random component generator.
"""


class RandomComponent:

    def __init__(self, gen, str, var, par):
        """
        Create a new RandomComponent.
        :param gen: the random generator.
        :param str: (dict) streams configuration.
        :param var: (dict) variates configuration.
        :param par: (dict) variates parameters.
        """
        self.gen = gen
        self.str = str
        self.var = var
        self.par = par

    def generate(self, key):
        """
        Generate a random number for the specified key.
        :param key: a key.
        :return: a random number for the specified key.
        """
        self.gen.stream(self.str[key])
        return self.var[key].generator.generate(u=self.gen, **self.par[key])

    def __str__(self):
        """
        String representation.
        :return: the string representation.
        """
        sb = ["{attr}={value}".format(attr=attr, value=self.__dict__[attr]) for attr in self.__dict__ if
              not attr.startswith("__") and not callable(getattr(self, attr))]
        return "RandomComponent({}:{})".format(id(self), ", ".join(sb))