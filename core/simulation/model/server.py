from enum import Enum, unique
from core.simulation.model.event import EventType
from core.simulation.model.scope import TaskScope
from core.random.rndvar import exponential
import logging

# Configure logger
logger = logging.getLogger(__name__)


@unique
class ServerState(Enum):
    """
    Enumerate server states.
    """
    IDLE = 0
    BUSY = 1


class SimpleServer:
    """
    A simple Server.
    """

    def __init__(self, rndgen, service_rate_1, service_rate_2):
        """
        Create a new Server.
        :param rndgen: (object) the multi-stream random number generator.
        :param service_rate_1: (float) the service rate for job of type 1 (tasks/s).
        :param service_rate_2: (float) the service rate for job of type 2 (tasks/s).
        """
        # Service rates
        self.rates = {
            TaskScope.TASK_1: service_rate_1,
            TaskScope.TASK_2: service_rate_2
        }

        # Randomization
        self.rndgen = rndgen
        self.streams = {
            TaskScope.TASK_1: EventType.COMPLETION_CLOUDLET_TASK_1.value + id(self),
            TaskScope.TASK_2: EventType.COMPLETION_CLOUDLET_TASK_2.value + id(self)
        }

        # State
        self.state = ServerState.IDLE  # the state of the server (ServerState)
        self.task_type = None  # the type of the task being served (TaskType)
        self.t_arrival = 0.0  # the last arrival time (float) (s)
        self.t_service = 0.0  # the last service time (float) (s)
        self.t_completion = 0.0  # the last completion time (float) (s)
        self.t_interruption = 0.0  # the last interruption time (float) (s)

        # Statistics
        self.arrived = {task: 0 for task in TaskScope}  # total number of arrived tasks, by task type
        self.completed = {task: 0 for task in TaskScope}  # total number of completed tasks, by task type
        self.switched = {task: 0 for task in TaskScope}  # total number of interrupted tasks, by task type
        self.service = {task: 0 for task in TaskScope}  # total service time, by task type

        self.t_idle = 0.0  # the total idle time (float) (s)

    # ==================================================================================================================
    # EVENT SUBMISSION
    #   * ARRIVAL_TASK_1
    #   * ARRIVAL_TASK_2
    #   * COMPLETION_TASK_1
    #   * COMPLETION_TASK_2
    #   * INTERRUPTION_TASK_2
    # ==================================================================================================================

    def submit_arrival(self, task_type, t_clock):
        """
        Submit a task.
        :param task_type: (TaskType) the type of the task.
        :param t_clock: (float) the current time.
        :return: (float) the completion time;
        """
        assert self.state is ServerState.IDLE

        # Update state
        self.state = ServerState.BUSY
        self.task_type = task_type
        self.t_arrival = t_clock
        self.t_service = self.get_service_time(task_type)
        self.t_completion = self.t_arrival + self.t_service

        # Update statistics
        self.arrived[task_type] += 1
        self.t_idle += (t_clock - self.t_completion)

        return self.t_completion

    def submit_interruption(self, task_type, t_clock):
        """
        Interrupt a task.
        :param task_type: (TaskType) the type of the task.
        :param t_clock: (float) the current time.
        :return: (c,a,s,r) where
        *c* is the scheduled completion time of the interrupted task;
        *a* is the arrival time of the interrupted task;
        *s* is the served time of the interrupted task;
        *r* is the remaining service time ratio of the interrupted task.
        """
        assert self.state is ServerState.BUSY and self.task_type is task_type
        assert self.t_completion >= t_clock

        t_served = t_clock - self.t_arrival

        # Update state
        self.state = ServerState.IDLE
        self.task_type = None
        self.t_interruption = t_clock

        # Update statistics
        self.switched[task_type] += 1
        self.service[task_type] += t_served

        ratio_remaining = (self.t_completion - t_served) / (self.t_completion - self.t_arrival)

        return self.t_completion, self.t_arrival, t_served, ratio_remaining

    def submit_completion(self):
        """
        Submit the completion of the running task.
        :return: (float) the service time.
        """
        assert self.state is ServerState.BUSY

        # Update statistics
        self.completed[self.task_type] += 1
        self.service[self.task_type] += (self.t_completion - self.t_arrival)

        # Update state
        self.state = ServerState.IDLE
        self.task_type = None

        return self.t_service

    # ==================================================================================================================
    # RANDOM TIME GENERATION
    # ==================================================================================================================

    def get_service_time(self, task_type):
        """
        Generate a random service time for the specified task type.
        :param task_type: (TaskType) the task type.
        :return: (float) a random service time for the specified task type.
        """
        self.rndgen.stream(self.streams[task_type])
        return exponential(1.0 / self.rates[task_type], self.rndgen.rnd())

    # ==================================================================================================================
    # OTHER
    # ==================================================================================================================

    def __str__(self):
        """
        String representation.
        :return: the string representation.
        """
        sb = ["{attr}={value}".format(attr=attr, value=self.__dict__[attr]) for attr in self.__dict__ if
              not attr.startswith("__") and not attr.startswith("_") and not callable(getattr(self, attr))]
        return "Server({}:{})".format(id(self), ", ".join(sb))

    def __repr__(self):
        """
        String representation.
        :return: the string representation.
        """
        return self.__str__()

    def __eq__(self, other):
        if not isinstance(other, SimpleServer):
            return False
        return id(self) == id(other)