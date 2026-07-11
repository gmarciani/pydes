import unittest

from pydes.core.analytical.markov import MarkovState
from pydes.core.analytical.markov_chains import (
    MarkovChainAlgorithm1,
    MarkovChainAlgorithm2,
)


class MarkovChainAlgorithm1Test(unittest.TestCase):
    def setUp(self):
        self.N = 2
        self.l1 = 6.0
        self.l2 = 6.25
        self.m1 = 0.45
        self.m2 = 0.25
        self.markov_chain = MarkovChainAlgorithm1(self.N, self.l1, self.l2, self.m1, self.m2)

    def test_symbols(self):
        self.assertEqual(
            dict(l1=self.l1, l2=self.l2, l=self.l1 + self.l2, m1=self.m1, m2=self.m2),
            self.markov_chain.symbols,
        )

    def test_states(self):
        expected_states = {
            MarkovState((0, 0)),
            MarkovState((1, 0)),
            MarkovState((0, 1)),
            MarkovState((2, 0)),
            MarkovState((1, 1)),
            MarkovState((0, 2)),
        }
        self.assertEqual(expected_states, self.markov_chain.states)

    def test_initial_state_has_expected_out_links(self):
        state_0_0 = MarkovState((0, 0))
        out_links = self.markov_chain.out_links(state_0_0)
        self.assertEqual(2, len(out_links))
        values = sorted(link.value for link in out_links)
        self.assertEqual(["l1", "l2"], values)

    def test_full_state_has_cloud_self_loop(self):
        # n1 + n2 == N: tasks are submitted to the Cloud (self-loop with value "l").
        full_state = MarkovState((self.N, 0))
        link = self.markov_chain.find_link(full_state, full_state)
        self.assertIsNotNone(link)
        self.assertEqual("l", link.value)

    def test_service_links_reduce_state(self):
        state_1_1 = MarkovState((1, 1))
        link_1 = self.markov_chain.find_link(state_1_1, MarkovState((0, 1)))
        self.assertIsNotNone(link_1)
        self.assertEqual("1*m1", link_1.value)

        link_2 = self.markov_chain.find_link(state_1_1, MarkovState((1, 0)))
        self.assertIsNotNone(link_2)
        self.assertEqual("1*m2", link_2.value)

    def test_invalid_state_raises(self):
        with self.assertRaises(ValueError):
            self.markov_chain._MarkovChainAlgorithm1__explore_state(
                MarkovState((self.N + 1, 0)), self.N, self.l1, self.l2, self.m1, self.m2
            )

    def test_solve_sums_to_one(self):
        solutions = self.markov_chain.solve()
        self.assertEqual(len(self.markov_chain.states), len(solutions))
        total = sum(float(v) for v in solutions.values())
        self.assertAlmostEqual(1.0, total)
        for v in solutions.values():
            self.assertGreaterEqual(float(v), 0.0)


class MarkovChainAlgorithm2Test(unittest.TestCase):
    def setUp(self):
        self.N = 2
        self.S = 1
        self.l1 = 6.0
        self.l2 = 6.25
        self.m1 = 0.45
        self.m2 = 0.25
        self.markov_chain = MarkovChainAlgorithm2(self.N, self.S, self.l1, self.l2, self.m1, self.m2)

    def test_symbols(self):
        self.assertEqual(
            dict(l1=self.l1, l2=self.l2, l=self.l1 + self.l2, m1=self.m1, m2=self.m2),
            self.markov_chain.symbols,
        )

    def test_states(self):
        expected_states = {
            MarkovState((0, 0)),
            MarkovState((0, 1)),
            MarkovState((1, 0)),
            MarkovState((2, 0)),
        }
        self.assertEqual(expected_states, self.markov_chain.states)

    def test_full_cloudlet_state_submits_to_cloud(self):
        # n1 == N: tasks are submitted to the Cloud (self-loop with value "l").
        full_state = MarkovState((self.N, 0))
        link = self.markov_chain.find_link(full_state, full_state)
        self.assertIsNotNone(link)
        self.assertEqual("l", link.value)

    def test_interruption_state(self):
        # n1 + n2 >= S and n2 > 0: arrival of task 1 interrupts task 2.
        state_0_1 = MarkovState((0, 1))
        link = self.markov_chain.find_link(state_0_1, MarkovState((1, 0)))
        self.assertIsNotNone(link)
        self.assertEqual("l1", link.value)

        self_loop = self.markov_chain.find_link(state_0_1, state_0_1)
        self.assertIsNotNone(self_loop)
        self.assertEqual("l2", self_loop.value)

    def test_solve_sums_to_one(self):
        solutions = self.markov_chain.solve()
        self.assertEqual(len(self.markov_chain.states), len(solutions))
        total = sum(float(v) for v in solutions.values())
        self.assertAlmostEqual(1.0, total)
        for v in solutions.values():
            self.assertGreaterEqual(float(v), 0.0)


if __name__ == "__main__":
    unittest.main()
