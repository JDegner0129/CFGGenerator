class PushdownAutomaton(object):

    def __init__(self):
        self._stack = []
        self._start_state = None
        self._final_states = set()
        self._transitions = {}

    @property
    def start_state(self):
        return self._start_state

    @start_state.setter
    def start_state(self, value):
        self._start_state = value

    def add_final_state(self, state):
        self._final_states.add(state)

    def add_transition(self, symbol, source, dest, push=None, pop=None):
        if input not in self._transitions:
            self._transitions[source] = {symbol: [(dest, push, pop)]}
        else:
            if symbol not in self._transitions:
                self._transitions[source][symbol] = [(dest, push, pop)]
            else:
                self._transitions[source][symbol].append((dest, push, pop))

    def pop_symbol(self):
        return self._stack.pop()

    def push_symbol(self, symbol):
        self._stack.append(symbol)

    def simulate(self, word):
        pass


class ContextFreeGrammar(object):

    def __init__(self):
        self._rules = {}
        self._start_rule = None

    @property
    def start_rule(self):
        return self._start

    @start_rule.setter
    def start_rule(self, value):
        self._start_rule = value

    def add_rule(self, symbol, rule):
        if symbol not in self._rules:
            self._rules[symbol] = [rule]
        else:
            self._rules[symbol].append(rule)

    def construct_pda(self):
        pass

    def simulate(self, str):
        pda = self.construct_pda()
        return pda.simulate(str)