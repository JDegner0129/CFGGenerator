class StateType:
    Start, Loop, Accept = range(3)


class PushdownAutomaton(object):

    def __init__(self):
        self._stack = []
        self._transitions = {}

    @property
    def transitions(self):
        return self._transitions

    def add_transition(self, symbol, source, dest, push=None, pop=None):
        if source not in self._transitions:
            self._transitions[source] = {symbol: [(dest, push, pop)]}
        else:
            if symbol not in self._transitions[source]:
                self._transitions[source][symbol] = [(dest, push, pop)]
            else:
                self._transitions[source][symbol].append((dest, push, pop))

    def simulate(self, word):
        pass


class Rule(object):

    def __init__(self, symbol, rule):
        self._symbol = symbol
        self._rule = rule

    @property
    def symbol(self):
        return self._symbol

    @property
    def rule(self):
        return self._rule


class ContextFreeGrammar(object):

    def __init__(self):
        self._rules = []

    @property
    def start_rule(self):
        if len(self._rules) == 0:
            return None
        return self._rules[0]

    def add_rule(self, symbol, rule):
        self._rules.append(Rule(symbol, rule))

    def construct_pda(self):
        pda = PushdownAutomaton()
        pda.add_transition('!',
                           StateType.Start,
                           StateType.Loop,
                           push=[self._rules[0].symbol, '$'])

        terminals = []
        for r in self._rules:
            push_syms = []
            for c in r.rule:
                if c != '!':
                    push_syms.append(c)
                    if c.islower() and c not in terminals:
                        terminals.append(c)
            push_syms = push_syms or None
            pda.add_transition('!',
                               StateType.Loop,
                               StateType.Loop,
                               push=push_syms,
                               pop=r.symbol)

        for c in terminals:
            pda.add_transition(c,
                               StateType.Loop,
                               StateType.Loop,
                               pop=c)
        pda.add_transition('!',
                           StateType.Loop,
                           StateType.Accept,
                           pop='$')
        return pda

    def simulate(self, word):
        pda = self.construct_pda()
        return pda.simulate(word)