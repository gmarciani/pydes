from enum import Enum, unique


@unique
class SystemScope(Enum):
    """
    The scope of events:
        * SYSTEM
        * CLOUDLET
        * CLOUD
    """

    SYSTEM = 0
    CLOUDLET = 1
    CLOUD = 2

    @staticmethod
    def subsystems():
        """
        Return the subsystem scopes only.
        :return: the subsystems scopes only.
        """
        return list(x for x in SystemScope if x is not SystemScope.SYSTEM)

    def __str__(self):
        """
        Return the string representation.
        :return: the string representation.
        """
        return self.name

    def __repr__(self):
        """
        Return the string representation.
        :return: the string representation.
        """
        return self.__str__()


@unique
class TaskScope(Enum):
    """
    The scope ot tasks:
        * GLOBAL (special scope used in statistics and task generation)
        * TASK_1
        * TASK_2
    """

    GLOBAL = 0
    TASK_1 = 1
    TASK_2 = 2

    @staticmethod
    def concrete():
        """
        Return the concrete task scopes only.
        :return: the concrete task scopes only.
        """
        return list(x for x in TaskScope if x is not TaskScope.GLOBAL)

    def __str__(self):
        """
        Return the string representation.
        :return: the string representation.
        """
        return self.name

    def __repr__(self):
        """
        Return the string representation.
        :return: the string representation.
        """
        return self.__str__()


@unique
class ActionScope(Enum):
    """
    The scope of event actions:
        * ARRIVAL
        * COMPLETION
        * INTERRUPTION
        * RESTART
    """

    ARRIVAL = 0
    COMPLETION = 1
    INTERRUPTION = 2
    RESTART = 3

    def __str__(self):
        """
        Return the string representation.
        :return: the string representation.
        """
        return self.name

    def __repr__(self):
        """
        Return the string representation.
        :return: the string representation.
        """
        return self.__str__()
