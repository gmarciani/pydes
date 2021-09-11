from core.rnd.rndvar import Variate
from core.simulation.model.system import SimpleCloudletCloudSystem as System
from core.simulation.model.scope import SystemScope
from core.simulation.model.scope import TaskScope
from core.utils.report import SimpleReport as Report
from core.rnd import rndgen
from core.simulation.model.taskgen import ExponentialTaskgen as Taskgen
from core.simulation.model.calendar import NextEventCalendar as Calendar
from core.simulation.model.event import ActionScope
from core.utils.guiutils import print_progress
from core.metrics.simulation_metrics import SimulationMetrics
from core.utils.file_utils import empty_file
from core.simulation.simulation_mode import SimulationMode
from core.simulation.model.controller import ControllerAlgorithm
from math import floor

from sys import maxsize as INFINITE
import os


# Logging
# logger = get_logger(__name__)


class Simulation:
    """
    A simple simulation of a two-layers Cloud computing system.
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
        self.mode = config_general["mode"]

        # Configuration - Transient Analysis
        if self.mode is SimulationMode.TRANSIENT_ANALYSIS:
            self.t_stop = config_general["t_stop"]
            # self.t_tran = 0
            self.batches = INFINITE
            self.batchdim = 1
            self.closed_door_condition = lambda: self.closed_door_condition_transient_analysis()
            self.print_progress = lambda: print_progress(
                self.calendar.get_clock(), self.t_stop, message="Clock: %d" % (self.calendar.get_clock())
            )
            # self.should_discard_transient_data = False

        # Configuration - Performance Analysis
        elif self.mode is SimulationMode.PERFORMANCE_ANALYSIS:
            self.t_stop = INFINITE
            # self.t_tran = config_general["t_tran"]
            self.batches = config_general["batches"]
            self.batchdim = config_general["batchdim"]
            self.closed_door_condition = lambda: self.closed_door_condition_performance_analysis()
            self.print_progress = lambda: print_progress(
                self.metrics.n_batches,
                self.batches,
                message="Clock: %d | Batches: %d | CurrentBatchSamples: %d"
                % (self.calendar.get_clock(), self.metrics.n_batches, self.metrics.curr_batchdim),
            )
            # self.should_discard_transient_data = self.t_tran > 0.0

        else:
            raise RuntimeError("The current version supports only TRANSIENT_ANALYSIS and PERFORMANCE_ANALYSIS")

        # Configuration - Randomization
        self.rndgen = getattr(rndgen, config_general["random"]["generator"])(config_general["random"]["seed"])

        # The simulation metrics
        self.metrics = SimulationMetrics(self.batchdim)
        self.confidence = config_general["confidence"]

        # Configuration - Tasks
        # Checks that the arrival process is Markovian (currently, the only one supported)
        if not all(
            variate is Variate.EXPONENTIAL
            for variate in [config["arrival"][tsk]["distribution"] for tsk in TaskScope.concrete()]
        ):
            raise NotImplementedError("The current version supports only exponential arrivals")
        self.taskgen = Taskgen(rndgen=self.rndgen, config=config["arrival"])

        # Configuration - System (Cloudlet and Cloud)
        config_system = config["system"]
        self.system = System(rndgen=self.rndgen, config=config_system, metrics=self.metrics)

        # Configuration - Calendar
        # Notice that the calendar internally manages:
        # (i) event sorting, by occurrence time.
        # (ii) scheduling of only possible events, that are:
        #   (ii.i) possible arrivals, i.e. arrivals with occurrence time lower than stop time.
        #   (ii.ii) departures of possible arrivals.
        # (iii) unscheduling of events to ignore, e.g. completion in Cloudlet of interrupted tasks.
        self.calendar = Calendar(t_clock=0.0)

        # Sampling management
        self.sampling_file = None

        # Simulation management
        self.closed_door = False

    # ==================================================================================================================
    # SIMULATION PROCESS
    # ==================================================================================================================

    def run(self, outdir=None, show_progress=False):
        """
        Run the simulation.
        :param outdir (string) the directory for output files (Default: None)
        :param show_progress (bool) if True, print the simulation real time progress bar.
        :param sampling (bool) if True, save samples into a dedicated file. (Default:False)
        :return: None
        """

        # Initialize sampling
        self.sampling_file = os.path.join(outdir, "result.sampling.csv")
        empty_file(self.sampling_file)

        # Initialize first arrivals
        # Schedule the first events, i.e. task of type 1 and 2.
        # Notice that the event order by arrival time is managed internally by the Calendar.
        self.calendar.schedule(self.taskgen.generate(self.calendar.get_clock()))

        # Run the simulation until the stop condition holds true
        while not self.stop_condition():

            # Get the next event and update the calendar clock.
            # Notice that the Calendar clock is automatically updated.
            # Notice that the next event is always a possible event.
            event = self.calendar.get_next_event()

            # Check the closed-door condition
            self.closed_door = self.closed_door_condition()

            # Submit the event to the system if:
            #   * the closed door condition is False
            #   * the closed door condition is True, but the event is not an ARRIVAL
            # Notice that every submission generates some other events to be scheduled/unscheduled,
            # e.g., completions and interruptions (i.e., completions to be ignored).
            if self.closed_door is False or event.type.act is not ActionScope.ARRIVAL:
                events_to_schedule, events_to_unschedule = self.system.submit(event)
                # Schedule/Unschedule response events
                self.calendar.schedule(*events_to_schedule)
                self.calendar.unschedule(*events_to_unschedule)

            # If the last event was an arrival and the closed-door condition does not hold, schedule a new arrival
            # Notice that, impossible events are automatically ignored by the calendar
            if event.type.act is ActionScope.ARRIVAL and self.closed_door is False:
                self.calendar.schedule(self.taskgen.generate(self.calendar.get_clock()))

            # Sampling
            if self.sampling_condition(event):
                sample = self.metrics.sampling(self.calendar.get_clock())
                sample.save_csv(self.sampling_file, append=True)

            # Simulation progress
            if show_progress:
                self.print_progress()

    # ==================================================================================================================
    # CONDITIONS
    # ==================================================================================================================

    def stop_condition(self):
        """
        Checks whether the stop condition holds true.
        The stop condition holds true when the closed door condition hilds true and the system is idle.
        :return: true, if the stop condition holds; false, otherwise.
        """
        return self.closed_door and self.system.is_idle()

    def closed_door_condition_performance_analysis(self):
        """
        Checks whether the closed door condition holds true (PERFORMANCE_ANALYSIS).
        The closed door condition holds true if the desired number of batches have been collected
        :return: true, if the closed door condition holds; false, otherwise.
        """
        return self.metrics.n_batches >= self.batches

    def closed_door_condition_transient_analysis(self):
        """
        Checks whether the closed door condition holds true (TRANSIENT_ANALYSIS).
        The closed door condition holds true if the clock time passed the stop time.
        :return: true, if the closed door condition holds; false, otherwise.
        """
        return self.calendar.get_clock() >= self.t_stop

    def sampling_condition(self, event):
        """
        Checks whether the sampling condition holds true.
        The sampling condition holds true on completion events.
        :return: true, if the sampling condition holds; false, otherwise.
        """
        return event.type.act is ActionScope.COMPLETION

    # ==================================================================================================================
    # REPORT
    # ==================================================================================================================

    def generate_report(self):
        """
        Generate the simulation report.
        :return: (SimpleReport) the simulation report.
        """
        r = Report(self.name)

        alpha = 1.0 - self.confidence

        # Report - General
        r.add("general", "mode", self.mode.name)
        if self.mode is SimulationMode.TRANSIENT_ANALYSIS:
            r.add("general", "t_stop", self.t_stop)
        elif self.mode is SimulationMode.PERFORMANCE_ANALYSIS:
            r.add("general", "batches", self.batches)
            r.add("general", "batchdim", self.batchdim)
        else:
            raise RuntimeError("The current version supports only TRANSIENT_ANALYSIS and PERFORMANCE_ANALYSIS")
        r.add("general", "confidence", self.confidence)

        # Report - Randomization
        r.add("randomization", "generator", self.rndgen.__class__.__name__)
        r.add("randomization", "iseed", self.rndgen.get_initial_seed())
        r.add("randomization", "modulus", self.rndgen.get_modulus())
        r.add("randomization", "multiplier", self.rndgen.get_multiplier())
        r.add("randomization", "streams", self.rndgen.get_nstreams())

        # Report - Arrivals
        for tsk in TaskScope.concrete():
            r.add("arrival", "arrival_{}_dist".format(tsk.name.lower()), Variate.EXPONENTIAL.name)
            r.add("arrival", "arrival_{}_rate".format(tsk.name.lower()), self.taskgen.rates[tsk])
        for tsk in TaskScope.concrete():
            r.add("arrival", "generated_{}".format(tsk.name.lower()), self.taskgen.generated[tsk])

        # Report - System/Cloudlet
        r.add("system/cloudlet", "n_servers", self.system.cloudlet.n_servers)
        r.add("system/cloudlet", "controller_algorithm", self.system.cloudlet.controller.controller_algorithm.name)
        if self.system.cloudlet.controller.controller_algorithm is ControllerAlgorithm.ALGORITHM_2:
            r.add("system/cloudlet", "threshold", self.system.cloudlet.threshold)
        for tsk in TaskScope.concrete():
            r.add(
                "system/cloudlet",
                "service_{}_dist".format(tsk.name.lower()),
                self.system.cloudlet.rndservice.var[tsk].name,
            )
            if self.system.cloudlet.rndservice.var[tsk] is Variate.EXPONENTIAL:
                r.add(
                    "system/cloudlet",
                    "service_{}_rate".format(tsk.name.lower()),
                    1.0 / self.system.cloudlet.rndservice.par[tsk]["m"],
                )
            else:
                for p in self.system.cloudlet.rndservice.par[tsk]:
                    r.add(
                        "system/cloudlet",
                        "service_{}_param_{}".format(tsk.name.lower(), p),
                        self.system.cloudlet.rndservice.par[tsk][p],
                    )

        # Report - System/Cloud
        for tsk in TaskScope.concrete():
            r.add(
                "system/cloud", "service_{}_dist".format(tsk.name.lower()), self.system.cloud.rndservice.var[tsk].name
            )
            if self.system.cloud.rndservice.var[tsk] is Variate.EXPONENTIAL:
                r.add(
                    "system/cloud",
                    "service_{}_rate".format(tsk.name.lower()),
                    1.0 / self.system.cloud.rndservice.par[tsk]["m"],
                )
            else:
                for p in self.system.cloud.rndservice.par[tsk]:
                    r.add(
                        "system/cloud",
                        "service_{}_param_{}".format(tsk.name.lower(), p),
                        self.system.cloud.rndservice.par[tsk][p],
                    )

        for tsk in TaskScope.concrete():
            r.add("system/cloud", "setup_{}_dist".format(tsk.name.lower()), self.system.cloud.rndsetup.var[tsk].name)
            for p in self.system.cloud.rndsetup.par[tsk]:
                r.add(
                    "system/cloud",
                    "service_{}_param_{}".format(tsk.name.lower(), p),
                    self.system.cloud.rndsetup.par[tsk][p],
                )

        # Report - Execution
        r.add("execution", "clock", self.calendar.get_clock())
        r.add("execution", "collected_samples", self.metrics.n_samples)
        r.add("execution", "collected_batches", self.metrics.n_batches)

        # Report - State
        for sys in sorted(self.system.state, key=lambda x: x.name):
            for tsk in sorted(self.system.state[sys], key=lambda x: x.name):
                r.add("state", "{}_{}".format(sys.name.lower(), tsk.name.lower()), self.system.state[sys][tsk])

        # Report - Statistics
        for metric in sorted(self.metrics.performance_metrics.__dict__):
            for sys in sorted(SystemScope, key=lambda x: x.name):
                for tsk in sorted(TaskScope, key=lambda x: x.name):
                    r.add(
                        "statistics",
                        "{}_{}_{}_mean".format(metric, sys.name.lower(), tsk.name.lower()),
                        getattr(self.metrics.performance_metrics, metric)[sys][tsk].mean(),
                    )
                    r.add(
                        "statistics",
                        "{}_{}_{}_sdev".format(metric, sys.name.lower(), tsk.name.lower()),
                        getattr(self.metrics.performance_metrics, metric)[sys][tsk].sdev(),
                    )
                    r.add(
                        "statistics",
                        "{}_{}_{}_cint".format(metric, sys.name.lower(), tsk.name.lower()),
                        getattr(self.metrics.performance_metrics, metric)[sys][tsk].cint(alpha),
                    )

        return r

    # ==================================================================================================================
    # OTHER
    # ==================================================================================================================

    def __str__(self):
        """
        String representation.
        :return: the string representation.
        """
        sb = [
            "{attr}={value}".format(attr=attr, value=self.__dict__[attr])
            for attr in self.__dict__
            if not attr.startswith("__") and not callable(getattr(self, attr))
        ]
        return "Simulation({}:{})".format(id(self), ", ".join(sb))


if __name__ == "__main__":
    from core.simulation.model.config import get_default_configuration

    mode = SimulationMode.TRANSIENT_ANALYSIS
    # mode = SimulationMode.PERFORMANCE_ANALYSIS

    config = get_default_configuration(mode)

    simulation = Simulation(config, name=mode.name)

    simulation.run(show_progress=True)

    report = simulation.generate_report()

    print(report)
