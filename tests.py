import unittest

from grammar import ContextFreeGrammar, State


class CFGTest(unittest.TestCase):

    def test_construct_pda(self):
        cfg = ContextFreeGrammar()
        cfg.add_rule('S', 'aR')
        cfg.add_rule('R', 'aRb')
        cfg.add_rule('R', '!')

        pda = cfg.construct_pda()

        start_transitions = {'!': [(State.Loop, ['S', '$'], None)]}
        loop_transitions = {
            '!': [(State.Loop, ['a', 'R'], 'S'),
                  (State.Loop, ['a', 'R', 'b'], 'R'),
                  (State.Loop, None, 'R'),
                  (State.Accept, None, '$')],
            'a': [(State.Loop, None, 'a')],
            'b': [(State.Loop, None, 'b')]
        }
        assert_transitions = {State.Start: start_transitions,
                              State.Loop: loop_transitions}

        self.assertEqual(assert_transitions, pda.transitions)

    def test_simulate(self):
        # First input file
        cfg = ContextFreeGrammar()
        cfg.add_rule('S', 'aSb')
        cfg.add_rule('S', '!')

        expr1 = 'ab'
        expr2 = 'aabb'
        expr3 = '!'
        expr4 = 'aaaabbbb'
        expr5 = 'ababa'
        expr6 = 'bbaaa'
        self.assertTrue(cfg.simulate(expr1))
        self.assertTrue(cfg.simulate(expr2))
        self.assertTrue(cfg.simulate(expr3))
        self.assertTrue(cfg.simulate(expr4))
        self.assertFalse(cfg.simulate(expr5))
        self.assertFalse(cfg.simulate(expr6))

        # Second input file
        cfg = ContextFreeGrammar()
        cfg.add_rule('S', 'a_N_tells_a_N_O')
        cfg.add_rule('N', 'boy')
        cfg.add_rule('N', 'girl')
        cfg.add_rule('O', 'a_story')
        cfg.add_rule('O', 'that_S')

        expr1 = 'a_boy_tells_a_girl_a_story'
        expr2 = 'a_boy_tells_a_girl_that_a_boy_tells_a_girl_a_story'
        expr3 = 'a_girl_tells_a_boy_a_story'
        expr4 = 'a_girl_tells_a_boy_that_a_boy_tells_a_girl_that'
        expr5 = 'a_story_tells_a_boy_a_story'
        expr6 = 'a_boy_tells_a_tells_a_boy_a_story'
        self.assertTrue(cfg.simulate(expr1))
        self.assertTrue(cfg.simulate(expr2))
        self.assertTrue(cfg.simulate(expr3))
        self.assertFalse(cfg.simulate(expr4))
        self.assertFalse(cfg.simulate(expr5))
        self.assertFalse(cfg.simulate(expr6))

        # Third input file
        cfg = ContextFreeGrammar()
        cfg.add_rule('S', 'XY')
        cfg.add_rule('X', 'AX')
        cfg.add_rule('X', '!')
        cfg.add_rule('A', 'a')
        cfg.add_rule('Y', 'BY')
        cfg.add_rule('Y', '!')
        cfg.add_rule('B', 'b')

        expr1 = 'a'
        expr2 = 'b'
        expr3 = 'aaaaaaaabbbbbbbbb'
        expr4 = '!'
        expr5 = 'bbbbbbbbbbbbbbbbbbbbbb'
        expr6 = 'ababab'
        self.assertTrue(cfg.simulate(expr1))
        self.assertTrue(cfg.simulate(expr2))
        self.assertTrue(cfg.simulate(expr3))
        self.assertTrue(cfg.simulate(expr4))
        self.assertTrue(cfg.simulate(expr5))
        self.assertFalse(cfg.simulate(expr6))

if __name__ == '__main__':
    unittest.main()