import os
import tempfile
import unittest
from unittest.mock import patch

from graphviz import Digraph

from pydes.exp.analytical import analytical_solution
from pydes.exp.simulation import performance_analysis, validation

ANALYTICAL_CONFIG_YAML = """
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

PERFORMANCE_CONFIG_YAML = """
general:
  mode: "PERFORMANCE_ANALYSIS"
  batches: 3
  batchdim: 20
  confidence: 0.95
  rnd:
    generator: "MarcianiMultiStream"
    seed: 123456789
""" + ANALYTICAL_CONFIG_YAML


class ValidationRunTest(unittest.TestCase):
    @patch.object(Digraph, "render")
    def setUp(self, mock_render):
        """
        The test setup: generate a real (tiny) analytical result and a real (tiny) simulation
        result, so that the CSV column layout consumed by validation.run() matches exactly what
        result_validator.validate()/result_printer.build_latex_table() expect.
        :return: None
        """
        self.tmpdir = tempfile.mkdtemp()

        analytical_config_path = os.path.join(self.tmpdir, "analytical.yaml")
        with open(analytical_config_path, "w") as f:
            f.write(ANALYTICAL_CONFIG_YAML)
        self.analytical_outdir = os.path.join(self.tmpdir, "analytical_out")
        analytical_solution.run(analytical_config_path, self.analytical_outdir, {})
        self.analytical_result_path = os.path.join(self.analytical_outdir, "result.csv")

        performance_config_path = os.path.join(self.tmpdir, "performance.yaml")
        with open(performance_config_path, "w") as f:
            f.write(PERFORMANCE_CONFIG_YAML)
        self.performance_outdir = os.path.join(self.tmpdir, "performance_out")
        performance_analysis.run(performance_config_path, self.performance_outdir, {})
        self.simulation_result_path = os.path.join(self.performance_outdir, "result.csv")

        self.outdir = os.path.join(self.tmpdir, "validation_out")

    def test_run(self):
        """
        Verify that run() validates the simulation result against the analytical one, and
        stores the txt/csv validation report.
        :return: None
        """
        validation.run(self.analytical_result_path, self.simulation_result_path, self.outdir)

        result_txt = os.path.join(self.outdir, "result.txt")
        result_csv = os.path.join(self.outdir, "result.csv")

        self.assertTrue(os.path.isfile(result_txt))
        self.assertTrue(os.path.isfile(result_csv))

        with open(result_txt) as f:
            content = f.read()
        self.assertIn("VALIDATION-CLOUD-CLOUDLET", content)


if __name__ == "__main__":
    unittest.main()
