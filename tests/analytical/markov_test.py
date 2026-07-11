import unittest
from unittest.mock import patch

from graphviz import Digraph

from pydes.core.analytical.markov import MarkovChain, MarkovLink, MarkovState


class MarkovStateTest(unittest.TestCase):
    def test_pretty_str_string_value(self):
        state = MarkovState("A")
        self.assertEqual("A", state.pretty_str())

    def test_pretty_str_tuple_value(self):
        state = MarkovState((0, 1))
        self.assertEqual("A0B1", state.pretty_str())

    def test_pretty_str_tuple_value_multiple_digits(self):
        state = MarkovState((2, 10))
        self.assertEqual("A2B10", state.pretty_str())

    def test_str(self):
        state = MarkovState((0, 1))
        self.assertEqual("(0, 1)", str(state))

    def test_repr(self):
        state = MarkovState((0, 1))
        self.assertEqual(str(state), repr(state))

    def test_eq_same_value(self):
        self.assertEqual(MarkovState((0, 1)), MarkovState((0, 1)))

    def test_eq_different_value(self):
        self.assertNotEqual(MarkovState((0, 1)), MarkovState((1, 0)))

    def test_eq_not_a_markov_state(self):
        self.assertFalse(MarkovState((0, 1)) == "(0, 1)")

    def test_hash_equal_for_equal_states(self):
        self.assertEqual(hash(MarkovState((0, 1))), hash(MarkovState((0, 1))))

    def test_lt(self):
        self.assertTrue(MarkovState((0, 0)) < MarkovState((0, 1)))
        self.assertFalse(MarkovState((0, 1)) < MarkovState((0, 0)))

    def test_lt_not_a_markov_state(self):
        self.assertFalse(MarkovState((0, 0)) < "(0, 1)")

    def test_getitem(self):
        state = MarkovState((3, 7))
        self.assertEqual(3, state[0])
        self.assertEqual(7, state[1])

    def test_states_are_sortable(self):
        states = [MarkovState((1, 0)), MarkovState((0, 1)), MarkovState((0, 0))]
        self.assertEqual(
            [MarkovState((0, 0)), MarkovState((0, 1)), MarkovState((1, 0))],
            sorted(states),
        )


class MarkovLinkTest(unittest.TestCase):
    def setUp(self):
        self.sA = MarkovState("A")
        self.sB = MarkovState("B")

    def test_str(self):
        link = MarkovLink(self.sA, self.sB, "p")
        self.assertEqual("(A-{p}->B)", str(link))

    def test_repr(self):
        link = MarkovLink(self.sA, self.sB, "p")
        self.assertEqual(str(link), repr(link))

    def test_eq_same_fields(self):
        self.assertEqual(MarkovLink(self.sA, self.sB, "p"), MarkovLink(self.sA, self.sB, "p"))

    def test_eq_different_value(self):
        self.assertNotEqual(MarkovLink(self.sA, self.sB, "p"), MarkovLink(self.sA, self.sB, "q"))

    def test_eq_different_head(self):
        self.assertNotEqual(MarkovLink(self.sA, self.sB, "p"), MarkovLink(self.sA, self.sA, "p"))

    def test_eq_not_a_markov_link(self):
        self.assertFalse(MarkovLink(self.sA, self.sB, "p") == "(A-{p}->B)")

    def test_hash_equal_for_equal_links(self):
        self.assertEqual(
            hash(MarkovLink(self.sA, self.sB, "p")),
            hash(MarkovLink(self.sA, self.sB, "p")),
        )

    def test_lt_different_tail(self):
        self.assertTrue(MarkovLink(self.sA, self.sB, "p") < MarkovLink(self.sB, self.sA, "q"))

    def test_lt_same_tail_different_head(self):
        self.assertTrue(MarkovLink(self.sA, self.sA, "p") < MarkovLink(self.sA, self.sB, "q"))

    def test_lt_not_a_markov_link(self):
        self.assertFalse(MarkovLink(self.sA, self.sB, "p") < "(A-{p}->B)")


