from core.simulation.model.event import EventType
from core.simulation.model.event import SimpleEvent as Event
from core.random.rndvar import exponential
import logging

# Configure logger
from core.simulation.model.task import Task

logger = logging.getLogger(__name__)


class SimpleCloud:
    """
    A simple Cloud server, defined by its state.
    """

    def __init__(self, rndgen, service_rate_1, service_rate_2, setup_mean):
        """
        Create a new Cloud server.
        :param rndgen: (object) the multi-stream random number generator.
        :param service_rate_1: (float) the service rate for job of type 1 (tasks/s).
        :param service_rate_2: (float) the service rate for job of type 2 (tasks/s).
        :param setup_mean: (float) the mean setup time to restart a task of type 2 in the Cloud (s).
        """
        # Service rates
        self.rates = {
            Task.TASK_1: service_rate_1,
            Task.TASK_2: service_rate_2
        }

        # Setup
        self.setup_mean = setup_mean

        # Randomization
        self.rndgen = rndgen
        self.streams = {
            Task.TASK_1: EventType.COMPLETION_CLOUD_TASK_1.value,
            Task.TASK_2: EventType.COMPLETION_CLOUD_TASK_2.value,
            EventType.SWITCH_TASK_2: EventType.SWITCH_TASK_2.value
        }

        # State
        self.n = {task: 0 for task in Task}  # current number of tasks, by task type

        # Whole-run Statistics (used in verification)
        self.arrived = {task: 0 for task in Task}  # total number of arrived tasks, by task type
        self.completed = {task: 0 for task in Task}  # total number of completed tasks, by task type
        self.switched = {task: 0 for task in Task}  # total number of restarted tasks, by task type
        self.service = {task: 0 for task in Task}  # total service time, by task type

    # ==================================================================================================================
    # EVENT SUBMISSION
    #   * ARRIVAL_TASK_1
    #   * ARRIVAL_TASK_2
    #   * RESTART_CLOUD_TASK_2
    #   * COMPLETION_CLOUD_TASK_1
    #   * COMPLETION_CLOUD_TASK_2
    # ==================================================================================================================

    def submit_arrival(self, task_type, t_arrival):
        """
        Submit to the Cloud the arrival of a task.
        :param task_type: (TaskType) the type of the task.
        :param t_arrival: (float) the arrival time.
        :return: (float) the completion time.
        """
        # Update state
        self.n[task_type] += 1

        # Generate completion
        t_service = self.get_service_time(task_type)
        t_completion = t_arrival + t_service

        # Update statistics
        self.arrived[task_type] += 1

        return t_completion

    def submit_restart(self, task_type, t_arrival, ratio_remaining):
        """
        Submit to the Cloud the restart of a task.
        :param task_type: (TaskType) the type of the task.
        :param t_arrival: (float) the arrival time.
        :param ratio_remaining: (float) the remaining ratio.
        :return: (float) the completion time.
        """
        # Update state
        self.n[task_type] += 1

        # Generate completion
        t_setup = self.get_setup_time()
        t_service = ratio_remaining * self.get_service_time(task_type) + t_setup
        t_completion = t_arrival + t_service

        # Update statistics
        self.switched[task_type] += 1

        return t_completion

    def submit_completion(self, task_type, t_completion, t_arrival):
        """
        Submit to the Cloud the completion of a task.
        :param task_type: (TaskType) the type of the task.
        :param t_completion: (float) the completion time.
        :param t_arrival: (float) the arrival time.
        :return: None
        """
        # Check correctness
        assert self.n[task_type] > 0

        # Update state
        self.n[task_type] -= 1

        # Update statistics
        self.completed[task_type] += 1
        self.service[task_type] += t_completion - t_arrival

    # ==================================================================================================================
    # RANDOM TIME GENERATION
    #   * service time
    #   * setup time
    # ==================================================================================================================

    def get_service_time(self, task_type):
        """
        Generate the service time for a task.
        :param task_type: (TaskType) the type of the task.
        :return: (float) the service time for a task of type 1 (s).
        """
        self.rndgen.stream(self.streams[task_type])
        return exponential(1.0 / self.rates[task_type], self.rndgen.rnd())

    def get_setup_time(self):
        """
        Generate the setup time for a restarted task.
        :return: (float) the setup time for a restarted task.
        """
        self.rndgen.stream(self.streams[EventType.SWITCH_TASK_2])
        return exponential(self.setup_mean, self.rndgen.rnd())

    # ==================================================================================================================
    # OTHER
    # ==================================================================================================================

    def __str__(self):
        """
        String representation.
        :return: the string representation.
        """
        sb = ["{attr}={value}".format(attr=attr, value=self.__dict__[attr]) for attr in self.__dict__ if
              not attr.startswith("__") and not callable(getattr(self, attr))]
        return "Cloud({}:{})".format(id(self), ", ".join(sb))