from copy import deepcopy
from enum import Enum, unique

from pydes.core.simulation.model.scope import TaskScope
from pydes.core.utils.logutils import get_logger

# Logging
logger = get_logger(__name__)


@unique
class ServerState(Enum):
    """
    Enumerate server states.
    """

    IDLE = 0
    BUSY = 1


class SimpleServer:
    """
    A Server resource.
    """

    def __init__(self, rndservice, idx):
        """
        Create a new Server.
        :param rndservice: (RandomComponent) rnd component for the service process.
        :param idx: (int) the server index.
        """
        # Server Index (used in randomization)
        self.idx = idx

        # Randomization
        self.rndservice = deepcopy(rndservice)
        for tsk in self.rndservice.str:
            self.rndservice.str[tsk] += self.idx  # decoupling of each server randomness

        # State and important variables
        self.state = ServerState.IDLE  # the state of the server (ServerState)
        self.task_type = None  # the type of the task being served (TaskType)
        self.t_arrival = 0.0  # the last arrival time (float) (s)
        self.t_service = 0.0  # the last service time (float) (s)
        self.t_completion = 0.0  # the last completion time (float) (s)
        self.t_interruption = 0.0  # the last interruption time (float) (s)

        # Statistics (used by server selection rules)
        self.arrived = {tsk: 0 for tsk in TaskScope.concrete()}  # total number of arrived tasks, by task type
        self.completed = {tsk: 0 for tsk in TaskScope.concrete()}  # total number of completed tasks, by task type
        self.switched = {tsk: 0 for tsk in TaskScope.concrete()}  # total number of interrupted tasks, by task type
        self.service = {tsk: 0 for tsk in TaskScope.concrete()}  # total service time, by task type
        self.t_idle = 0.0  # the total idle time (float) (s)

    # ==================================================================================================================
    # EVENT SUBMISSION
    #   * ARRIVAL_TASK_1
    #   * ARRIVAL_TASK_2
    #   * COMPLETION_TASK_1
    #   * COMPLETION_TASK_2
    #   * INTERRUPTION_TASK_2
    # ==================================================================================================================

    def submit_arrival(self, tsk, t_now):
        """
        Submit a task.
        :param tsk: (TaskType) the type of the task.
        :param t_now: (float) the current time.
        :return: (float) the completion time;
        """
        assert self.state is ServerState.IDLE

        # Update state
        self.state = ServerState.BUSY
        self.task_type = tsk
        self.t_arrival = t_now
        self.t_service = self.rndservice.generate(tsk)
        self.t_completion = self.t_arrival + self.t_service

        # Update statistics
        self.arrived[tsk] += 1
        self.t_idle += t_now - self.t_completion

        return self.t_completion

    def submit_interruption(self, tsk, t_now):
        """
        Interrupt a task.
        :param tsk: (TaskType) the type of the task.
        :param t_now: (float) the current time.
        :return: (c,a,s,r) where
        *c* is the scheduled completion time of the interrupted task;
        *a* is the arrival time of the interrupted task;
        """
        assert self.state is ServerState.BUSY and self.task_type is tsk
        assert self.t_completion >= t_now

        t_served = t_now - self.t_arrival

        # Update state
        self.state = ServerState.IDLE
        self.task_type = None
        self.t_interruption = t_now

        # Update statistics
        self.switched[tsk] += 1
        self.service[tsk] += t_served

        return self.t_completion, self.t_arrival

    def submit_completion(self):
        """
        Submit the completion of the running task.
        :return: (float) the service time.
        """
        assert self.state is ServerState.BUSY

        # Update statistics
        self.completed[self.task_type] += 1
        self.service[self.task_type] += self.t_completion - self.t_arrival

        # Update state
        self.state = ServerState.IDLE
        self.task_type = None

        return self.t_service

    # ==================================================================================================================
    # OTHER
    # ==================================================================================================================

    def __str__(self):
        """
        String representation.
        :return: the string representation.
        """
        sb = [
            "{attr}={value}".format(attr=attr, value=self.__dict__[attr])
            for attr in self.__dict__
            if not attr.startswith("__") and not attr.startswith("_") and not callable(getattr(self, attr))
        ]
        return "Server({}:{})".format(id(self), ", ".join(sb))

    def __eq__(self, other):
        if not isinstance(other, SimpleServer):
            return False
        return id(self) == id(other)