class MarkovChainTest(unittest.TestCase):
    def setUp(self):
        """
        Build a simple 2-state Markov Chain with a known analytical solution:
        A <-> B, with P(A->B) = a and P(B->A) = b.
        Stationary distribution: pA = b / (a + b), pB = a / (a + b).
        """
        self.a = 0.3
        self.b = 0.2

        self.markov_chain = MarkovChain()
        self.sA = self.markov_chain.add_state("A")
        self.sB = self.markov_chain.add_state(MarkovState("B"))
        self.markov_chain.add_symbols(a=self.a, b=self.b)

        self.markov_chain.add_link(MarkovLink(self.sA, self.sA, "1-a"))
        self.markov_chain.add_link(MarkovLink(self.sA, self.sB, "a"))
        self.markov_chain.add_link(MarkovLink(self.sB, self.sB, "1-b"))
        self.markov_chain.add_link(MarkovLink(self.sB, self.sA, "b"))

    def test_add_state_new_value(self):
        markov_chain = MarkovChain()
        state = markov_chain.add_state("X")
        self.assertIsInstance(state, MarkovState)
        self.assertIn(state, markov_chain.states)

    def test_add_state_existing_markov_state(self):
        markov_chain = MarkovChain()
        existing = MarkovState("X")
        state = markov_chain.add_state(existing)
        self.assertIs(existing, state)

    def test_add_link_new(self):
        markov_chain = MarkovChain()
        sX = markov_chain.add_state("X")
        sY = markov_chain.add_state("Y")
        added = markov_chain.add_link(MarkovLink(sX, sY, "p"))
        self.assertTrue(added)
        self.assertEqual(1, len(markov_chain.links))

    def test_add_link_duplicate(self):
        markov_chain = MarkovChain()
        sX = markov_chain.add_state("X")
        sY = markov_chain.add_state("Y")
        markov_chain.add_link(MarkovLink(sX, sY, "p"))
        added_again = markov_chain.add_link(MarkovLink(sX, sY, "p"))
        self.assertFalse(added_again)
        self.assertEqual(1, len(markov_chain.links))

    def test_add_symbols(self):
        markov_chain = MarkovChain()
        markov_chain.add_symbols(x=1, y=2)
        self.assertEqual({"x": 1, "y": 2}, markov_chain.symbols)
        markov_chain.add_symbols(z=3)
        self.assertEqual({"x": 1, "y": 2, "z": 3}, markov_chain.symbols)

    def test_in_links(self):
        links = self.markov_chain.in_links(self.sA)
        self.assertEqual(2, len(links))
        self.assertTrue(all(link.head == self.sA for link in links))

    def test_out_links(self):
        links = self.markov_chain.out_links(self.sA)
        self.assertEqual(2, len(links))
        self.assertTrue(all(link.tail == self.sA for link in links))

    def test_find_link_existing(self):
        link = self.markov_chain.find_link(self.sA, self.sB)
        self.assertIsNotNone(link)
        self.assertEqual(self.sA, link.tail)
        self.assertEqual(self.sB, link.head)
        self.assertEqual("a", link.value)

    def test_find_link_missing(self):
        markov_chain = MarkovChain()
        sX = markov_chain.add_state("X")
        sY = markov_chain.add_state("Y")
        self.assertIsNone(markov_chain.find_link(sX, sY))

    def test_get_states(self):
        self.assertEqual([self.sA, self.sB], self.markov_chain.get_states())

    def test_transition_matrix_not_evaluated(self):
        tmatrix = self.markov_chain.transition_matrix()
        self.assertEqual("(1-a)/(1-a+a)", tmatrix[0][0])
        self.assertEqual("(a)/(1-a+a)", tmatrix[0][1])
        self.assertEqual("(b)/(b+1-b)", tmatrix[1][0])
        self.assertEqual("(1-b)/(b+1-b)", tmatrix[1][1])

    def test_transition_matrix_evaluated(self):
        tmatrix = self.markov_chain.transition_matrix(evaluate=True)
        self.assertAlmostEqual(1.0 - self.a, tmatrix[0][0])
        self.assertAlmostEqual(self.a, tmatrix[0][1])
        self.assertAlmostEqual(self.b, tmatrix[1][0])
        self.assertAlmostEqual(1.0 - self.b, tmatrix[1][1])

    def test_transition_matrix_evaluated_with_missing_link(self):
        markov_chain = MarkovChain()
        sX = markov_chain.add_state("X")
        sY = markov_chain.add_state("Y")
        markov_chain.add_symbols(x=0.4, y=0.6)
        markov_chain.add_link(MarkovLink(sX, sY, "x"))
        markov_chain.add_link(MarkovLink(sY, sX, "y"))

        tmatrix = markov_chain.transition_matrix(evaluate=True)

        # No self-loops: the diagonal stays the untouched float 0.0.
        self.assertEqual(0.0, tmatrix[0][0])
        self.assertEqual(0.0, tmatrix[1][1])
        self.assertAlmostEqual(1.0, tmatrix[0][1])
        self.assertAlmostEqual(1.0, tmatrix[1][0])

    def test_solve(self):
        solutions = self.markov_chain.solve()
        expected_pA = self.b / (self.a + self.b)
        expected_pB = self.a / (self.a + self.b)
        self.assertAlmostEqual(expected_pA, float(solutions["A"]))
        self.assertAlmostEqual(expected_pB, float(solutions["B"]))
        self.assertAlmostEqual(1.0, float(solutions["A"]) + float(solutions["B"]))

    def test_generate_equations(self):
        equations = self.markov_chain.generate_equations()
        self.assertEqual(2, len(equations))
        for lhs, rhs in equations:
            self.assertEqual(2, len(lhs))
            self.assertEqual(2, len(rhs))

    def test_generate_sympy_equations(self):
        equations, variables = self.markov_chain.generate_sympy_equations()
        # One flow-balance equation per state, plus the normalization equation.
        self.assertEqual(3, len(equations))
        self.assertEqual({"A", "B"}, {v.name for v in variables})

    def test_matrixs(self):
        s = self.markov_chain.matrixs()
        self.assertEqual(2, s.count("\n"))
        for row in s.strip().split("\n"):
            self.assertEqual(1, row.count(","))

    def test_str(self):
        s = str(self.markov_chain)
        self.assertIn("States:", s)
        self.assertIn("Links:", s)
        self.assertIn("Symbols:", s)

    def test_repr(self):
        self.assertEqual(str(self.markov_chain), repr(self.markov_chain))

    @patch.object(Digraph, "render")
    def test_render_graph(self, mock_render):
        s_0_0 = MarkovState((0, 0))
        s_0_1 = MarkovState((0, 1))
        s_1_0 = MarkovState((1, 0))

        markov_chain = MarkovChain()
        markov_chain.add_state(s_0_0)
        markov_chain.add_state(s_0_1)
        markov_chain.add_state(s_1_0)
        markov_chain.add_symbols(p=0.9, q=0.8, r=0.5)
        markov_chain.add_link(MarkovLink(s_0_0, s_0_0, "p"))
        markov_chain.add_link(MarkovLink(s_0_0, s_0_1, "(1-p)*0.75"))
        markov_chain.add_link(MarkovLink(s_0_1, s_1_0, "(1-q)*0.25"))

        markov_chain.render_graph("SomeFileName")

        mock_render.assert_called_once_with(filename="SomeFileName", format="svg")

    @patch.object(Digraph, "render")
    def test_render_graph_default_filename(self, mock_render):
        markov_chain = MarkovChain()
        markov_chain.add_state(MarkovState((0, 0)))

        markov_chain.render_graph()

        mock_render.assert_called_once_with(filename="MarkovChain", format="svg")


