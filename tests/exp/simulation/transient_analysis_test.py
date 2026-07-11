import os
import tempfile
import unittest

from pydes.exp.simulation import transient_analysis

CONFIG_YAML = """
general:
  mode: "TRANSIENT_ANALYSIS"
  replications: 1
  t_stop: 20
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


class TransientAnalysisRunTest(unittest.TestCase):
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

    def test_run_single_replication(self):
        """
        Verify that run() executes a single, tiny (short stop time) replication and stores the
        sampling output under a seed-specific subdirectory.
        :return: None
        """
        transient_analysis.run(self.config_path, self.outdir, {})

        outdir_replica = os.path.join(self.outdir, "seed_123456789")
        sampling_file = os.path.join(outdir_replica, "result.sampling.csv")

        self.assertTrue(os.path.isfile(sampling_file))

    def test_run_multiple_replications(self):
        """
        Verify that run() executes multiple replications, each seeded by the ending seed of the
        previous one, generating one output subdirectory per replication.
        :return: None
        """
        parameters = {"general": {"replications": 2}}

        transient_analysis.run(self.config_path, self.outdir, parameters)

        subdirs = [
            entry
            for entry in os.listdir(self.outdir)
            if os.path.isdir(os.path.join(self.outdir, entry)) and entry.startswith("seed_")
        ]
        self.assertEqual(2, len(subdirs))


if __name__ == "__main__":
    unittest.main()
