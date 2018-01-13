from core.simulations.cloud.model.system import SimpleCloudletCloudSystem as System
from core.random import rndgen
from core.simulations.cloud.model.taskgen import SimpleTaskgen as Taskgen
from core.simulations.common.calendar import NextEventCalendar as Calendar
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
        self.t_stop = config_general["t_stop"]
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
        # Notice that the calendar internally manages:
        # (i) event sorting, by occurrence time.
        # (ii) scheduling of only possible events, that are:
        #   (ii.i) possible arrivals, i.e. arrivals with occurrence time lower than stop time.
        #   (ii.ii) departures of possible arrivals.
        # (iii) unscheduling of events to ignore, e.g. completion in Cloudlet of interrupted tasks of type 2.
        self.calendar = Calendar(0.0, self.t_stop, [EventType.ARRIVAL_TASK_1, EventType.ARRIVAL_TASK_2])

        self._closed_door = False

    def run(self):
        """
        Run the simulation.
        :return: (void)
        """

        # Simulation Start.
        logger.info("Simulation started")

        # Initialize first arrivals
        self._init_arrivals()

        # Run the simulation while the calendar is not empty.
        # Notice that the calendar contains only possible events, that are:
        # (i) possible arrivals, i.e. arrivals with occurrence time lower than stop time.
        # (ii) departures of possible arrivals.
        while not self.calendar.empty() or not self.system.empty():

            logger.debug("### SYSTEM REPORT ### {}".format(self.system))

            # Get the next event and update the calendar clock.
            # Notice that the Calendar clock is automatically updated.
            # Notice that the next event is always a possible event.
            event = self.calendar.get_next_event()
            logger.debug("Next: %s", event)

            # If the close door condition holds, close the door to arrivals
            if not self._closed_door and self._close_door_condition():
                logger.debug("Closing door to arrivals")
                self._closed_door = True

            # Process according to event types.
            if event.type is EventType.ARRIVAL_TASK_1:
                # Submit to the System the arrival of a task of type 1.
                completion, completion_restart, completion_to_ignore = self.system.submit_arrival_task_1(event.time)

                # Schedule completion events.
                self.calendar.schedule(completion)
                if completion_restart is not None:
                    self.calendar.unschedule(completion_to_ignore)
                    self.calendar.schedule(completion_restart)

                # If the closed_door condition is False, schedule a new random arrival of a task of type 1.
                # Notice that this s only an optimization, as the calendar internally schedules only possible events.
                if not self._closed_door:
                    self.calendar.schedule(self.taskgen.generate_new_arrival_1(self.calendar.get_clock()))

            elif event.type is EventType.ARRIVAL_TASK_2:
                # Submit to the System the arrival of a task of type 2.
                completion = self.system.submit_arrival_task_2(event.time)

                # Schedule completion event.
                self.calendar.schedule(completion)

                # If the closed_door condition is False, schedule a new random arrival of a task of type 2.
                # Notice that this s only an optimization, as the calendar internally schedules only possible events.
                if not self._closed_door:
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

            # Simulation progess
            print_progress(self.calendar.get_clock(), self.t_stop)

        # Simulation End.
        logger.info("Simulation stopped")

    def _init_arrivals(self):
        """
        Initialize event queue with first arrivals.
        :return: (void)
        """
        # Schedule the first events, i.e. task of type 1 and 2.
        # Notice that the event order by arrival time is managed internally by the Calendar.
        event_arrival_task_1 = Event(EventType.ARRIVAL_TASK_1,
                                     self.calendar.get_clock() + self.taskgen.get_inter_arrival_task_1())
        event_arrival_task_2 = Event(EventType.ARRIVAL_TASK_2,
                                     self.calendar.get_clock() + self.taskgen.get_inter_arrival_task_2())
        self.calendar.schedule(event_arrival_task_1)
        self.calendar.schedule(event_arrival_task_2)

    def _close_door_condition(self):
        """
        Check if the stop condition is satisfied for the simulation.
        :return: True, if the simulation should stop; False, otherwise.
        """
        return self.calendar.get_clock() >= self.t_stop

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
    from core.simulations.cloud.config.configuration import get_default_configuration

    config = get_default_configuration()
    simulation_1 = SimpleCloudSimulation(config)

    print("Simulation 1", simulation_1)