import sympy
from core.markov.markovchain import MarkovChain, MarkovLink


def generate_markov_chain(N, S, l1, l2, m1, m2):
    """
    Generate the matrix for the flow equations.
    :param N: (int) the number of Cloudlet servers.
    :param S: (int) the Cloudlet threshold.
    :param l1: (float) the arrival rate for tasks of type 1.
    :param l2: (float) the arrival rate for tasks of type 2.
    :param m1: (float) the service rate for tasks of type 1.
    :param m2: (float) the service rate for tasks of type 2.
    :return: the matrix.
    """
    M = MarkovChain()
    state = M.add_state((0,0))
    explore_state(M, state, N, S, l1, l2, m1, m2)
    return M


def explore_state(M, state, N, S, l1, l2, m1, m2):
    """
    Recursive state exploration.
    :param M: the Markov Chain.
    :param state: the current state.
    :param N: (int) the number of Cloudlet servers.
    :param S: (int) the Cloudlet threshold.
    :param l1: (float) the arrival rate for tasks of type 1.
    :param l2: (float) the arrival rate for tasks of type 2.
    :param m1: (float) the service rate for tasks of type 1.
    :param m2: (float) the service rate for tasks of type 2.
    :return:
    """
    n1 = state.value[0]
    n2 = state.value[1]

    if n1 + n2 <= N:

        if n1 + n2 < S:
            # arrival task 1
            state_arrival = M.add_state((n1+1,n2))
            link = MarkovLink(state, state_arrival, l1)
            added = M.add_link(link)
            if added:
                explore_state(M, state_arrival, N, S, l1, l2, m1, m2)

            # arrival task 2
            state_arrival = M.add_state((n1, n2 + 1))
            link = MarkovLink(state, state_arrival, l2)
            added = M.add_link(link)
            if added:
                explore_state(M, state_arrival, N, S, l1, l2, m1, m2)

        if n1 + n2 >= S and n2 > 0:
            # arrival task 1
            state_arrival = M.add_state((n1 + 1, n2-1))
            link = MarkovLink(state, state_arrival, l1)
            added = M.add_link(link)
            if added:
                explore_state(M, state_arrival, N, S, l1, l2, m1, m2)

    if n1 > 0:
        # service task 1
        state_served = M.add_state((n1-1,n2))
        link = MarkovLink(state, state_served, n1*m1)
        added = M.add_link(link)
        if added:
            explore_state(M, state_served, N, S, l1, l2, m1, m2)

    if n2 > 0:
        # service task 2
        state_served = M.add_state((n1,n2-1))
        link = MarkovLink(state, state_served, n2 * m2)
        added = M.add_link(link)
        if added:
            explore_state(M, state_served, N, S, l1, l2, m1, m2)


def generate_equations(MC):
    """
    Generate flow equations from the MArkov chain.
    :param MC: (MarkovChain) the Markov Chain.
    :return: the list of equations
    """
    equations = []
    for s in MC.states:
        lhs = MC.out_links(s)
        rhs = MC.in_links(s)
        equations.append((lhs,rhs))

    return equations


def generate_sympy_equations(eqns):
    """
    Generate sympy flow equations from the Markov chain.
    :param M: (MarkovChain) the Markov Chain.
    :return: the list of equations
    """
    variables = set()
    equations = []
    for eqn in eqns:
        equation = 0
        lhs = eqn[0]
        rhs = eqn[1]
        for lhs_link in lhs:
            variable = sympy.Symbol(lhs_link.tail.pretty_str())
            variables.add(variable)
            equation += variable * lhs_link.value

        for rhs_link in rhs:
            variable = sympy.Symbol(rhs_link.tail.pretty_str())
            variables.add(variable)
            equation -= variable * rhs_link.value

        equations.append(equation)

    equation = -1
    for variable in variables:
        equation += variable
    equations.append(equation)

    return equations, variables


def solve(MC):
    """
    Solves a Markov Chain.
    :param MC: the Markov Chain.
    :return: the solutions of the Markov Chain.
    """
    equations, variables = generate_sympy_equations(generate_equations(MC))
    solutions = sympy.solve(equations, variables)

    state_solutions = {}
    for symbol, value in solutions.items():
        state_solutions[symbol.name] = value

    return state_solutions


def matrixs(M):
    """
    Return the string representation of the matrix.
    :param M: the matrix.
    :return: the string representation.
    """
    s = ""
    for r in M:
        s += "{}\n".format(",".join(map(str,r)))
    return s


def compute_states_clt_1(states, clt_n_servers):
    """
    Return the subset of states S_clt_1.
    :param states: the state space.
    :param clt_n_servers: the number of servers in Cloudlet.
    :return: the subset of states S_clt_1.
    """
    states_clt_1 = []

    for state in states:
        n_clt_1 = state.value[0]
        n_clt_2 = state.value[1]

        if (n_clt_1 + n_clt_2 < clt_n_servers) or (n_clt_2 > 0):
            states_clt_1.append(state)

    return states_clt_1


def compute_states_clt_2(states, clt_n_servers, clt_threshold):
    """
    Return the subset of states S_clt_2.
    :param states: the state space.
    :param clt_n_servers: the number of servers in Cloudlet.
    :param clt_threshold: the Cloudlet threshold.
    :return: the subset of states S_clt_2.
    """
    states_clt_2 = []

    for state in states:
        n_clt_1 = state.value[0]
        n_clt_2 = state.value[1]

        if (n_clt_1 + n_clt_2 < clt_n_servers) and (n_clt_2 < clt_threshold):
            states_clt_2.append(state)

    return states_clt_2


def compute_states_clt_3(states, clt_n_servers, clt_threshold):
    """
    Return the subset of states S_clt_3.
    :param states: the state space.
    :param clt_n_servers: the number of servers in Cloudlet.
    :param clt_threshold: the Cloudlet threshold.
    :return: the subset of states S_clt_3.
    """
    states_clt_3 = []

    for state in states:
        n_clt_1 = state.value[0]
        n_clt_2 = state.value[1]

        if (n_clt_1 + n_clt_2 == clt_n_servers) and (n_clt_2 > 0):
            states_clt_3.append(state)

    return states_clt_3


if __name__ == "__main__":
    N = 3
    S = 3
    l1 = 1
    l2 = 3
    m1 = 2
    m2 = 4

    MC = generate_markov_chain(N, S, l1, l2, m1, m2)
    print(MC)
    M, S = MC.transition_matrix()
    print(matrixs(M))
    print(S)
    MC.render_graph("out")
