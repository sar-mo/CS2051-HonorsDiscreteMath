# test_logic.py
# CS 2051 Spring 2023 - HW2 Supplement : Logic Playground
# Instructor: Gerandy Brito
# author: Sarthak Mohanty

from proposition_parser import *

from functools import partial
import unittest
from unittest import mock
import re
import random

class TestLogic(unittest.TestCase):
    def setUp(self):

        class Infix(object):
            def __init__(self, func):
                self.func = func
            def __or__(self, other):
                return self.func(other)
            def __ror__(self, other):
                return Infix(partial(self.func, other))
            def __call__(self, v1, v2):
                return self.func(v1, v2)

        @Infix
        def implies(p, q):
            return (not p) or q

        @Infix
        def iff(p, q):
            return (p |implies| q) and (q |implies| p)

        def generate_random_model(proposition: str):
            extract_variables = lambda proposition: sorted(set(re.findall(r'\b[a-z][0-9]*\b', proposition)))
            variables = extract_variables(proposition)
            model = {}
            for var in variables:
                model[var] = random.choice([True, False])
            return model
        
        def instructor_evaluate(proposition: str, model: dict):
            """Evaluates a proposition given a model.

            Parameters:
                proposition: The proposition to evaluate.
                model: A dictionary mapping variables to their assignments.

            Returns:
                The truth value of the proposition.

            Example:
                >>> evaluate("p and (q implies r)", {'p': True, 'q': False, 'r': True}
                True
            """
            model['iff'] = iff
            model['implies'] = implies
            proposition = proposition.replace('iff', '|iff|').replace('implies', '|implies|')
            return eval(proposition, model)

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
        prop18 = 'p implies q'
        prop19 = 'p implies (q and r)'
        prop20 = '(p implies q) and (p implies r)'
        prop21 = '(p implies r) and (q implies r)'

        # Equivalences
        prop22 = 'p iff q'
        prop23 = 'False iff True'
        prop24 = '(p iff q) iff ((not p) iff (not q))'
        prop25 = '(p and q) iff (not (p implies (not q)))'

        # extra
        prop26 = 'p and (s or False)'
        prop27 = 'True and p'
        prop28 = '(False) or q'
        prop29 = '(not v) and (True)'

        prop30 = 'p or q or r or s or t or u or v or w or x'

        self.props = [prop1, prop2, prop3, prop4, prop5,
                prop6, prop7, prop8, prop9, prop10,
                prop11, prop12, prop13, prop14, prop15,
                prop16, prop17, prop18, prop19, prop20,
                prop21, prop22, prop23, prop24, prop25,
                prop26, prop27, prop28, prop29, prop30]
        self.models = [generate_random_model(prop) for prop in self.props]
        self.instructor_evaluate = instructor_evaluate
        
    def test_evaluate(self):
        # make sure eval is not being called in evaluate
        with mock.patch('builtins.eval') as mock_eval:
            sample_prop = 'p and q'
            sample_model = {'p': True, 'q': False}
            evaluate(sample_prop, sample_model)  # Call your evaluate function
            self.assertFalse(mock_eval.called, msg="No cheating! You can't use the built-in eval() method.")

        for i in range(len(self.props)):
            student_evaluation = evaluate(self.props[i], self.models[i])
            instructor_evaluation = self.instructor_evaluate(self.props[i], self.models[i])
            self.assertEqual(student_evaluation, instructor_evaluation, msg=f"Proposition: {self.props[i]}\nStudent Evaluation: {student_evaluation}\nInstructor Evaluation: {instructor_evaluation}")