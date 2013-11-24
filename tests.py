import unittest

from app import construct_grammar
from structures import ContextFreeGrammar, StateType


class StructureTest(unittest.TestCase):

    def test_construct_pda(self):
        cfg = ContextFreeGrammar()
        cfg.add_rule('S', 'aR')
        cfg.add_rule('R', 'aRb')
        cfg.add_rule('R', '!')

        pda = cfg.construct_pda()

        start_transitions = {'!': [(StateType.Loop, ['S', '$'], None)]}
        loop_transitions = {'!': [(StateType.Loop, ['a', 'R'], 'S'),
                                  (StateType.Loop, ['a', 'R', 'b'], 'R'),
                                  (StateType.Loop, None, 'R'),
                                  (StateType.Accept, None, '$')],
                            'a': [(StateType.Loop, None, 'a')],
                            'b': [(StateType.Loop, None, 'b')]
                            }
        assert_transitions = {StateType.Start: start_transitions,
                              StateType.Loop: loop_transitions}

        self.assertEqual(assert_transitions, pda.transitions)
        print 'Testing complete!'


class AppTest(unittest.TestCase):
    pass


if __name__ == '__main__':
    unittest.main()