class MarkovChainBullBearStagnantTest(unittest.TestCase):
    """
    Adapted from the demo in markov.py's __main__ block: a 3-state Markov
    Chain modeling a Bull/Bear/Stagnant market.
    """

    def setUp(self):
        self.markov_chain = MarkovChain()

        self.s_0_0 = MarkovState((0, 0))  # Bull Market
        self.s_0_1 = MarkovState((0, 1))  # Bear Market
        self.s_1_0 = MarkovState((1, 0))  # Stagnant Market

        self.markov_chain.add_state(self.s_0_0)
        self.markov_chain.add_state(self.s_0_1)
        self.markov_chain.add_state(self.s_1_0)

        self.markov_chain.add_symbols(p=0.9, q=0.8, r=0.5)

        self.markov_chain.add_link(MarkovLink(self.s_0_0, self.s_0_0, "p"))
        self.markov_chain.add_link(MarkovLink(self.s_0_0, self.s_0_1, "(1-p)*0.75"))
        self.markov_chain.add_link(MarkovLink(self.s_0_0, self.s_1_0, "(1-p)*0.25"))

        self.markov_chain.add_link(MarkovLink(self.s_0_1, self.s_0_1, "q"))
        self.markov_chain.add_link(MarkovLink(self.s_0_1, self.s_0_0, "(1-q)*0.75"))
        self.markov_chain.add_link(MarkovLink(self.s_0_1, self.s_1_0, "(1-q)*0.25"))

        self.markov_chain.add_link(MarkovLink(self.s_1_0, self.s_1_0, "r"))
        self.markov_chain.add_link(MarkovLink(self.s_1_0, self.s_0_0, "(1-r)*0.5"))
        self.markov_chain.add_link(MarkovLink(self.s_1_0, self.s_0_1, "(1-r)*0.5"))

    def test_get_states(self):
        self.assertEqual(
            [self.s_0_0, self.s_0_1, self.s_1_0],
            self.markov_chain.get_states(),
        )

    def test_solve_sums_to_one(self):
        solutions = self.markov_chain.solve()
        self.assertEqual(3, len(solutions))
        total = sum(float(v) for v in solutions.values())
        self.assertAlmostEqual(1.0, total)
        for v in solutions.values():
            self.assertGreater(float(v), 0.0)

    def test_pretty_str(self):
        self.assertEqual("A0B0", self.s_0_0.pretty_str())
        self.assertEqual("A0B1", self.s_0_1.pretty_str())
        self.assertEqual("A1B0", self.s_1_0.pretty_str())


if __name__ == "__main__":
    unittest.main()
