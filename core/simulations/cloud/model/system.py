from core.simulations.cloud.model.cloudlet import SimpleCloudLet as Cloudlet
from core.simulations.cloud.model.cloud import SimpleCloud as Cloud
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
            config_cloudlet["threshold"]
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

    def submit_arrival_task_1(self, event_time):
        """
        Submit to the system the arrival of a task of type 1.
        :param event_time: (float) the occurrence time of the event.
        :return: (c1,c2,c3) (SimpleEvent,SimpleEvent)completion events, where
        *c1* is the completion event of the submitted task of type 1;
        *c2* is the completion event of the restarted task of type 2, if present; if it is not present, *c2* is None;
        *c3* is the completion time of the interrupted task of type 2 in the Cloudlet, if present; if it is not
        present, *c3* is None.
        """
        # state change
        self.n_1 += 1

        # record statistics
        self.n_arrival_1 += 1

        # processing
        if self.cloudlet.n_1 == self.cloudlet.n_servers:
            logger.debug("ARRIVAL_TASK_1 submitted to CLOUD at time {}".format(event_time))
            completion_event = self.cloud.submit_arrival_task_1(event_time)
            return completion_event, None, None
        elif self.cloudlet.n_1 + self.cloudlet.n_2 < self.cloudlet.threshold:
            logger.debug("ARRIVAL_TASK_1 submitted to CLOUDLET at time {}".format(event_time))
            completion_event = self.cloudlet.submit_arrival_task_1(event_time)
            return completion_event, None, None
        elif self.cloudlet.n_2 > 0:
            logger.debug("REMOVAL_TASK_2 from CLOUDLET at time {}".format(event_time))
            completion_to_ignore = self.cloudlet.submit_removal_task_2(event_time)
            logger.debug("RESTART_TASK_2 submitted to CLOUD at time {}".format(event_time))
            completion_restart_event = self.cloud.submit_restart_task_2(event_time)
            logger.debug("ARRIVAL_TASK_1 submitted to CLOUDLET at time {}".format(event_time))
            completion_event = self.cloudlet.submit_arrival_task_1(event_time)
            return completion_event, completion_restart_event, completion_to_ignore
        else:
            logger.debug("ARRIVAL_TASK_1 submitted to CLOUDLET at time {}".format(event_time))
            completion_event = self.cloudlet.submit_arrival_task_1(event_time)
            return completion_event, None, None

    def submit_arrival_task_2(self, event_time):
        """
        Submit to the system the arrival of a task of type 2.
        :param event_time: (float) the occurrence time of the event.
        :return: (SimpleEvent) completion event of the submitted task of type 2.
        """
        # state change
        self.n_2 += 1

        # record statistics
        self.n_arrival_2 += 1

        # processing
        if self.cloudlet.n_1 + self.cloudlet.n_2 >= self.cloudlet.threshold:
            logger.debug("ARRIVAL_TASK_2 submitted to CLOUD at time {}".format(event_time))
            completion_event = self.cloud.submit_arrival_task_2(event_time)
            return completion_event
        else:
            logger.debug("ARRIVAL_TASK_2 submitted to CLOUDLET at time {}".format(event_time))
            completion_event = self.cloudlet.submit_arrival_task_2(event_time)
            return completion_event

    def submit_completion_cloudlet_task_1(self, event_time):
        """
        Submit to the system the completion of a task of type 1 in Cloudlet.
        :param event_time: (float) the occurrence time of the event.
        :return: (void)
        """
        logger.debug("COMPLETION_TASK_1 submitted to CLOUDLET at time {}".format(event_time))

        # state change
        self.n_1 -= 1

        # record statistics
        self.n_served_1 += 1

        # processing
        self.cloudlet.submit_completion_task_1(event_time)

    def submit_completion_cloudlet_task_2(self, event_time):
        """
        Submit to the system the completion of a task of type 2 in Cloudlet.
        :param event_time: (float) the occurrence time of the event.
        :return: (void)
        """
        logger.debug("COMPLETION_TASK_2 submitted to CLOUDLET at time {}".format(event_time))

        # state change
        self.n_2 -= 1

        # record statistics
        self.n_served_2 += 1

        # processing
        self.cloudlet.submit_completion_task_2(event_time)

    def submit_completion_cloud_task_1(self, event_time):
        """
        Submit to the system the completion of a task of type 1 in Cloud.
        :param event_time: (float) the occurrence time of the event.
        :return: (void)
        """
        logger.debug("COMPLETION_TASK_1 submitted to CLOUD at time {}".format(event_time))

        # state change
        self.n_1 -= 1

        # record statistics
        self.n_served_1 += 1

        # processing
        self.cloud.submit_completion_task_1(event_time)

    def submit_completion_cloud_task_2(self, event_time):
        """
        Submit to the system the completion of a task of type 2 in Cloud.
        :param event_time: (float) the occurrence time of the event.
        :return: (void)
        """
        logger.debug("COMPLETION_TASK_2 submitted to CLOUD at time {}".format(event_time))

        # state change
        self.n_2 -= 1

        # record statistics
        self.n_served_2 += 1

        # processing
        self.cloud.submit_completion_task_2(event_time)

    def __str__(self):
        """
        String representation.
        :return: the string representation.
        """
        sb = ["{attr}='{value}'".format(attr=attr, value=self.__dict__[attr]) for attr in self.__dict__ if not attr.startswith("__") and not callable(getattr(self, attr))]
        return "System({}:{})".format(id(self), ", ".join(sb))

    def __repr__(self):
        """
        String representation.
        :return: the string representation.
        """
        return self.__str__()

    def __eq__(self, other):
        if not isinstance(other, SimpleCloudletCloudSystem):
            return False
        return self.cloudlet == other.cloudlet and \
               self.cloud == other.cloud


if __name__ == "__main__":
    from core.simulations.cloud.config.configuration import default_configuration
    from core.random.rndgen import MarcianiMultiStream as RandomGenerator

    rndgen = RandomGenerator(123456789)

    config_cloudlet = default_configuration["system"]["cloudlet"]
    config_cloud = default_configuration["system"]["cloud"]
    system_1 = SimpleCloudletCloudSystem(rndgen, config_cloudlet, config_cloud)
    print("System 1:", system_1)
    system_2 = SimpleCloudletCloudSystem(rndgen, config_cloudlet, config_cloud)
    print("System 2:", system_2)

    print("System 1 equals System 2:", system_1 == system_2)