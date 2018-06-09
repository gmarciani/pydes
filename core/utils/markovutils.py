class MarkovState:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "[{}]".format(self.value)

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        if not isinstance(other, MarkovState):
            return False
        return self.value == other.value


class MarkovLink:

    def __init__(self, tail, head, value):
        self.tail = tail
        self.head = head
        self.value = value

    def __str__(self):
        return "({}-{}->{})".format(self.tail, self.value, self.head)

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        if not isinstance(other, MarkovLink):
            return False
        return self.tail == other.tail and self.head == other.head and self.value == other.value


class MarkovChain:

    def __init__(self):
        self.states = set()
        self.links = set()

    def add_state(self, value):
        state = MarkovState(value)
        self.states.add(state)
        return state

    def add_link(self, link):
        if link not in self.links:
            self.links.add(link)
            return True
        return False

    def in_links(self, state):
        return list(l for l in self.links if l.head == state)

    def out_links(self, state):
        return list(l for l in self.links if l.tail == state)

    def __str__(self):
        return "States: {}\nLinks: {}\n".format(self.states, self.links)

    def __repr__(self):
        return self.__str__()


def generate_markov_chain(N, S, l1, l2, mu1, mu2):
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


def explore_state(M, state, N, S, l1, l2, mu1, mu2):
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
        link = MarkovLink(state, state_served, n1*mu1)
        added = M.add_link(link)
        if added:
            explore_state(M, state_served, N, S, l1, l2, m1, m2)

    if n2 > 0:
        # service task 2
        state_served = M.add_state((n1,n2-1))
        link = MarkovLink(state, state_served, n2 * mu2)
        added = M.add_link(link)
        if added:
            explore_state(M, state_served, N, S, l1, l2, m1, m2)


def generate_equations(M):
    """
    Generate flow equations from the MArkov chain.
    :param M: (MarkovChain) the Markov Chain.
    :return: the list of equations
    """
    balancing = {s: (M.in_links(s), M.out_links(s)) for s in M.states}
    equations = []
    for si in M.states:
        lhs = None
        rhs = None
        equations.append((lhs,rhs))

    return equations



def matrixs(M):
    """
    Return the string representation of the matrix.
    :param M: the matrix.
    :return: the string representation.
    """
    s = ""
    for r in range(len(M)):
        s += "{}\n".format(",".join(map(str,M[r])))
    return s


if __name__ == "__main__":
    N = 2
    S = 2
    l1 = 1
    l2 = 3
    m1 = 2
    m2 = 4

    M = generate_markov_chain(N, S, l1, l2, m1, m2)
    print(M)
    #E = generate_equations(M)
    #print(matrixs(E))
