import copy
import os
import unittest

from pydes.core.rnd.rndvar import Variate
from pydes.core.simulation.model.config import (
    _normalize_random_config,
    get_default_configuration,
    load_configuration,
)
from pydes.core.simulation.model.controller import ControllerAlgorithm
from pydes.core.simulation.model.scope import TaskScope
from pydes.core.simulation.model.server_selection import SelectionRule
from pydes.core.simulation.simulation_mode import SimulationMode

# Resolved relative to this test file (not the installed pydes package) so that
# the fixtures are found whether pydes is installed editable or as a real wheel.
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
RESOURCES_CONFIG_DIR = os.path.join(REPO_ROOT, "resources", "config")


class GetDefaultConfigurationTest(unittest.TestCase):
    def test_performance_analysis_defaults(self):
        """
        Verify the defaults for PERFORMANCE_ANALYSIS mode.
        :return: None
        """
        config = get_default_configuration(SimulationMode.PERFORMANCE_ANALYSIS)
        self.assertEqual(config["general"]["mode"], SimulationMode.PERFORMANCE_ANALYSIS)
        self.assertEqual(config["general"]["batches"], 10)
        self.assertEqual(config["general"]["batchdim"], 100)
        self.assertNotIn("t_stop", config["general"])

    def test_transient_analysis_defaults(self):
        """
        Verify the defaults for TRANSIENT_ANALYSIS mode.
        :return: None
        """
        config = get_default_configuration(SimulationMode.TRANSIENT_ANALYSIS)
        self.assertEqual(config["general"]["mode"], SimulationMode.TRANSIENT_ANALYSIS)
        self.assertEqual(config["general"]["replications"], 5)
        self.assertEqual(config["general"]["t_stop"], 3600)
        self.assertNotIn("batches", config["general"])
        self.assertNotIn("batchdim", config["general"])

    def test_normalize_converts_types(self):
        """
        Verify that normalize() coerces string values into the expected types.
        :return: None
        """
        config = get_default_configuration()

        self.assertIsInstance(config["general"]["mode"], SimulationMode)
        self.assertEqual(config["general"]["rnd"]["generator"], "MarcianiMultiStream")

        self.assertIsInstance(
            config["system"]["cloudlet"]["server_selection"],
            SelectionRule,
        )
        self.assertIsInstance(
            config["system"]["cloudlet"]["controller_algorithm"],
            ControllerAlgorithm,
        )

        for tsk in TaskScope.concrete():
            self.assertIsInstance(config["arrival"][tsk]["distribution"], Variate)
            # The arrival rate "r" is converted to a mean inter-arrival time "m".
            self.assertIn("m", config["arrival"][tsk]["parameters"])
            self.assertNotIn("r", config["arrival"][tsk]["parameters"])

    def test_normalize_random_config_is_idempotent(self):
        """
        Verify that calling _normalize_random_config() on an already-normalized entry (i.e. one keyed
        by TaskScope rather than strings) is a no-op for those entries (covers the "already normalized"
        branch, exercised e.g. when normalize() processes an entry more than once).
        :return: None
        """
        config = get_default_configuration()
        before = copy.deepcopy(config["arrival"])

        _normalize_random_config(config["arrival"])

        self.assertEqual(set(before.keys()), set(config["arrival"].keys()))
        for tsk in TaskScope.concrete():
            self.assertEqual(config["arrival"][tsk]["distribution"], before[tsk]["distribution"])
            self.assertEqual(config["arrival"][tsk]["parameters"], before[tsk]["parameters"])


class LoadConfigurationTest(unittest.TestCase):
    def test_load_performance_analysis_configuration_from_file(self):
        """
        Verify loading and normalizing a PERFORMANCE_ANALYSIS configuration from a real YAML resource file.
        Notice: the resource file uses the legacy "random" key (instead of "rnd"), which normalize() must
        transparently rename for the configuration to be usable by Simulation.
        :return: None
        """
        path = os.path.join(RESOURCES_CONFIG_DIR, "performance_analysis_1.yaml")
        config = load_configuration(path)

        self.assertEqual(config["general"]["mode"], SimulationMode.PERFORMANCE_ANALYSIS)
        self.assertEqual(config["general"]["batches"], 64)
        self.assertEqual(config["general"]["batchdim"], 512)
        self.assertIn("rnd", config["general"])
        self.assertNotIn("random", config["general"])
        self.assertEqual(config["general"]["rnd"]["seed"], 123456789)

        self.assertEqual(
            config["system"]["cloudlet"]["controller_algorithm"],
            ControllerAlgorithm.ALGORITHM_1,
        )
        self.assertEqual(config["system"]["cloudlet"]["server_selection"], SelectionRule.RANDOM)

    def test_load_transient_analysis_configuration_from_file(self):
        """
        Verify loading and normalizing a TRANSIENT_ANALYSIS configuration from a real YAML resource file.
        :return: None
        """
        path = os.path.join(RESOURCES_CONFIG_DIR, "transient_analysis_1.yaml")
        config = load_configuration(path)

        self.assertEqual(config["general"]["mode"], SimulationMode.TRANSIENT_ANALYSIS)
        self.assertEqual(config["general"]["t_stop"], 3000)
        self.assertEqual(config["general"]["replications"], 5)
        self.assertIn("rnd", config["general"])
        self.assertEqual(config["general"]["rnd"]["seed"], 123456789)

    def test_load_configuration_without_normalization(self):
        """
        Verify that norm=False leaves the configuration untouched (raw strings, legacy keys).
        :return: None
        """
        path = os.path.join(RESOURCES_CONFIG_DIR, "performance_analysis_1.yaml")
        config = load_configuration(path, norm=False)

        self.assertEqual(config["general"]["mode"], "PERFORMANCE_ANALYSIS")
        self.assertIn("random", config["general"])
        self.assertNotIn("rnd", config["general"])


if __name__ == "__main__":
    unittest.main()
