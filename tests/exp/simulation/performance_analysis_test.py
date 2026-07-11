import os
import tempfile
import unittest

from pydes.exp.simulation import performance_analysis

CONFIG_YAML = """
general:
  mode: "PERFORMANCE_ANALYSIS"
  batches: 3
  batchdim: 20
  confidence: 0.95
  rnd:
    generator: "MarcianiMultiStream"
    seed: 123456789

arrival:
  TASK_1:
    distribution: "EXPONENTIAL"
    parameters:
      r: 6.00
  TASK_2:
    distribution: "EXPONENTIAL"
    parameters:
      r: 6.25

system:
  cloudlet:
    n_servers: 2
    threshold: 2
    server_selection: "ORDER"
    controller_algorithm: "ALGORITHM_1"
    service:
      TASK_1:
        distribution: "EXPONENTIAL"
        parameters:
          r: 0.45
      TASK_2:
        distribution: "EXPONENTIAL"
        parameters:
          r: 0.27
  cloud:
    service:
      TASK_1:
        distribution: "EXPONENTIAL"
        parameters:
          r: 0.25
      TASK_2:
        distribution: "EXPONENTIAL"
        parameters:
          r: 0.22
    setup:
      TASK_1:
        distribution: "DETERMINISTIC"
        parameters:
          v: 0
      TASK_2:
        distribution: "EXPONENTIAL"
        parameters:
          m: 0.8
"""


class PerformanceAnalysisRunTest(unittest.TestCase):
    def setUp(self):
        """
        The test setup.
        :return: None
        """
        self.tmpdir = tempfile.mkdtemp()
        self.config_path = os.path.join(self.tmpdir, "config.yaml")
        with open(self.config_path, "w") as f:
            f.write(CONFIG_YAML)
        self.outdir = os.path.join(self.tmpdir, "out")

    def test_run(self):
        """
        Verify that run() executes a tiny performance analysis simulation (few batches, small
        batch dimension) and stores the txt/csv report.
        :return: None
        """
        performance_analysis.run(self.config_path, self.outdir, {})

        result_txt = os.path.join(self.outdir, "result.txt")
        result_csv = os.path.join(self.outdir, "result.csv")

        self.assertTrue(os.path.isfile(result_txt))
        self.assertTrue(os.path.isfile(result_csv))

        with open(result_txt) as f:
            content = f.read()
        self.assertIn("SIMULATION-CLOUD-CLOUDLET", content)
        self.assertIn("PERFORMANCE_ANALYSIS", content)

    def test_run_with_parameter_override(self):
        """
        Verify that run() honours the parameters dict, overriding the loaded configuration
        (e.g. reducing the number of batches even further).
        :return: None
        """
        parameters = {"general": {"batches": 2, "batchdim": 10}}

        performance_analysis.run(self.config_path, self.outdir, parameters)

        result_csv = os.path.join(self.outdir, "result.csv")
        self.assertTrue(os.path.isfile(result_csv))

        with open(result_csv) as f:
            csv_content = f.read()
        self.assertIn("general_batches", csv_content)


if __name__ == "__main__":
    unittest.main()
