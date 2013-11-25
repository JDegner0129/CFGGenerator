from sys import stdin


class State:
    Start, Loop, Accept = range(3)


class PushdownAutomaton(object):

    def __init__(self):
        self._transitions = {}
        self._steps = 100

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

    def simulate(self, symbols, stack=[], state=State.Start):
        if state == State.Start:
            self._steps = 100
        while self._steps > 0:
            self._steps -= 1
            next_char = '!'
            if symbols:
                next_char = symbols[0]
            if state not in self._transitions or \
                    (next_char not in self._transitions[state] and '!' not in self._transitions[state]):
                return False
            else:
                if next_char in self._transitions[state]:
                    for new_state, push_chars, pop_char in self._transitions[state][next_char]:
                        if not pop_char or pop_char == stack[-1]:
                            stack_copy = [x for x in stack]
                            if (new_state == State.Accept and len(symbols) == 1) or \
                                    self._take_transition(symbols[1:], new_state, stack_copy, push_chars, pop_char):
                                return True
                if '!' in self._transitions[state]:
                    for new_state, push_chars, pop_char in self._transitions[state]['!']:
                        if not pop_char or pop_char == stack[-1]:
                            stack_copy = [x for x in stack]
                            if (new_state == State.Accept and len(symbols) == 0) or \
                                    self._take_transition(symbols, new_state, stack_copy, push_chars, pop_char):
                                return True

                return False
        return False

    def _take_transition(self, symbols, state, stack, push_chars, pop_char):
        if pop_char:
            stack.pop()
        if push_chars:
            stack += push_chars[::-1]
        return self.simulate(symbols, stack, state)


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
                           State.Start,
                           State.Loop,
                           push=[self._rules[0].symbol, '$'])

        terminals = []
        for r in self._rules:
            push_syms = []
            for c in r.rule:
                if c != '!':
                    push_syms.append(c)
                    if (c.islower() or c == '_') and \
                                    c not in terminals:
                        terminals.append(c)
            push_syms = push_syms or None
            pda.add_transition('!',
                               State.Loop,
                               State.Loop,
                               push=push_syms,
                               pop=r.symbol)

        for c in terminals:
            pda.add_transition(c,
                               State.Loop,
                               State.Loop,
                               pop=c)
        pda.add_transition('!',
                           State.Loop,
                           State.Accept,
                           pop='$')
        return pda

    def simulate(self, word):
        pda = self.construct_pda()
        return pda.simulate(word)

if __name__ == '__main__':
    num_rules = None
    rules_read = 0
    cfg = ContextFreeGrammar()
    expressions = []

    for line in stdin:
        stripped_line = line.strip()
        if not stripped_line:
            break
        if num_rules is None:
            num_rules = int(stripped_line)
        elif rules_read < num_rules:
            symbol, rule = stripped_line.split('->')
            cfg.add_rule(symbol, rule)
            rules_read += 1
        else:
            expressions.append(stripped_line)

    for expr in expressions:
        if cfg.simulate(expr):
            print 'yes'
        else:
            print 'no'