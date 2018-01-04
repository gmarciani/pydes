from core.simulations.cloud.model.system import SimpleCloudletCloudSystem as System
from core.rnd import rndgen
from core.rnd import rndvar
from core.simulations.cloud.model.taskgen import SimpleTaskgen as Taskgen
from core.simulations.utils.calendar import NextEventCalendar as Calendar
from core.utils.report import SimpleReport as Report
from core.simulations.cloud.model.event import SimpleEvent as Event
from core.simulations.cloud.model.event import EventType
from core.utils.guiutils import print_progress
import logging

# Configure logger
logger = logging.getLogger(__name__)


class SimpleCloudSimulation:
    """
    A simple simulation about Cloud computing.
    """

    def __init__(self, config):
        """
        Create a new simulation.
        :param config: the configuration for the simulation
        """
        self.config = config

        # Configuration - General
        config_general = config["general"]
        self.t_stop = config_general["t_stop"]
        self.replica = config_general["replica"]
        self.rndgen = getattr(rndgen, config_general["random"]["generator"])(config_general["random"]["seed"])

        # Configuration - Tasks
        config_tasks = config["tasks"]
        self.taskgen = Taskgen(
            self.rndgen,
            config_tasks["arrival_rate_1"],
            config_tasks["arrival_rate_2"]
        )

        # Configuration - System (Cloudlet and Cloud)
        config_system = self.config["system"]
        self.system = System(
            self.rndgen,
            config_system["cloudlet"],
            config_system["cloud"]
        )

        # Configuration - Calendar
        self.calendar = Calendar()

    def run(self):
        """
        Run the simulation.
        :return: (SimpleReport) the simulation report.
        """

        # Simulation Start.
        logger.info("Simulation started")

        # Schedule the first events, i.e. task of type 1 and 2.
        # Notice that the event order by arrival time is managed internally by the Calendar.
        event_arrival_task_1 = Event(EventType.ARRIVAL_TASK_1,
                                     self.calendar.get_clock() + self.taskgen.get_inter_arrival_task_1())
        event_arrival_task_2 = Event(EventType.ARRIVAL_TASK_2,
                                     self.calendar.get_clock() + self.taskgen.get_inter_arrival_task_2())
        self.calendar.schedule(event_arrival_task_1, event_arrival_task_2)

        # Run the simulation while:
        # (i) the calendar is not empty, and
        # (ii) the stop condition is not satisfied.
        # Notice that the stop condition is processed within the loop.
        while not self.calendar.is_empty():

            logger.debug("### SYSTEM REPORT ### {}".format(self.system))

            # Get the next event and update the calendar clock.
            # Notice that the Calendar clock is automatically updated.
            event = self.calendar.get_next_event()
            logger.debug("Next: %s", event)

            # If the stop condition holds, stop the simulation.
            if self.stop_condition():
                logger.debug("Stopping simulation")
                break

            if event.type is EventType.ARRIVAL_TASK_1:
                # Submit to the System the arrival of a task of type 1.
                completion, completion_restart, completion_to_ignore = self.system.submit_arrival_task_1(event.time)

                # Schedule completion events.
                self.calendar.schedule(completion)
                if completion_restart is not None:
                    self.calendar.unschedule(completion_to_ignore)
                    self.calendar.schedule(completion_restart)

                # Schedule a new random arrival of a task of type 1.
                self.calendar.schedule(self.taskgen.generate_new_arrival_1(self.calendar.get_clock()))

            elif event.type is EventType.ARRIVAL_TASK_2:
                # Submit to the System the arrival of a task of type 2.
                completion = self.system.submit_arrival_task_2(event.time)

                # Schedule completion event.
                self.calendar.schedule(completion)

                # Schedule a new random arrival of a task of type 2.
                self.calendar.schedule(self.taskgen.generate_new_arrival_2(self.calendar.get_clock()))

            elif event.type is EventType.COMPLETION_CLOUDLET_TASK_1:
                # Submit to the System the completion of task of type 1 from within the Cloudlet.
                self.system.submit_completion_cloudlet_task_1(event.time)

            elif event.type is EventType.COMPLETION_CLOUDLET_TASK_2:
                # Submit to the System the completion of task of type 2 from within the Cloudlet.
                self.system.submit_completion_cloudlet_task_2(event.time)

            elif event.type is EventType.COMPLETION_CLOUD_TASK_1:
                # Submit to the System the completion of task of type 1 from within the Cloud.
                self.system.submit_completion_cloud_task_1(event.time)

            elif event.type is EventType.COMPLETION_CLOUD_TASK_2:
                # Submit to the System the completion of task of type 2 from within the Cloud.
                self.system.submit_completion_cloud_task_2(event.time)

            else:
                raise ValueError("Unrecognized event: {}".format(event))
                pass

            # Simulation progess
            print_progress(self.calendar.get_clock(), self.t_stop)

        # Simulation End.
        logger.info("Simulation stopped")

        # Reporting.
        report = self.generate_report()
        logger.info("Report generated")

        return report

    def stop_condition(self):
        """
        Check if the stop condition is satsfied for the simulation.
        :return: True, if the simulation should stop; False, otherwise.
        """
        return self.calendar.get_clock() >= self.t_stop

    def generate_report(self):
        report = Report('SIMULATION')

        # Report - General
        report.add("general", "simulation_class", self.__class__.__name__)
        report.add("general", "t_stop", self.t_stop)
        report.add("general", "replica", self.replica)
        report.add("general", "random_generator", self.rndgen.__class__.__name__)
        report.add("general", "random_seed", self.rndgen.get_initial_seed())

        # Report - Tasks
        for attr in self.taskgen.__dict__:
            if not attr.startswith("__") and not attr.startswith("_") and not callable(getattr(self.taskgen, attr)):
                report.add("tasks", attr, self.taskgen.__dict__[attr])

        # Report - System
        report.add("system", "n_tasks_1", self.system.n_tasks_1)
        report.add("system", "n_tasks_2", self.system.n_tasks_2)
        report.add("system", "n_served_1", self.system.n_served_1)
        report.add("system", "n_served_2", self.system.n_served_2)

        # Report - System/Cloudlet
        for attr in self.system.cloudlet.__dict__:
            if not attr.startswith("__") and not attr.startswith("_") and not callable(getattr(self.system.cloudlet, attr)):
                report.add("system/cloudlet", attr, self.system.cloudlet.__dict__[attr])

        # Report - System/Cloud
        for attr in self.system.cloud.__dict__:
            if not attr.startswith("__") and not attr.startswith("_") and not callable(getattr(self.system.cloud, attr)):
                report.add("system/cloud", attr, self.system.cloud.__dict__[attr])

        return report

    def __str__(self):
        """
        String representation.
        :return: the string representation.
        """
        sb = ["{attr}='{value}'".format(attr=attr, value=self.__dict__[attr]) for attr in self.__dict__ if not attr.startswith('__') and not callable(getattr(self, attr))]
        return "Simulation({}:{})".format(id(self), ', '.join(sb))

    def __repr__(self):
        """
        String representation.
        :return: the string representation.
        """
        return self.__str__()


if __name__ == "__main__":
    from core.simulations.cloud.config.configuration import default_configuration

    simulation_1 = SimpleCloudSimulation(default_configuration)

    print("Simulation 1", simulation_1)