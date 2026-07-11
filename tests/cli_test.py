import json
import logging
import os
import tempfile
import unittest
from os import path
from unittest.mock import patch

from click.testing import CliRunner

import pydes.cli as clim


class CliTest(unittest.TestCase):
    def setUp(self):
        """
        The test setup.
        :return: None
        """
        self.runner = CliRunner()
        self.tmpdir = tempfile.mkdtemp()

    def _touch(self, name):
        """
        Create an empty file under the temp directory, useful to satisfy Click options of type
        click.Path(exists=True).
        :param name: (string) the file name.
        :return: (string) the absolute path of the created file.
        """
        filepath = os.path.join(self.tmpdir, name)
        with open(filepath, "w") as f:
            f.write("")
        return filepath

    # ==================================================================================================================
    # GENERAL
    # ==================================================================================================================

    def test_help(self):
        """
        Verify that invoking with --help prints the usage and exits successfully.
        :return: None
        """
        result = self.runner.invoke(clim.main, ["--help"])

        self.assertEqual(0, result.exit_code)
        self.assertIn("Usage", result.output)
        self.assertIn("find-modulus", result.output)

    def test_no_subcommand_prints_help(self):
        """
        Verify that invoking without a subcommand prints the splash and the help, without error.
        :return: None
        """
        result = self.runner.invoke(clim.main, [])

        self.assertEqual(0, result.exit_code)
        self.assertIn("Usage", result.output)

    def test_debug_flag_sets_debug_log_level(self):
        """
        Verify that passing --debug activates the DEBUG log level, while its absence leaves the
        logger at INFO level.
        :return: None
        """
        with patch.object(clim.modulus, "run") as mock_run:
            result = self.runner.invoke(clim.main, ["--debug", "find-modulus", "--bits", "8", "--outdir", self.tmpdir])
        self.assertEqual(0, result.exit_code, result.output)
        self.assertEqual(logging.DEBUG, clim.logger.level)
        mock_run.assert_called_once_with(8, self.tmpdir)

        with patch.object(clim.modulus, "run") as mock_run:
            result = self.runner.invoke(clim.main, ["find-modulus", "--bits", "8", "--outdir", self.tmpdir])
        self.assertEqual(0, result.exit_code, result.output)
        self.assertEqual(logging.INFO, clim.logger.level)

    def test_version(self):
        """
        Verify that --version reports the expected version string.
        :return: None
        """
        result = self.runner.invoke(clim.main, ["--version"])

        self.assertEqual(0, result.exit_code)
        self.assertIn("0.0.1", result.output)

    # ==================================================================================================================
    # RND EXPERIMENTS
    # ==================================================================================================================

    def test_find_modulus(self):
        """
        Verify that find-modulus wires bits/outdir into modulus.run().
        :return: None
        """
        with patch.object(clim.modulus, "run") as mock_run:
            result = self.runner.invoke(clim.main, ["find-modulus", "--bits", "8", "--outdir", self.tmpdir])

        self.assertEqual(0, result.exit_code, result.output)
        mock_run.assert_called_once_with(8, self.tmpdir)

    def test_find_multipliers(self):
        """
        Verify that find-multipliers wires modulus/outdir into mulfind.run().
        :return: None
        """
        with patch.object(clim.mulfind, "run") as mock_run:
            result = self.runner.invoke(clim.main, ["find-multipliers", "--modulus", "31", "--outdir", self.tmpdir])

        self.assertEqual(0, result.exit_code, result.output)
        mock_run.assert_called_once_with(31, self.tmpdir)

    def test_find_jumpers(self):
        """
        Verify that find-jumpers wires modulus/multiplier/streams/outdir into jumpfind.run().
        :return: None
        """
        with patch.object(clim.jumpfind, "run") as mock_run:
            result = self.runner.invoke(
                clim.main,
                [
                    "find-jumpers",
                    "--modulus",
                    "127",
                    "--multiplier",
                    "3",
                    "--streams",
                    "8",
                    "--outdir",
                    self.tmpdir,
                ],
            )

        self.assertEqual(0, result.exit_code, result.output)
        mock_run.assert_called_once_with(127, 3, 8, self.tmpdir)

    def test_check_multiplier(self):
        """
        Verify that check-multiplier wires modulus/multiplier/outdir into mulcheck.run().
        :return: None
        """
        with patch.object(clim.mulcheck, "run") as mock_run:
            result = self.runner.invoke(
                clim.main,
                ["check-multiplier", "--modulus", "31", "--multiplier", "3", "--outdir", self.tmpdir],
            )

        self.assertEqual(0, result.exit_code, result.output)
        mock_run.assert_called_once_with(31, 3, self.tmpdir)

    def test_test_spectral(self):
        """
        Verify that test-spectral builds a MarcianiSingleStream generator with the given
        modulus/multiplier and wires it, together with samsize/interval/outdir, into
        spectral.run().
        :return: None
        """
        with patch.object(clim.spectral, "run") as mock_run:
            result = self.runner.invoke(
                clim.main,
                [
                    "test-spectral",
                    "--modulus",
                    "127",
                    "--multiplier",
                    "3",
                    "--samsize",
                    "50",
                    "--outdir",
                    self.tmpdir,
                ],
            )

        self.assertEqual(0, result.exit_code, result.output)
        mock_run.assert_called_once()
        call_args = mock_run.call_args[0]
        generator = call_args[0]
        self.assertEqual(127, generator.get_modulus())
        self.assertEqual(3, generator.get_multiplier())
        self.assertEqual(50, call_args[1])
        self.assertEqual(self.tmpdir, call_args[3])

    def test_test_extremes(self):
        """
        Verify that test-extremes builds a MarcianiMultiStream generator with the given
        modulus/multiplier/jumper/streams and wires it, together with the remaining test
        parameters, into extremes.run().
        :return: None
        """
        with patch.object(clim.extremes, "run") as mock_run:
            result = self.runner.invoke(
                clim.main,
                [
                    "test-extremes",
                    "--modulus",
                    "127",
                    "--multiplier",
                    "3",
                    "--jumper",
                    "9",
                    "--streams",
                    "20",
                    "--samsize",
                    "50",
                    "--bins",
                    "10",
                    "--confidence",
                    "0.95",
                    "--d",
                    "2",
                    "--outdir",
                    self.tmpdir,
                ],
            )

        self.assertEqual(0, result.exit_code, result.output)
        mock_run.assert_called_once()
        generator, samsize, bins, confidence, d, outdir = mock_run.call_args[0]
        self.assertEqual(127, generator.get_modulus())
        self.assertEqual(3, generator.get_multiplier())
        self.assertEqual(9, generator.get_jumper())
        self.assertEqual(20, generator.get_nstreams())
        self.assertEqual(50, samsize)
        self.assertEqual(10, bins)
        self.assertEqual(0.95, confidence)
        self.assertEqual(2, d)
        self.assertEqual(self.tmpdir, outdir)

    def test_test_kolmogorov_smirnov(self):
        """
        Verify that test-kolmogorov-smirnov builds a MarcianiMultiStream generator, parses the
        JSON test-params string into a dict, and wires everything into kolmogorov_smirnov.run().
        This also exercises the fix for the bug where test_params used to be forwarded as a raw
        (unparsed) string, causing a TypeError inside kolmogorov_smirnov.run().
        :return: None
        """
        test_params = {"samsize": 50, "bins": 10, "confidence": 0.95, "d": 2}
        with patch.object(clim.kolmogorov_smirnov, "run") as mock_run:
            result = self.runner.invoke(
                clim.main,
                [
                    "test-kolmogorov-smirnov",
                    "--modulus",
                    "127",
                    "--multiplier",
                    "3",
                    "--jumper",
                    "9",
                    "--streams",
                    "20",
                    "--test",
                    "extremes",
                    "--test-params",
                    json.dumps(test_params),
                    "--outdir",
                    self.tmpdir,
                ],
            )

        self.assertEqual(0, result.exit_code, result.output)
        mock_run.assert_called_once()
        generator, test_name, params, outdir = mock_run.call_args[0]
        self.assertEqual(127, generator.get_modulus())
        self.assertEqual("extremes", test_name)
        self.assertEqual(test_params, params)
        self.assertIsInstance(params, dict)
        self.assertEqual(path.join(self.tmpdir, "extremes"), outdir)

    def test_test_kolmogorov_smirnov_default_test_params(self):
        """
        Verify that test-kolmogorov-smirnov works with the default --test-params value (i.e. the
        default is valid JSON and correctly round-trips into a dict).
        :return: None
        """
        with patch.object(clim.kolmogorov_smirnov, "run") as mock_run:
            result = self.runner.invoke(
                clim.main,
                [
                    "test-kolmogorov-smirnov",
                    "--modulus",
                    "127",
                    "--multiplier",
                    "3",
                    "--jumper",
                    "9",
                    "--streams",
                    "20",
                    "--outdir",
                    self.tmpdir,
                ],
            )

        self.assertEqual(0, result.exit_code, result.output)
        params = mock_run.call_args[0][2]
        self.assertIsInstance(params, dict)
        self.assertEqual(10000, params["samsize"])

    # ==================================================================================================================
    # SIMULATION / ANALYTICAL EXPERIMENTS
    # ==================================================================================================================

    def test_simulate_transient(self):
        """
        Verify that simulate-transient wires config/outdir/parameters (parsed from JSON) into
        transient_analysis.run().
        :return: None
        """
        config_path = self._touch("transient.yaml")
        with patch.object(clim.transient_analysis, "run") as mock_run:
            result = self.runner.invoke(
                clim.main,
                [
                    "simulate-transient",
                    "--config",
                    config_path,
                    "--outdir",
                    self.tmpdir,
                    "--parameters",
                    '{"general": {"replications": 1}}',
                ],
            )

        self.assertEqual(0, result.exit_code, result.output)
        mock_run.assert_called_once_with(config_path, self.tmpdir, {"general": {"replications": 1}})

    def test_simulate_performance(self):
        """
        Verify that simulate-performance wires config/outdir/parameters (parsed from JSON) into
        performance_analysis.run().
        :return: None
        """
        config_path = self._touch("performance.yaml")
        with patch.object(clim.performance_analysis, "run") as mock_run:
            result = self.runner.invoke(
                clim.main,
                [
                    "simulate-performance",
                    "--config",
                    config_path,
                    "--outdir",
                    self.tmpdir,
                    "--parameters",
                    '{"general": {"batches": 2}}',
                ],
            )

        self.assertEqual(0, result.exit_code, result.output)
        mock_run.assert_called_once_with(config_path, self.tmpdir, {"general": {"batches": 2}})

    def test_solve_cloud_cloudlet(self):
        """
        Verify that solve-cloud-cloudlet wires config/outdir/parameters (parsed from JSON) into
        analytical_solution.run().
        :return: None
        """
        config_path = self._touch("analytical.yaml")
        with patch.object(clim.analytical_solution, "run") as mock_run:
            result = self.runner.invoke(
                clim.main,
                [
                    "solve-cloud-cloudlet",
                    "--config",
                    config_path,
                    "--outdir",
                    self.tmpdir,
                    "--parameters",
                    '{"system": {"cloudlet": {"threshold": 5}}}',
                ],
            )

        self.assertEqual(0, result.exit_code, result.output)
        mock_run.assert_called_once_with(config_path, self.tmpdir, {"system": {"cloudlet": {"threshold": 5}}})

    def test_validate_cloud_cloudlet(self):
        """
        Verify that validate-cloud-cloudlet wires analytical-result/simulation-result/outdir
        into validation.run().
        :return: None
        """
        analytical_result_path = self._touch("analytical_result.csv")
        simulation_result_path = self._touch("simulation_result.csv")
        with patch.object(clim.validation, "run") as mock_run:
            result = self.runner.invoke(
                clim.main,
                [
                    "validate-cloud-cloudlet",
                    "--analytical-result",
                    analytical_result_path,
                    "--simulation-result",
                    simulation_result_path,
                    "--outdir",
                    self.tmpdir,
                ],
            )

        self.assertEqual(0, result.exit_code, result.output)
        mock_run.assert_called_once_with(analytical_result_path, simulation_result_path, self.tmpdir)

    # ==================================================================================================================
    # ERROR HANDLING
    # ==================================================================================================================

    def test_simulate_transient_missing_config_fails(self):
        """
        Verify that a missing --config file is rejected by Click before reaching the callback.
        :return: None
        """
        result = self.runner.invoke(
            clim.main,
            ["simulate-transient", "--config", os.path.join(self.tmpdir, "does_not_exist.yaml")],
        )

        self.assertNotEqual(0, result.exit_code)


if __name__ == "__main__":
    unittest.main()
