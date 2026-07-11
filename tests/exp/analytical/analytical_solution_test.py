import os
import tempfile
import unittest
from unittest.mock import patch

from graphviz import Digraph

from pydes.exp.analytical import analytical_solution

CONFIG_YAML = """
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


class AnalyticalSolutionRunTest(unittest.TestCase):
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

    @patch.object(Digraph, "render")
    def test_run(self, mock_render):
        """
        Verify that run() solves the analytical model with a small state space (2 servers)
        and stores the txt/csv report. The Markov Chain rendering is mocked out since the
        test environment has no 'dot' executable available.
        :return: None
        """
        analytical_solution.run(self.config_path, self.outdir, {})

        result_txt = os.path.join(self.outdir, "result.txt")
        result_csv = os.path.join(self.outdir, "result.csv")

        self.assertTrue(os.path.isfile(result_txt))
        self.assertTrue(os.path.isfile(result_csv))

        with open(result_txt) as f:
            content = f.read()
        self.assertIn("ANALYTICAL-SOLUTION", content)

        with open(result_csv) as f:
            csv_content = f.read().strip().splitlines()
        self.assertEqual(2, len(csv_content))  # header + one data row

        mock_render.assert_called_once()

    @patch.object(Digraph, "render")
    def test_run_with_parameter_override(self, mock_render):
        """
        Verify that run() honours the parameters dict, overriding the loaded configuration
        (e.g. changing the arrival rate).
        :return: None
        """
        parameters = {"arrival": {"TASK_1": {"parameters": {"r": 3.0}}}}

        analytical_solution.run(self.config_path, self.outdir, parameters)

        result_csv = os.path.join(self.outdir, "result.csv")
        self.assertTrue(os.path.isfile(result_csv))

        with open(result_csv) as f:
            csv_content = f.read()
        self.assertIn("3.0", csv_content)


if __name__ == "__main__":
    unittest.main()
