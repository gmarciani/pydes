from core.simulations.cloud.model.server import SimpleServer as Server
from core.simulations.cloud.model.task import TaskType as TaskType
import logging

# Configure logger
logger = logging.getLogger(__name__)

class SimpleCloudLet:
    """
    A simple Cloudlet, defined by its state.
    """

    def __init__(self, n_servers, service_rate_1, service_rate_2, threshold):
        """
        Create a new Cloudlet.
        :param n_servers: (integer) the number of servers.
        :param service_rate_1: (float) the service rate for job of type 1 (tasks/s).
        :param service_rate_2: (float) the service rate for job of type 2 (tasks/s).
        :param threshold: (int) the occupancy threshold.
        """
        self.n_servers = n_servers
        self.service_rate_1 = service_rate_1
        self.service_rate_2 = service_rate_2
        self.threshold = threshold

        self.__servers = [Server()] * self.n_servers

        self.n_tasks_1 = 0  # number of tasks of type 1
        self.n_tasks_2 = 0  # number of tasks of type 2

    def submit_task(self, task):
        """
        Submit a task to the Cloudlet
        :param task: (Task) the task to submit.
        :return: True, if the task has been accepted; False, otherwise.
        """
        if task.type == TaskType.TASK_1:
            if self.n_tasks_1 == self.n_servers:
                return False
            elif self.n_tasks_1 + self.n_tasks_2 < self.threshold:
                # self.__process_task(task)
                return True
            elif self.n_tasks_2 > 0:
                # self.__swap_task_2()
                # self.__process_task(task)
                return True
            else:
                # self.__process_task(task)
                return True
        elif task.type == TaskType.TASK_2:
            if self.n_tasks_1 + self.n_tasks_2 >= self.threshold:
                # self.__send_to_cloud(task)
                return False
            else:
                # self.__process_task(task)
                return True
        else:
            logger.warning("Unknown task type submitted to Cloudlet %d: %d", id(self), task.type)

    def __str__(self):
        """
        String representation.
        :return: the string representation.
        """
        sb = ["{attr}='{value}'".format(attr=attr, value=self.__dict__[attr]) for attr in self.__dict__ if not attr.startswith("__") and not callable(getattr(self, attr))]
        return "Cloudlet({}:{})".format(id(self), ", ".join(sb))

    def __repr__(self):
        """
        String representation.
        :return: the string representation.
        """
        return self.__str__()

    def __eq__(self, other):
        if not isinstance(other, SimpleCloudLet):
            return False
        return id(self) == id(other)


if __name__ == "__main__":
    cloudlet_1 = SimpleCloudLet(10, 0.45, 0.30, 10)
    print("Cloudlet 1:", cloudlet_1)
    cloudlet_2 = SimpleCloudLet(20, 0.90, 0.60, 20)
    print("Cloudlet 2:", cloudlet_2)

    print("Cloudlet 1 equals Cloudlet 2:", cloudlet_1 == cloudlet_2)