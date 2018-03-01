from core.simulation.model.system import SimpleCloudletCloudSystem as System
from core.simulation.model.task import Task
from core.simulation.model.report import SimpleReport as Report
from core.random import rndgen
from core.simulation.model.taskgen import SimpleTaskgen as Taskgen
from core.simulation.model.calendar import NextEventCalendar as Calendar
from core.simulation.model.event import EventType, Action
from core.utils.guiutils import print_progress
from core.simulation.model.statistics import SimulationStatistics
from core.utils.logutils import ConsoleHandler
from core.utils.file_utils import empty_file
import os
from core.utils.csv_utils import save
import logging


# Configure logger
logging.basicConfig(level=logging.INFO, handlers=[ConsoleHandler(logging.INFO)])
logger = logging.getLogger(__name__)


class Simulation:
    """
    A simple simulation about Cloud computing.
    """

    def __init__(self, config, name="SIMULATION-CLOUD-CLOUDLET"):
        """
        Create a new simulation.
        :param config: the configuration for the simulation.
        :param name: the name of the simulation.
        """
        self.name = name

        # Configuration - General
        config_general = config["general"]
        self.t_stop = config["general"]["t_stop"]
        self.t_tran = config["general"]["t_tran"]
        self.n_batch = config_general["n_batch"]
        self.t_batch = self.t_stop / self.n_batch
        self.confidence = config_general["confidence"]
        self.rndgen = getattr(rndgen, config_general["random"]["generator"])(config_general["random"]["seed"])
        self.t_sample = config["general"]["t_sample"]

        # The statistics
        self.statistics = SimulationStatistics(self.t_batch)

        # Configuration - Tasks
        config_tasks = config["tasks"]
        self.taskgen = Taskgen(
            self.rndgen,
            config_tasks["arrival_rate_1"],
            config_tasks["arrival_rate_2"],
            self.t_stop
        )

        # Configuration - System (Cloudlet and Cloud)
        config_system = config["system"]
        self.system = System(
            self.rndgen,
            config_system["cloudlet"],
            config_system["cloud"],
            self.statistics
        )

        # Configuration - Calendar
        # Notice that the calendar internally manages:
        # (i) event sorting, by occurrence time.
        # (ii) scheduling of only possible events, that are:
        #   (ii.i) possible arrivals, i.e. arrivals with occurrence time lower than stop time.
        #   (ii.ii) departures of possible arrivals.
        # (iii) unscheduling of events to ignore, e.g. completion in Cloudlet of interrupted tasks of type 2.
        self.calendar = Calendar(0.0, self.t_stop, [EventType.ARRIVAL_TASK_1, EventType.ARRIVAL_TASK_2])

        # The index of the current batch
        self.curr_batch = 0

    # ==================================================================================================================
    # SIMULATION PROCESS
    # ==================================================================================================================

    def run(self, outdir=None, show_progress=False):
        """
        Run the simulation.
        :param outdir (string) the directory for output files (Default: None)
        :param show_progress (bool) if True, print the simulation real time progress bar.
        :return: None
        """

        # Prepare the output files
        if outdir is not None:
            transientfile = os.path.join(outdir, "result.transient.csv")
            batchmeansfile = os.path.join(outdir, "result.batch.csv")
            empty_file(transientfile)
            empty_file(batchmeansfile)
        else:
            transientfile = None
            batchmeansfile = None
        t_last_sample = 0

        # Simulation Start.
        logger.info("Simulation started")

        # Initialize first arrivals
        # Schedule the first events, i.e. task of type 1 and 2.
        # Notice that the event order by arrival time is managed internally by the Calendar.
        self.calendar.schedule(self.taskgen.generate(Task.TASK_1, self.calendar.get_clock()))
        self.calendar.schedule(self.taskgen.generate(Task.TASK_2, self.calendar.get_clock()))

        # Run the simulation while the calendar clock is less than the stop time.
        while self.calendar.get_clock() < self.t_stop:

            # Run the simulation for the current batch
            while self.curr_batch < self.n_batch and self.calendar.get_clock() < self.t_batch * (self.curr_batch+1):

                # Get the next event and update the calendar clock.
                # Notice that the Calendar clock is automatically updated.
                # Notice that the next event is always a possible event.
                event = self.calendar.get_next_event()
                logger.debug("Next: %s", event)

                # Submit the event to the system.
                # Notice that every submission generates some other events to be scheduled/unscheduled,
                # e.g., completions and interruptions (i.e., completions to be ignored).
                events_to_schedule, events_to_unschedule = self.system.submit(event)

                # Schedule/Unschedule response events
                self.calendar.schedule(*events_to_schedule)
                self.calendar.unschedule(*events_to_unschedule)

                # If the event is an arrival, schedule a new arrival of the same type
                # Notice that the next arrival generation is not managed by the system, because it is an event that
                # is related to the simulation paradigm, not to the internal mechanism of the system.
                if event.type.action is Action.ARRIVAL:
                    next_arrival = self.taskgen.generate(event.type.task, self.calendar.get_clock())
                    self.calendar.schedule(next_arrival)

                # If transient data has to be recorded
                if transientfile is not None and \
                    self.calendar.get_clock() > self.t_tran and \
                    self.calendar.get_clock() >= t_last_sample + self.t_sample:
                        self.statistics.sample(self.calendar.get_clock()).save_csv(transientfile, append=True)
                        t_last_sample = self.calendar.get_clock()

                # Simulation progress
                if show_progress:
                    print_progress(self.calendar.get_clock(), self.t_stop)

            # Process the current batch
            # Notice that, if an output file has been specified, it is filled with current batch metrics as CSV.
            if self.calendar.get_clock() > self.t_tran:
                self.statistics.register_batch()
                if batchmeansfile is not None:
                    self.statistics.save_csv(batchmeansfile, append=True, batch=(self.curr_batch))
                self.curr_batch += 1
            else:
                self.statistics.discard_batch()

        # Simulation End.
        logger.info("Simulation completed")

    # ==================================================================================================================
    # REPORT
    # ==================================================================================================================

    def generate_report(self):
        """
        Generate the statistics report.
        :return: (SimpleReport) the statistics report.
        """
        r = Report(self.name)

        alpha = 1.0 - self.confidence

        # Report - General
        r.add("general", "t_stop", self.t_stop)
        r.add("general", "n_batch", self.n_batch)
        r.add("general", "t_batch", self.t_batch)
        r.add("general", "i_batch", self.i_batch)
        r.add("general", "rndgen", self.rndgen.__class__.__name__)
        r.add("general", "rndseed", self.rndgen.get_initial_seed())

        # Report - Tasks
        r.add("tasks", "arrival_rate_1", self.taskgen.rates[Task.TASK_1])
        r.add("tasks", "arrival_rate_2", self.taskgen.rates[Task.TASK_2])
        r.add("tasks", "n_generated_1", self.taskgen.generated[Task.TASK_1])
        r.add("tasks", "n_generated_2", self.taskgen.generated[Task.TASK_2])

        # Report - System/Cloudlet
        r.add("system/cloudlet", "service_rate_1", self.system.cloudlet.rates[Task.TASK_1])
        r.add("system/cloudlet", "service_rate_2", self.system.cloudlet.rates[Task.TASK_2])
        r.add("system/cloudlet", "n_servers", self.system.cloudlet.n_servers)
        r.add("system/cloudlet", "threshold", self.system.cloudlet.threshold)

        # Report - System/Cloud
        r.add("system/cloud", "service_rate_1", self.system.cloud.rates[Task.TASK_1])
        r.add("system/cloud", "service_rate_2", self.system.cloud.rates[Task.TASK_2])
        r.add("system/cloud", "setup_mean", self.system.cloud.setup_mean)

        # Report - Statistics
        r.add("statistics", "population_mean", self.statistics.population.mean())
        r.add("statistics", "population_sdev", self.statistics.population.sdev())
        r.add("statistics", "population_cint", self.statistics.population.cint(alpha))

        r.add("statistics", "response_mean", self.statistics.response.mean())
        r.add("statistics", "response_sdev", self.statistics.response.sdev())
        r.add("statistics", "response_cint", self.statistics.response.cint(alpha))

        r.add("statistics", "throughput_mean", self.statistics.throughput.mean())
        r.add("statistics", "throughput_sdev", self.statistics.throughput.sdev())
        r.add("statistics", "throughput_cint", self.statistics.throughput.cint(alpha))

        return r

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
    config["general"]["n_batch"] = 10
    config["general"]["t_batch"] = 200
    simulation = Simulation(config)

    simulation.run()

    report = simulation.generate_report()

    print(report)