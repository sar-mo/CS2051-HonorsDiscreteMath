# test_logic.py
# CS 2051 Spring 2023 - HW2 Supplement : Logic Playground
# Instructor: Gerandy Brito
# author: Sarthak Mohanty

import logic_solutions as sol
from logic import *

import unittest

class TestLogic(unittest.TestCase):
    def setUp(self):

        # Basic Propositions
        prop1 = 'True'
        prop2 = 'False'
        prop3 = '(z)'
        prop4 = 'p and q'
        prop5 = '(not p) or q'

        # Complex Propositions
        prop6 = 'p and q and (r or (not s))'
        prop7 = '((p) and q) or (not t)'
        prop8 = '(((((p and q) or (not r)) and s) and t) or u) and ((not v) and (w and x))'
        prop9 = 'p and q and r and s and t and u and v and w and x and y and z'

        # De Morgan's Laws
        prop10 = '(not s) or (not v)'
        prop11 = '(not p) and (not q)'
        prop12 = 'not (v and s)'
        prop13 = 'not (p or q)'

        # Distributive Laws
        prop14 = '(p and q) or (p and r)'
        prop15 = '(p or q) and (p or r)'
        prop16 = 'p or (q and r)'
        prop17 = 'p and (q or r)'

        # Implications
        prop18 = 'p |implies| q'
        prop19 = 'p |implies| (q and r)'
        prop20 = '(p |implies| q) and (p |implies| r)'
        prop21 = '(p |implies| r) and (q |implies| r)'

        # Equivalences
        prop22 = 'p |iff| q'
        prop23 = 'False |iff| True'
        prop24 = '(p |iff| q) |iff| ((not p) |iff| (not q))'
        prop25 = '(p and q) |iff| (not (p |implies| (not q)))'

        # extra
        prop26 = 'p and (s or False)'
        prop27 = 'True and p'
        prop28 = '(False) or q'
        prop29 = '(not v) and (True)'
        # takes long time for test_model_fitting
        prop30 = 'p or q or r or s or t or u or v or w or x or y or z'

        self.props = [prop1, prop2, prop3, prop4, prop5,
                        prop6, prop7, prop8, prop9, prop10,
                        prop11, prop12, prop13, prop14, prop15,
                        prop16, prop17, prop18, prop19, prop20,
                        prop21, prop22, prop23, prop24, prop25,
                        prop26, prop27, prop28, prop29, prop30]
        self.longMessage = False
        
    def test_count_satisfying(self):
        for prop in self.props:
            self.assertEqual(count_satisfying(prop), sol.count_satisfying(prop), msg='count_satisfying failed')
 
    def test_are_equivalent(self):
        pairs = [(prop1, prop2) for i, prop1 in enumerate(self.props) for prop2 in self.props[i + 1:]]
        for prop1, prop2 in pairs:
            self.assertEqual(are_equivalent(prop1, prop2), sol.are_equivalent(prop1, prop2), msg='are_equivalent failed')

    def test_is_tautology(self):
        for prop in self.props:
            self.assertEqual(is_tautology(prop), sol.is_tautology(prop), msg='improper tautology evaluation')
        
    def test_is_contradiction(self):
        for prop in self.props:
            self.assertEqual(is_contradiction(prop), sol.is_contradiction(prop), msg='improper contradiction evaluation')
    
    def test_is_contingency(self):
        for prop in self.props:
            self.assertEqual(is_contingency(prop), sol.is_contingency(prop), msg='improper contingency evaluation')

    def test_model_fitting(self):
        for prop in self.props:
            self.assertEqual(truth_table(model_fitting(truth_table(prop))), truth_table(prop))
