from core.simulations.cloud.model.cloudlet import SimpleCloudlet as Cloudlet
from core.simulations.cloud.model.cloud import SimpleCloud as Cloud
from core.simulations.cloud.model.server_selector import SelectionRule
from core.statistics.sample_statistics import SimpleSampleStatistics as SampleStatistic
import logging

# Configure logger
logger = logging.getLogger(__name__)


class SimpleCloudletCloudSystem:
    """
    A simple system, made of a Cloudlet and a Cloud.
    """

    def __init__(self, rndgen, config_cloudlet, config_cloud):
        """
        Create a new system.
        :param rndgen: (object) the multi-stream random number generator.
        :param config_cloudlet: (dictionary) the configuration for the Cloudlet.
        :param config_cloud: (dictionary) the configuration for the Cloud.
        """
        self.cloudlet = Cloudlet(
            rndgen,
            config_cloudlet["n_servers"],
            config_cloudlet["service_rate_1"],
            config_cloudlet["service_rate_2"],
            config_cloudlet["threshold"],
            SelectionRule[config_cloudlet["server_selection"]]
        )

        self.cloud = Cloud(
            rndgen,
            config_cloud["service_rate_1"],
            config_cloud["service_rate_2"],
            config_cloud["t_setup_mean"]
        )

        # state
        self.n_1 = 0  # total number of serving tasks of type 1
        self.n_2 = 0  # total number of serving tasks of type 2

        # statistics
        self.n_arrival_1 = 0  # total number of arrived tasks of type 1
        self.n_arrival_2 = 0  # total number of arrived tasks of type 2
        self.n_served_1 = 0  # total number of served tasks of type 1
        self.n_served_2 = 0  # total number of served tasks of type 2
        self.response_time = SampleStatistic()  # the response time

        # meta
        self.area_service = 0.0  # the service area, used to compute utilization
        self.t_last_completion = 0.0  # the last completion time, used to compute throughput and utilization

    # ==================================================================================================================
    # EVENT SUBMISSION
    #   * ARRIVAL_TASK_1
    #   * ARRIVAL_TASK_2
    #   * COMPLETION_CLOUDLET_TASK_1
    #   * COMPLETION_CLOUDLET_TASK_2
    #   * COMPLETION_CLOUD_TASK_1
    #   * COMPLETION_CLOUD_TASK_2
    # ==================================================================================================================

    def submit_arrival_task_1(self, t_arrival):
        """
        Submit to the system the arrival of a task of type 1.
        :param t_arrival: (float) the arrival time.
        :return: (e1,e2,e3) (SimpleEvent,SimpleEvent,SimpleEvent) events, where
        *e1* is the completion event of the submitted task of type 1;
        *e2* is the completion time of the interrupted task of type 2 in the Cloudlet, if present; if it is not
        present, *c3* is None.
        *e3* is the completion event of the restarted task of type 2, if present; if it is not present, *c2* is None;
        """
        # Update state
        self.n_1 += 1

        # Update statistics
        self.n_arrival_1 += 1

        # Process event
        if self.cloudlet.n_1 == self.cloudlet.n_servers:
            logger.debug("TASK_1 sent to CLOUD at time {}".format(t_arrival))
            completion_event = self.cloud.submit_arrival_task_1(t_arrival)

            return completion_event, None, None

        elif self.cloudlet.n_1 + self.cloudlet.n_2 < self.cloudlet.threshold:
            logger.debug("TASK_1 sent to CLOUDLET at time {}".format(t_arrival))
            completion_event = self.cloudlet.submit_arrival_task_1(t_arrival)

            return completion_event, None, None

        elif self.cloudlet.n_2 > 0:
            logger.debug("TASK_2 interrupted in CLOUDLET at time {}".format(t_arrival))
            completion_event_to_ignore, t_wasted = self.cloudlet.submit_interruption_task_2(t_arrival)

            logger.debug("TASK_2 restarted in CLOUD at time {}".format(t_arrival))
            completion_restart_event = self.cloud.submit_restart_task_2(t_arrival)
            completion_restart_event.t_wait += t_wasted

            logger.debug("TASK_1 sent to CLOUDLET at time {}".format(t_arrival))
            completion_event = self.cloudlet.submit_arrival_task_1(t_arrival)

            return completion_event, completion_event_to_ignore, completion_restart_event

        else:
            logger.debug("TASK_1 sent to CLOUDLET at time {}".format(t_arrival))
            completion_event = self.cloudlet.submit_arrival_task_1(t_arrival)

            return completion_event, None, None

    def submit_arrival_task_2(self, event_time):
        """
        Submit to the system the arrival of a task of type 2.
        :param event_time: (float) the occurrence time of the event.
        :return: (SimpleEvent) completion event of the submitted task of type 2.
        """
        # Update state
        self.n_2 += 1

        # Update statistics
        self.n_arrival_2 += 1

        # Process event
        if self.cloudlet.n_1 + self.cloudlet.n_2 >= self.cloudlet.threshold:
            logger.debug("TASK_2 sent to CLOUD at time {}".format(event_time))
            completion_event = self.cloud.submit_arrival_task_2(event_time)

            return completion_event
        else:
            logger.debug("TASK_2 sent to CLOUDLET at time {}".format(event_time))
            completion_event = self.cloudlet.submit_arrival_task_2(event_time)

            return completion_event

    def submit_completion_cloudlet_task_1(self, t_completion, t_service, t_wait=0):
        """
        Submit to the system the completion of a task of type 1 in Cloudlet.
        :param t_completion: (float) the completion time.
        :param t_service: (float) the service time.
        :param t_wait: (float) the waiting time.
        :return: None
        """
        logger.debug("TASK_1 completed in CLOUDLET t_completion={}, t_service={}, t_wait={}".format(t_completion, t_service, t_wait))

        # Check correctness
        assert self.n_1 > 0

        # Update state
        self.n_1 -= 1

        # Update statistics
        self.n_served_1 += 1
        self.response_time.add_value(t_service + t_wait)

        # Update meta
        self.area_service += t_service
        self.t_last_completion = t_completion

        # Process event
        self.cloudlet.submit_completion_task_1(t_completion)

    def submit_completion_cloudlet_task_2(self, t_completion, t_service, t_wait=0):
        """
        Submit to the system the completion of a task of type 2 in Cloudlet.
        :param t_completion: (float) the occurrence time of the event.
        :param t_service: (float) the service time.
        :param t_wait: (float) the waiting time.
        :return: None
        """
        logger.debug("TASK_2 completed in CLOUDLET t_completion={}, t_service={}, t_wait={}".format(t_completion, t_service, t_wait))

        # Check correctness
        assert self.n_2 > 0

        # Update state
        self.n_2 -= 1

        # Update statistics
        self.n_served_2 += 1
        self.response_time.add_value(t_service + t_wait)

        # Update meta
        self.area_service += t_service
        self.t_last_completion = t_completion

        # Process event
        self.cloudlet.submit_completion_task_2(t_completion)

    def submit_completion_cloud_task_1(self, t_completion, t_service, t_wait=0):
        """
        Submit to the system the completion of a task of type 1 in Cloud.
        :param t_completion: (float) the occurrence time of the event.
        :param t_service: (float) the service time.
        :param t_wait: (float) the waiting time.
        :return: None
        """
        logger.debug("TASK_1 completed in CLOUD t_completion={}, t_service={}, t_wait={}".format(t_completion, t_service, t_wait))

        # Check correctness
        assert self.n_1 > 0

        # Update state
        self.n_1 -= 1

        # Update statistics
        self.n_served_1 += 1
        self.response_time.add_value(t_service + t_wait)

        # Update meta
        self.area_service += t_service
        self.t_last_completion = t_completion

        # Process event
        self.cloud.submit_completion_task_1(t_completion, t_service)

    def submit_completion_cloud_task_2(self, t_completion, t_service, t_wait=0):
        """
        Submit to the system the completion of a task of type 2 in Cloud.
        :param t_completion: (float) the occurrence time of the event.
        :param t_service: (float) the service time.
        :param t_wait: (float) the waiting time.
        :return: None
        """
        logger.debug("TASK_2 completed in CLOUD t_completion={}, t_service={}, t_wait={}".format(t_completion, t_service, t_wait))

        # Check correctness
        assert self.n_2 > 0

        # Update state
        self.n_2 -= 1

        # Update statistics
        self.n_served_2 += 1
        self.response_time.add_value(t_service + t_wait)

        # Update meta
        self.area_service += t_service
        self.t_last_completion = t_completion

        # Process event
        self.cloud.submit_completion_task_2(t_completion, t_service)

    # ==================================================================================================================
    # METRICS
    # ==================================================================================================================

    def get_response_time(self):
        """
        Compute the overall system response time.
        :return: (float) the overall system response time.
        """
        return self.response_time.get_mean()

    def get_throughput(self):
        """
        Compute the overall system throughput.
        :return: (float) the overall system throughput.
        """
        return (self.n_served_1 + self.n_served_2) / self.t_last_completion

    def get_utilization(self):
        """
        Compute the overall system utilization.
        :return: (float) the overall system utilization.
        """
        return self.area_service / self.t_last_completion

    def get_wasted_time(self):
        """
        Compute the overall system wasted time.
        :return: (float) the overall system wasted time.
        """
        return self.cloudlet.t_wasted_2 + self.cloud.t_restart_2

    # ==================================================================================================================
    # OTHER
    # ==================================================================================================================

    def empty(self):
        """
        Check weather the system is empty or not.
        :return: True, if the system is empty; False, otherwise.
        """
        return self.n_1 + self.n_2 == 0

    def __str__(self):
        """
        String representation.
        :return: the string representation.
        """
        sb = ["{attr}={value}".format(attr=attr, value=self.__dict__[attr]) for attr in self.__dict__ if
              not attr.startswith("__") and not callable(getattr(self, attr))]
        return "System({}:{})".format(id(self), ", ".join(sb))