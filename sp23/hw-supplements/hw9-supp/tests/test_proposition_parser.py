"""Tests for the propositions_parser module."""

import unittest

from proposition_parser_solution import *

class TestPropositionParser(unittest.TestCase):
    def setUp(self) -> None:
        self.parsing_tests = [('', None, ''),
                        ('x', 'x', ''),
                        ('T', 'T', ''),
                        ('a', None, ''),
                        (')', None, ''),
                        ('x&', 'x', '&'),
                        ('p3&y', 'p3', '&y'),
                        ('F)', 'F', ')'),
                        ('~x', '~x', ''),
                        ('~', None, ''),
                        ('x2', 'x2', ''),
                        ('x|y', 'x', '|y'),
                        ('(p|x13)', '(p|x13)', ''),
                        ('((p|x13))', None, ''),
                        ('x13->x14', 'x13', '->x14'),
                        ('(x13->x14)', '(x13->x14)', ''),
                        ('(x&y',None,''),
                        ('(T)',None,''),
                        ('(x&&y)', None, ''),
                        ('-|x',None,''),
                        ('-->',None,''),
                        ('(q~p)',None,''),
                        ('(~F)', None, ''),
                        ('(r&(y|(z->w)))','(r&(y|(z->w)))',''),
                        ('~~~x~~','~~~x','~~'),
                        ('(((~T->s45)&s45)|~y)', '(((~T->s45)&s45)|~y)' ,''),
                        ('((p->q)->(~q->~p))->T)','((p->q)->(~q->~p))','->T)'),
                        ('((p->q)->(~q->~p)->T)',None,''),
                        ('(x|y|z)', None, ''),
                        ('~((~x17->p)&~~(~F|~p))', '~((~x17->p)&~~(~F|~p))', '')]

    def test_parse(self, debug=False):
        return NotImplementedError

    def test_evaluate(debug=False):
        infix1 = '~(p&q7)'
        models_values1 = [
            ({'p': True,  'q7': False}, True),
            ({'p': False, 'q7': False}, True),
            ({'p': True,  'q7': True},  False)
        ]
        infix2 = '~~~x'
        models_values2 = [
            ({'x': True}, False),
            ({'x': False}, True)
        ]
        infix3 = '((x->y)&(~x->z))'
        models_values3 = [
            ({'x': True,  'y': False, 'z':True},  False),
            ({'x': False, 'y': False, 'z':True},  True),
            ({'x': True,  'y': True,  'z':False}, True)
        ]
        infix4 = '(T&p)'
        models_values4 = [
            ({'p': True},  True),
            ({'p': False}, False)
        ]
        infix5 = '(F|p)'
        models_values5 = [
            ({'p': True},  True),
            ({'p': False}, False)
        ]
        for infix,models_values in [[infix1, models_values1],
                                    [infix2, models_values2],
                                    [infix3, models_values3],
                                    [infix4, models_values4],
                                    [infix5, models_values5]]:
            formula = Formula.parse(infix)
            for model,value in models_values:
                if debug:
                    print('Testing evaluation of formula', formula, 'in model',
                        model)
                assert evaluate(formula, model) == value # model can be optionally frozendict