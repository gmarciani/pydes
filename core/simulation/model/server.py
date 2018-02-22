from enum import Enum, unique
from core.simulation.model.event import EventType
from core.simulation.model.task import TaskType
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
        self._rndgen = rndgen
        self.service_rate_1 = service_rate_1
        self.service_rate_2 = service_rate_2

        # state
        self.state = ServerState.IDLE  # the state of the server (ServerState)
        self.task_type = None  # the type of the task being served (TaskType)
        self.t_arrival = 0.0  # the last arrival time (float) (s)
        self.t_service = 0.0  # the last service time (float) (s)
        self.t_completion = 0.0  # the last completion time (float) (s)
        self.t_interruption = 0.0  # the last interruption time (float) (s)

        # statistics
        self.n_served_1 = 0  # the total amount of served tasks of type 1
        self.n_served_2 = 0  # the total amount of served tasks of type 2
        self.n_interrupted_2 = 0  # the total amount of interrupted tasks of type 2
        self.idle_time = 0.0  # the total idle time (float) (s)
        self.busy_time = 0.0  # the total busy time (float) (s)
        self.wasted_time = 0.0  # the total wasted time (float) (s)

        # meta
        self.stream_service_task_1 = EventType.COMPLETION_CLOUDLET_TASK_1.value + int(id(self))
        self.stream_service_task_2 = EventType.COMPLETION_CLOUDLET_TASK_2.value + int(id(self))

    # ==================================================================================================================
    # EVENT SUBMISSION
    #   * ARRIVAL_TASK_1
    #   * ARRIVAL_TASK_2
    #   * COMPLETION_TASK_1
    #   * COMPLETION_TASK_2
    #   * INTERRUPTION_TASK_2
    # ==================================================================================================================

    def submit_task_1(self, t_clock):
        """
        Submit a task of type 1.
        :param t_clock: (float) the current time (s).
        :return: (c,s) where *c* is the completion time and *s* is the service time.
        """
        assert self.state is ServerState.IDLE

        # Update state
        self.state = ServerState.BUSY
        self.task_type = TaskType.TASK_1
        self.t_arrival = t_clock
        self.t_service = self.get_service_task_1()
        self.t_completion = self.t_arrival + self.t_service

        # Update statistics
        self.idle_time += (t_clock - self.t_completion)

        return self.t_completion, self.t_service

    def submit_task_2(self, t_clock):
        """
        Submit a task of type 2.
        :param t_clock: (float) the current time (s).
        :return: (c,s) where *c* is the completion time and *s* is the service time.
        """
        assert self.state is ServerState.IDLE

        # Update state
        self.state = ServerState.BUSY
        self.task_type = TaskType.TASK_2
        self.t_arrival = t_clock
        self.t_service = self.get_service_task_2()
        self.t_completion = self.t_arrival + self.t_service

        # Update statistics
        self.idle_time += (t_clock - self.t_completion)

        return self.t_completion, self.t_service

    def interrupt_task_2(self, t_clock):
        """
        Interrupt the running task of type 2.
        :param t_clock: (float) the current time (s).
        :return: (c,a,w) where *c* is the completion time of the interrupted task;
        *a* is the arrival time of the interrupted task;
        *w* is the wasted time for the itnerrupted task.
        """
        assert self.state is ServerState.BUSY and self.task_type is TaskType.TASK_2
        assert self.t_completion >= t_clock

        t_busy = t_clock - self.t_arrival

        # Update state
        self.state = ServerState.IDLE
        self.task_type = None
        self.t_interruption = t_clock

        # Update statistics
        self.n_interrupted_2 += 1
        self.busy_time += t_busy
        self.wasted_time += t_busy

        return self.t_completion, self.t_arrival, t_busy

    def submit_completion(self):
        """
        Submit the completion of the running task.
        :return: (float) the service time.
        """
        assert self.state is ServerState.BUSY

        # Update statistics
        if self.task_type is TaskType.TASK_1:
            self.n_served_1 += 1
        elif self.task_type is TaskType.TASK_2:
            self.n_served_2 += 1
        else:
            raise ValueError("Unknown task type: {}".format(self.task_type))
        self.busy_time += (self.t_completion - self.t_arrival)

        # Update state
        self.state = ServerState.IDLE
        self.task_type = None

        return self.t_service

    # ==================================================================================================================
    # RANDOM TIME GENERATION
    #   * service time task 1
    #   * service time task 2
    # ==================================================================================================================

    def get_service_task_1(self):
        """
        Generate a random service time for a task of type 1, exponentially distributed with rate *service_rate_1*.
        :return: (float) a random service time for a task of type 1 (s).
        """
        self._rndgen.stream(self.stream_service_task_1)
        return exponential(1.0 / self.service_rate_1, self._rndgen.rnd())

    def get_service_task_2(self):
        """
        Generate a random service time for a task of type 2, exponentially distributed with rate *service_rate_2*.
        :return: (float) a random service time for a task of type 2 (s).
        """
        self._rndgen.stream(self.stream_service_task_2)
        return exponential(1.0 / self.service_rate_2, self._rndgen.rnd())

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


if __name__ == "__main__":
    from core.random.rndgen import MarcianiMultiStream as RandomGenerator

    rndgen = RandomGenerator(123456789)

    # Creation
    server = SimpleServer(rndgen, 0.45, 0.30)

    # Server loop
    clock = 0.0
    for i in range(5):

        clock += rndgen.rnd()
        server.submit_task_1(clock)
        print("Server state (after submission task type 1 at time {}): {}".format(clock, server))

        clock = server.t_completion
        server.submit_completion()
        print("Server state (after completion task type 1 at time {}): {}".format(clock, server))

        clock += rndgen.rnd()
        server.submit_task_2(clock)
        print("Server state (after submission task type 2 at time {}): {}".format(clock, server))

        clock = server.t_completion
        server.submit_completion()
        print("Server state (after completion task type 2 at time {}): {}".format(clock, server))

        clock += rndgen.rnd()
        server.submit_task_2(clock)
        print("Server state (after submission task type 2 at time {}): {}".format(clock, server))

        clock = (server.t_completion + clock) / 2
        server.interrupt_task_2(clock)
        print("Server state (after interruption task type 2 at time {}): {}".format(clock, server))

        clock += rndgen.rnd()
        server.submit_task_1(clock)
        print("Server state (after submission task type 1 at time {}): {}".format(clock, server))

        clock = server.t_completion
        server.submit_completion()
        print("Server state (after completion task type 1 at time {}): {}".format(clock, server))