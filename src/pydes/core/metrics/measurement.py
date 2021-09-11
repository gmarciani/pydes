class Measure:
    """
    The base class for measurement.
    A measure is a value with a measurement unit.
    """

    def __init__(self, unit=None):
        """
        Create a new measure.
        :param unit (String) the measurement unit (Default: None).
        """
        self._value = 0.0
        self._unit = unit

    def get_value(self):
        """
        Get the current value.
        :return: the current value.
        """
        return self._value

    def set_value(self, value):
        """
        Set the current value.
        :param value: the value.
        :return: None
        """
        self._value = value

    def get_unit(self):
        """
        Get the measurement unit.
        :return: the measurement unit.
        """
        return self._unit

    def __str__(self):
        """
        String representation.
        :return: the string representation.
        """
        sb = [
            "{attr}={value}".format(attr=attr, value=self.__dict__[attr])
            for attr in self.__dict__
            if not attr.startswith("__") and not callable(getattr(self, attr))
        ]
        return "SampleMeasure({}:{})".format(id(self), ", ".join(sb))

    def __repr__(self):
        """
        String representation.
        :return: the string representation.
        """
        return self.__str__()
