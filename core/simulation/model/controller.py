from enum import Enum, unique
from core.simulation.model.scope import TaskScope


class SimpleController:
    """
    A simple Cloudlet Controller.
    """

    def __init__(self, controller_algorithm):
        self.controller_algorithm = controller_algorithm

    def process(self, tsk):
        raise NotImplementedError()

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
        return "Controller({}:{})".format(id(self), ", ".join(sb))


class ControllerAlgorithm1(SimpleController):
    """
    A Cloudlet Controller implementing Algorithm 1.
    """

    def __init__(self, cloudlet_state, cloudlet_n_servers):
        super().__init__(ControllerAlgorithm.ALGORITHM_1)
        self.cloudlet_state = cloudlet_state
        self.cloudlet_n_servers = cloudlet_n_servers

    def process(self, tsk):
        n1 = self.cloudlet_state[TaskScope.TASK_1]
        n2 = self.cloudlet_state[TaskScope.TASK_2]
        if n1 + n2 == self.cloudlet_n_servers:
            return ControllerResponse.SUBMIT_TO_CLOUD
        else:
            return ControllerResponse.SUBMIT_TO_CLOUDLET


class ControllerAlgorithm2(SimpleController):
    """
    A Cloudlet Controller implementing Algorithm 2.
    """

    def __init__(self, cloudlet_state, cloudlet_n_servers, cloudlet_threshold):
        super().__init__(ControllerAlgorithm.ALGORITHM_2)
        self.cloudlet_state = cloudlet_state
        self.cloudlet_n_servers = cloudlet_n_servers
        self.cloudlet_threshold = cloudlet_threshold

    def process(self, tsk):
        n1 = self.cloudlet_state[TaskScope.TASK_1]
        n2 = self.cloudlet_state[TaskScope.TASK_2]

        if tsk is TaskScope.TASK_1:

            if n1 == self.cloudlet_n_servers:
                return ControllerResponse.SUBMIT_TO_CLOUD

            elif n1 + n2 < self.cloudlet_threshold:
                return ControllerResponse.SUBMIT_TO_CLOUDLET

            elif n2 > 0:
                return ControllerResponse.SUBMIT_TO_CLOUDLET_WITH_INTERRUPTION

            else:
                return ControllerResponse.SUBMIT_TO_CLOUDLET

        elif tsk is TaskScope.TASK_2:
            if n1 + n2 >= self.cloudlet_threshold:
                return ControllerResponse.SUBMIT_TO_CLOUD

            else:
                return ControllerResponse.SUBMIT_TO_CLOUDLET

        else:
            raise ValueError("Unrecognized task type {}".format(tsk))


@unique
class ControllerAlgorithm(Enum):
    """
    A controller algorithm can be:
        * ALGORITHM_1
        * ALGORITHM_2
    """

    def __new__(cls, *args, **kwds):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    ALGORITHM_1 = 1
    ALGORITHM_2 = 2


@unique
class ControllerResponse(Enum):
    """
    A controller algorithm can return the following responses:
        * SUBMIT_TO_CLOUDLET
        * SUBMIT_TO_CLOUDLET_WITH_INTERRUPTION
        * SUBMIT_TO_CLOUD
    """

    def __new__(cls, *args, **kwds):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    SUBMIT_TO_CLOUDLET = 1
    SUBMIT_TO_CLOUDLET_WITH_INTERRUPTION = 2
    SUBMIT_TO_CLOUD = 2


if __name__ == "__main__":
    algorithm_1 = ControllerAlgorithm["ALGORITHM_1"]
    print(algorithm_1)

    algorithm_2 = ControllerAlgorithm["ALGORITHM_2"]
    print(algorithm_2)

    controller_1 = SimpleController(algorithm_1)
    print(controller_1)

    controller_2 = SimpleController(algorithm_2)
    print(controller_2)
