import os
import unittest

from pydes.core.simulation.result_printer import build_latex_table, get_index_symbol
from tests import RES_DIR

ANALYTICAL_RESULT_PATH = os.path.join(RES_DIR, "analytical_result.csv")
SIMULATION_RESULT_PATH = os.path.join(RES_DIR, "simulation_result.csv")


class GetIndexSymbolTest(unittest.TestCase):
    def test_population_global(self):
        self.assertEqual(get_index_symbol("population", "system", "global"), "N_{sys}")

    def test_response_task_1(self):
        self.assertEqual(get_index_symbol("response", "cloudlet", "task_1"), "T_{clt,1}")

    def test_throughput_task_2(self):
        self.assertEqual(get_index_symbol("throughput", "cloud", "task_2"), "X_{cld,2}")


class BuildLatexTableTest(unittest.TestCase):
    def test_build_latex_table_from_real_result_files(self):
        """
        Build the LaTeX table out of a real analytical/simulation result pair (the same fixtures
        used by the pydes.exp.simulation.validation demo experiment).
        :return: None
        """
        table = build_latex_table(ANALYTICAL_RESULT_PATH, SIMULATION_RESULT_PATH)

        self.assertIsInstance(table, str)
        self.assertIn("Measure & Theoretical & Experimental", table)
        # One line per (system_scope, index, task_scope) combination: 3 systems * 3 indices * 3 tasks.
        self.assertEqual(table.count("\\pm"), 3 * 3 * 3)
        # One trailing \hline per system scope, plus the two \hline in the table header.
        self.assertEqual(table.count("\\hline"), 3 + 2)
        # Sanity check on the population/system/global entry.
        self.assertIn("$N_{sys}$", table)


if __name__ == "__main__":
    unittest.main()
