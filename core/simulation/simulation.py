from core.simulation.model.system import SimpleCloudletCloudSystem as System
from core.simulation.model.scope import SystemScope
from core.simulation.model.scope import TaskScope
from core.utils.report import SimpleReport as Report
from core.random import rndgen
from core.simulation.model.taskgen import SimpleTaskgen as Taskgen
from core.simulation.model.calendar import NextEventCalendar as Calendar
from core.simulation.model.event import EventType, ActionScope
from core.utils.guiutils import print_progress
from core.simulation.model.stats import SimulationStatistics
from core.utils.file_utils import empty_file
import os
from core.utils.logutils import get_logger


# Logging
logger = get_logger(__name__)


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
        self.t_batch = (self.t_stop - self.t_tran) / self.n_batch
        self.confidence = config_general["confidence"]
        self.rndgen = getattr(rndgen, config_general["random"]["generator"])(config_general["random"]["seed"])
        self.t_sample = config["general"]["t_sample"] if config["general"]["t_sample"] is not None else float("inf")

        # The statistics
        self.statistics = SimulationStatistics(self.t_batch)

        # Configuration - Tasks
        self.taskgen = Taskgen(
            self.rndgen,
            config["arrival"],
            self.t_stop
        )

        # Configuration - System (Cloudlet and Cloud)
        config_system = config["system"]
        self.system = System(
            self.rndgen,
            config_system,
            self.statistics
        )

        # Configuration - Calendar
        # Notice that the calendar internally manages:
        # (i) event sorting, by occurrence time.
        # (ii) scheduling of only possible events, that are:
        #   (ii.i) possible arrivals, i.e. arrivals with occurrence time lower than stop time.
        #   (ii.ii) departures of possible arrivals.
        # (iii) unscheduling of events to ignore, e.g. completion in Cloudlet of interrupted tasks of type 2.
        self.calendar = Calendar(0.0, self.t_stop, EventType.arrivals())

        # Sampling management
        self.t_last_sample = 0
        self.sampling_file = None

        # Batch management
        self.curr_batch = 0
        self.transient_mark = False
        self.t_last_batch = self.t_tran

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
            self.sampling_file = os.path.join(outdir, "result.sampling.csv")
            empty_file(self.sampling_file)

        # Simulation Start.
        logger.info("Simulation started")

        # Initialize first arrivals
        # Schedule the first events, i.e. task of type 1 and 2.
        # Notice that the event order by arrival time is managed internally by the Calendar.
        self.calendar.schedule(self.taskgen.generate(self.calendar.get_clock()))

        # Run the simulation while the calendar clock is less than the stop time.
        while self.calendar.get_clock() < self.t_stop:

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
            if event.type.action is ActionScope.ARRIVAL:
                self.calendar.schedule(self.taskgen.generate(self.calendar.get_clock()))

            # Simulation progress
            if show_progress:
                print_progress(self.calendar.get_clock(), self.t_stop)

            # If transient period has been passed...
            if self.calendar.get_clock() > self.t_tran:

                # Write sampling data
                if self.sampling_file is not None and self.calendar.get_clock() >= self.t_last_sample + self.t_sample:
                    self.statistics.sample(self.calendar.get_clock()).save_csv(self.sampling_file, append=True)
                    self.t_last_sample = self.calendar.get_clock()

                # Discard batch data collected during the transient period
                if not self.transient_mark:
                    self.statistics.discard_batch()
                    self.transient_mark = True

                # Record batch data
                if self.calendar.get_clock() >= self.t_last_batch + self.t_batch:
                    self.statistics.register_batch()
                    self.curr_batch += 1
                    self.t_last_batch = self.calendar.get_clock()

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
        r.add("general", "t_tran", self.t_tran)
        r.add("general", "n_batch", self.n_batch)
        r.add("general", "t_batch", self.t_batch)

        # Report - Randomization
        r.add("randomization", "generator", self.rndgen.__class__.__name__)
        r.add("randomization", "iseed", self.rndgen.get_initial_seed())
        r.add("randomization", "modulus", self.rndgen.get_modulus())
        r.add("randomization", "multiplier", self.rndgen.get_multiplier())
        r.add("randomization", "streams", self.rndgen.get_nstreams())

        # Report - Arrivals
        for tsk in TaskScope.concrete():
            r.add("arrival", "arrival_{}_dist".format(tsk.name.lower()), self.taskgen.rndarrival.var[tsk].name.lower())
            for p in self.taskgen.rndarrival.par[tsk]:
                r.add("arrival", "arrival_{}_param_{}".format(tsk.name.lower(), p), self.taskgen.rndarrival.par[tsk][p])
        for tsk in TaskScope.concrete():
            r.add("arrival", "generated_{}".format(tsk.name.lower()), self.taskgen.generated[tsk])

        # Report - System/Cloudlet
        r.add("system/cloudlet", "n_servers", self.system.cloudlet.n_servers)
        r.add("system/cloudlet", "threshold", self.system.cloudlet.threshold)
        for tsk in TaskScope.concrete():
            r.add("system/cloudlet", "service_{}_dist".format(tsk.name.lower()), self.system.cloudlet.rndservice.var[tsk].name.lower())
            for p in self.system.cloudlet.rndservice.par[tsk]:
                r.add("system/cloudlet", "service_{}_param_{}".format(tsk.name.lower(), p), self.system.cloudlet.rndservice.par[tsk][p])

        # Report - System/Cloud
        for tsk in TaskScope.concrete():
            r.add("system/cloud", "service_{}_dist".format(tsk.name.lower()), self.system.cloud.rndservice.var[tsk].name.lower())
            for p in self.system.cloud.rndservice.par[tsk]:
                r.add("system/cloud", "service_{}_param_{}".format(tsk.name.lower(), p), self.system.cloud.rndservice.par[tsk][p])

        for tsk in TaskScope.concrete():
            r.add("system/cloud", "setup_{}_dist".format(tsk.name.lower()), self.system.cloud.rndsetup.var[tsk].name.lower())
            for p in self.system.cloud.rndsetup.par[tsk]:
                r.add("system/cloud", "service_{}_param_{}".format(tsk.name.lower(), p), self.system.cloud.rndsetup.par[tsk][p])

        # Report - State
        for sys in sorted(self.system.state, key=lambda x: x.name):
            for tsk in sorted(self.system.state[sys], key=lambda x: x.name):
                r.add("state", "{}_{}".format(sys.name.lower(), tsk.name.lower()), self.system.state[sys][tsk])

        # Report - Statistics
        for metric in sorted(self.statistics.metrics.__dict__):
            for sys in sorted(SystemScope, key=lambda x: x.name):
                for tsk in sorted(TaskScope, key=lambda x: x.name):
                    r.add("statistics", "{}_{}_{}_mean".format(metric, sys.name.lower(), tsk.name.lower()),
                          getattr(self.statistics.metrics, metric)[sys][tsk].mean())
                    r.add("statistics", "{}_{}_{}_sdev".format(metric, sys.name.lower(), tsk.name.lower()),
                          getattr(self.statistics.metrics, metric)[sys][tsk].sdev())
                    r.add("statistics", "{}_{}_{}_cint".format(metric, sys.name.lower(), tsk.name.lower()),
                          getattr(self.statistics.metrics, metric)[sys][tsk].cint(alpha))
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
    from core.simulation.model.config import get_default_configuration

    config = get_default_configuration()
    config["general"]["n_batch"] = 10
    config["general"]["t_batch"] = 200
    simulation = Simulation(config)

    simulation.run(show_progress=True)

    report = simulation.generate_report()

    print(report)