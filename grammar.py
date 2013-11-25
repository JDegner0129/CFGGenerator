from sys import stdin


class State:
    """
    An enumeration of the possible states of the constructed PDA.
    """
    Start, Loop, Accept = range(3)


class PushdownAutomaton(object):
    """
    A class to store information concerning a pushdown automaton.
    """

    def __init__(self):
        self._transitions = {}
        self._steps = 100

    @property
    def transitions(self):
        """
        The transition function for this automaton.
        """
        return self._transitions

    def add_transition(self, symbol, source, dest, push=None, pop=None):
        """
        Adds a transition to the transition function.
        """
        if source not in self._transitions:
            self._transitions[source] = {symbol: [(dest, push, pop)]}
        else:
            if symbol not in self._transitions[source]:
                self._transitions[source][symbol] = [(dest, push, pop)]
            else:
                self._transitions[source][symbol].append((dest, push, pop))

    def simulate(self, symbols, stack=[], state=State.Start):
        """
        Simulates this automaton on the given symbols, starting at the given state.
        """

        if state == State.Start:  # if we're on the start state, reset the steps we have left
            self._steps = 100
        while self._steps > 0:
            self._steps -= 1
            next_char = '!'
            if symbols:
                next_char = symbols[0]

            # if the current state has no transitions, or there are no empty transitions or
            # transitions for the current character, we're done
            if state not in self._transitions or \
                    (next_char not in self._transitions[state] and '!' not in self._transitions[state]):
                return False

            else:
                # iterate over acceptable transitions (next character and empty)
                for sym in filter(lambda y: y in [next_char, '!'], self._transitions[state]):

                    # for each transition in the transition function for this character, attempt to
                    # simulate on the new transition
                    for new_state, push_chars, pop_char in self._transitions[state][sym]:
                        if not pop_char or pop_char == stack[-1]:
                            stack_copy = [x for x in stack]

                            # if we're not processing any characters, don't remove the first symbol
                            new_symbols = symbols if (sym == '!' and next_char != '!') else symbols[1:]

                            # if we hit the accept state with no characters,
                            # or the new simulation succeeds, we accept
                            if (new_state == State.Accept and len(new_symbols) == 0) or \
                                    self._take_transition(new_symbols, new_state, stack_copy, push_chars, pop_char):
                                return True

                return False
        return False

    def _take_transition(self, symbols, state, stack, push_chars, pop_char):
        """
        Updates the stack and state and begins a new simulation on this PDA.
        """
        if pop_char:
            stack.pop()
        if push_chars:
            stack += push_chars[::-1]
        return self.simulate(symbols, stack, state)


class ContextFreeGrammar(object):
    """
    A class to store information concerning a context-free grammar.
    """

    def __init__(self):
        self._rules = []

    def add_rule(self, symbol, rule):
        """
        Adds a new rule to the context-free grammar.
        """
        self._rules.append((symbol, rule))

    def construct_pda(self):
        """
        Constructs an equivalent PDA for this context-free grammar.
        """
        pda = PushdownAutomaton()

        # add an initial transition from the start state
        pda.add_transition('!',
                           State.Start,
                           State.Loop,
                           push=[self._rules[0][0], '$'])

        # iterate over all rules and add appropriate transitions
        terminals = []
        for symbol, rule in self._rules:
            push_syms = []
            for c in rule:
                if c != '!':
                    push_syms.append(c)

                    # if the current character is an unread terminal,
                    # add a looping transition for it
                    if (c.islower() or c == '_') and c not in terminals:
                        terminals.append(c)
                        pda.add_transition(c,
                                           State.Loop,
                                           State.Loop,
                                           pop=c)
            push_syms = push_syms or None
            pda.add_transition('!',
                               State.Loop,
                               State.Loop,
                               push=push_syms,
                               pop=symbol)

        # add a transition to the accepting state
        pda.add_transition('!',
                           State.Loop,
                           State.Accept,
                           pop='$')
        return pda

    def simulate(self, word):
        """
        Simulates the given word in this context-free grammar by constructing a PDA and
        simulating it with the word.
        """
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