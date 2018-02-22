from core.simulation.model.system import SimpleCloudletCloudSystem as System
from core.utils.report import SimpleReport as Report
from core.random import rndgen
from core.simulation.model.taskgen import SimpleTaskgen as Taskgen
from core.simulation.model.calendar import NextEventCalendar as Calendar
from core.simulation.model.event import EventType
from core.utils.guiutils import print_progress
import logging

# Configure logger
logger = logging.getLogger(__name__)


class Simulation:
    """
    A simple simulation about Cloud computing.
    """

    def __init__(self, config, name="SIMULATION"):
        """
        Create a new simulation.
        :param config: the configuration for the simulation.
        :param name: the name of the simulation.
        """
        self.config = config
        self.name = name

        # Configuration - General
        config_general = config["general"]
        self.n_batch = config_general["n_batch"]
        self.t_batch = config_general["t_batch"]
        self.t_stop = self.n_batch * self.t_batch
        self.rndgen = getattr(rndgen, config_general["random"]["generator"])(config_general["random"]["seed"])

        # Configuration - Tasks
        config_tasks = config["tasks"]
        self.taskgen = Taskgen(
            self.rndgen,
            config_tasks["arrival_rate_1"],
            config_tasks["arrival_rate_2"],
            self.t_stop
        )

        # Configuration - System (Cloudlet and Cloud)
        config_system = self.config["system"]
        self.system = System(
            self.rndgen,
            config_system["cloudlet"],
            config_system["cloud"]
        )

        # Configuration - Calendar
        # Notice that the calendar internally manages:
        # (i) event sorting, by occurrence time.
        # (ii) scheduling of only possible events, that are:
        #   (ii.i) possible arrivals, i.e. arrivals with occurrence time lower than stop time.
        #   (ii.ii) departures of possible arrivals.
        # (iii) unscheduling of events to ignore, e.g. completion in Cloudlet of interrupted tasks of type 2.
        self.calendar = Calendar(0.0, self.t_stop, [EventType.ARRIVAL_TASK_1, EventType.ARRIVAL_TASK_2])


        # The closed door status: if True, no more arrivals will be accepted.
        self.closed_door = False

    # ==================================================================================================================
    # SIMULATION PROCESS
    # ==================================================================================================================

    def run(self):
        """
        Run the simulation.
        :return: None
        """

        # Simulation Start.
        logger.info("Simulation started")

        # Initialize first arrivals
        # Schedule the first events, i.e. task of type 1 and 2.
        # Notice that the event order by arrival time is managed internally by the Calendar.
        self.calendar.schedule(self.taskgen.generate_new_arrival_1(self.calendar.get_clock()))
        self.calendar.schedule(self.taskgen.generate_new_arrival_2(self.calendar.get_clock()))

        # Run the simulation while the calendar is not empty.
        # Notice that the calendar contains only possible events, that are:
        # (i) possible arrivals, i.e. arrivals with occurrence time lower than stop time.
        # (ii) departures of possible arrivals.
        while not self.calendar.empty() or not self.system.empty():

            # Get the next event and update the calendar clock.
            # Notice that the Calendar clock is automatically updated.
            # Notice that the next event is always a possible event.
            event = self.calendar.get_next_event()
            logger.debug("Next: %s", event)

            # If the close door condition holds, close the door to arrivals
            if not self.closed_door and self.calendar.get_clock() >= self.t_stop:
                logger.debug("Closing door to arrivals")
                self.closed_door = True

            # Process according to event types.
            if event.type is EventType.ARRIVAL_TASK_1:
                # Submit to the System the arrival of a task of type 1.
                completion_event, interrupted_completion_event, completion_restart_event = self.system.submit_arrival_task_1(event.time)

                # Schedule completion events.
                self.calendar.schedule(completion_event)
                if completion_restart_event is not None:
                    self.calendar.unschedule(interrupted_completion_event)
                    self.calendar.schedule(completion_restart_event)

                # If the closed_door condition is False, schedule a new random arrival of a task of type 1.
                # Notice that this s only an optimization, as the calendar internally schedules only possible events.
                if not self.closed_door:
                    arrival_event = self.taskgen.generate_new_arrival_1(self.calendar.get_clock())
                    self.calendar.schedule(arrival_event)

            elif event.type is EventType.ARRIVAL_TASK_2:
                # Submit to the System the arrival of a task of type 2.
                completion_event = self.system.submit_arrival_task_2(event.time)

                # Schedule completion event.
                self.calendar.schedule(completion_event)

                # If the closed_door condition is False, schedule a new random arrival of a task of type 2.
                # Notice that this s only an optimization, as the calendar internally schedules only possible events.
                if not self.closed_door:
                    arrival_event = self.taskgen.generate_new_arrival_2(self.calendar.get_clock())
                    self.calendar.schedule(arrival_event)

            elif event.type is EventType.COMPLETION_CLOUDLET_TASK_1:
                # Submit to the System the completion of task of type 1 from within the Cloudlet.
                self.system.submit_completion_cloudlet_task_1(event.time, event.t_service)

            elif event.type is EventType.COMPLETION_CLOUDLET_TASK_2:
                # Submit to the System the completion of task of type 2 from within the Cloudlet.
                self.system.submit_completion_cloudlet_task_2(event.time, event.t_service)

            elif event.type is EventType.COMPLETION_CLOUD_TASK_1:
                # Submit to the System the completion of task of type 1 from within the Cloud.
                self.system.submit_completion_cloud_task_1(event.time, event.t_service)

            elif event.type is EventType.COMPLETION_CLOUD_TASK_2:
                # Submit to the System the completion of task of type 2 from within the Cloud.
                self.system.submit_completion_cloud_task_2(event.time, event.t_service)

            else:
                raise ValueError("Unrecognized event: {}".format(event))

            # Simulation progess
            print_progress(self.calendar.get_clock(), self.t_stop)

        # Simulation End.
        logger.info("Simulation stopped")

    # ==================================================================================================================
    # REPORT
    # ==================================================================================================================

    def generate_report(self, float_prec=3):
        """
        Generate a full report about the given simulation.
        :param float_prec: (int) the number of decimals for float values.
        :return: (SimpleReport) the report.
        """
        report = Report(self.name)

        # Report - General
        report.add("general", "simulation_class", self.__class__.__name__)
        report.add("general", "t_stop", self.t_stop)
        report.add("general", "random_generator", self.rndgen.__class__.__name__)
        report.add("general", "random_seed", self.rndgen.get_initial_seed())

        # Report - Tasks
        report.add_all("tasks", self.taskgen)

        # Report - System
        report.add("system", "n_1", self.system.n_1)
        report.add("system", "n_2", self.system.n_2)
        report.add("system", "n_arrival_1", self.system.n_arrival_1)
        report.add("system", "n_arrival_2", self.system.n_arrival_2)
        report.add("system", "n_served_1", self.system.n_served_1)
        report.add("system", "n_served_2", self.system.n_served_2)
        report.add("system", "response_time", round(self.system.get_response_time(), float_prec))
        report.add("system", "throughput", round(self.system.get_throughput(), float_prec))
        report.add("system", "utilization", round(self.system.get_utilization(), float_prec))
        report.add("system", "wasted_time", round(self.system.get_wasted_time(), float_prec))

        # Report - System/Cloudlet
        report.add_all("system/cloudlet", self.system.cloudlet)

        # Report - System/Cloud
        report.add_all("system/cloud", self.system.cloud)

        return report

    # ==================================================================================================================
    # OTHER
    # ==================================================================================================================

    def __str__(self):
        """
        String representation.
        :return: the string representation.
        """
        sb = ["{attr}={value}".format(attr=attr, value=self.__dict__[attr]) for attr in self.__dict__ if
              not attr.startswith('__') and not callable(getattr(self, attr))]
        return "Simulation({}:{})".format(id(self), ', '.join(sb))


if __name__ == "__main__":
    from core.simulation.config.configuration import get_default_configuration

    config = get_default_configuration()
    simulation = Simulation(config)

    simulation.run()

    report = simulation.generate_report()

    print(report)