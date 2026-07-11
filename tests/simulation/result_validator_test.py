import csv
import os
import shutil
import tempfile
import unittest

from pydes.core.simulation.result_validator import validate
from pydes.core.utils.report import SimpleReport
from tests import RES_DIR

ANALYTICAL_RESULT_PATH = os.path.join(RES_DIR, "analytical_result.csv")
SIMULATION_RESULT_PATH = os.path.join(RES_DIR, "simulation_result.csv")


def _read_single_row(path):
    with open(path, "r") as f:
        return list(csv.DictReader(f))[0]


def _write_single_row(path, row):
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(row.keys()))
        writer.writeheader()
        writer.writerow(row)


class ValidateTest(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmpdir, ignore_errors=True)

    def test_validate_with_real_result_files(self):
        """
        Validate a real analytical/simulation result pair (the same fixtures used by the
        pydes.exp.simulation.validation demo experiment).
        :return: None
        """
        report = validate(ANALYTICAL_RESULT_PATH, SIMULATION_RESULT_PATH)

        self.assertIsInstance(report, SimpleReport)
        self.assertEqual(report.title, "VALIDATION-CLOUD-CLOUDLET")

        total_entries = len(report.params.get("matching", [])) + len(report.params.get("not matching", []))
        # 3 indices * 3 system scopes * 3 task scopes.
        self.assertEqual(total_entries, 3 * 3 * 3)

    def test_validate_covers_threshold_check_when_algorithm_2(self):
        """
        When the controller algorithm is ALGORITHM_2, __verify_model_settings must also compare the
        cloudlet threshold between the analytical and simulation results. Use the real simulation
        fixture as a base (it already uses ALGORITHM_2), only patching the controller-algorithm value
        to match the current report format (bare enum name, not the qualified "ClassName.MEMBER" the
        legacy fixture uses).
        :return: None
        """
        row = _read_single_row(SIMULATION_RESULT_PATH)
        row["system_cloudlet_controller_algorithm"] = "ALGORITHM_2"

        analytical_path = os.path.join(self.tmpdir, "analytical_result.csv")
        simulation_path = os.path.join(self.tmpdir, "simulation_result.csv")
        _write_single_row(analytical_path, row)
        _write_single_row(simulation_path, row)

        report = validate(analytical_path, simulation_path)

        # Since both files are identical, every statistic must be reported as matching.
        self.assertEqual(len(report.params.get("not matching", [])), 0)
        self.assertGreater(len(report.params.get("matching", [])), 0)

    def test_validate_raises_on_system_settings_mismatch(self):
        """
        If the two result files describe different system configurations (e.g. a different number of
        cloudlet servers), validation must fail loudly rather than silently comparing incompatible runs.
        :return: None
        """
        row = _read_single_row(SIMULATION_RESULT_PATH)
        mismatched_row = dict(row)
        mismatched_row["system_cloudlet_n_servers"] = str(int(row["system_cloudlet_n_servers"]) + 1)

        analytical_path = os.path.join(self.tmpdir, "analytical_result.csv")
        simulation_path = os.path.join(self.tmpdir, "simulation_result.csv")
        _write_single_row(analytical_path, mismatched_row)
        _write_single_row(simulation_path, row)

        with self.assertRaises(AssertionError):
            validate(analytical_path, simulation_path)


if __name__ == "__main__":
    unittest.main()
