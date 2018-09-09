class MarkovState:
    def __init__(self, value):
        self.value = value

    def pretty_str(self):
        str = ""
        sym = 'A'
        idx = 0
        for i in self.value:
            str += "{}{}".format(chr(ord(sym)+idx), i)
        return str

    def __str__(self):
        return "{}".format(self.value)

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

    def find_link(self, state1, state2):
        return next((l for l in self.out_links(state1) if l.head == state2 ), None)

    def get_states(self):
        return sorted([s for s in self.states], key=lambda state: state.value)

    def transition_matrix(self):
        states = self.get_states()
        tmatrix = []
        for state1 in states:
            row = []
            for state2 in states:
                link = self.find_link(state1, state2)
                link_value = 0.0 if link is None else link.value
                row.append(link_value)
            tmatrix.append(row)
        return tmatrix, states

    def __str__(self):
        return "States: {}\nLinks: {}\n".format(self.states, self.links)

    def __repr__(self):
        return self.__str__()
