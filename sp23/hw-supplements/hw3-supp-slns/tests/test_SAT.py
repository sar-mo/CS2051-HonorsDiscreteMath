# CS 2051 Spring 2023 - HW3 Supplement Part 2 Test Cases
# creator - Sarthak Mohanty
# collaborators - N/A

import unittest
from unittest import mock

from logic_helper import evaluate
import SAT

import json

class TestSAT(unittest.TestCase):

    def setUp(self) -> None:
        # a list of 50 sample fourCOLOR problems, with the i-th elememt corresponding to a problem with i points
        self.fourCOLOR_problems = json.load(open('tests/fourCOLOR_sample_problems.json', 'r'))

    def test_walkSAT(self):
        # test to make sure that the pySAT method is not being called using mock
        with mock.patch('SAT.pySAT_solver') as mock_pySAT_solver:
            i = 5
            proposition = self.fourCOLOR_problems[i]['SAT_problem']
            model = SAT.walkSAT_solver(proposition, 0.5, 10000)
            self.assertNotEqual(model, None, msg="The solver does not work at all.")
            self.assertFalse(mock_pySAT_solver.called, msg="No cheating! You can't use the pySAT_solver method for the walkSAT_solver method.")

        # test best performance when p = 0.5
        for i in range(40, 50):
            proposition = self.fourCOLOR_problems[i]['SAT_problem']
            model = SAT.walkSAT_solver(proposition, 0.5, 10000)
            self.assertNotEqual(model, None, msg="The solver does not perform good enough when p = 0.5, cannot solve four coloring problem for 40-50 regions.")
            self.assertTrue(evaluate(proposition, model))

        # test probability 1
        for i in range(15, 30):
            proposition = self.fourCOLOR_problems[i]['SAT_problem']
            model = SAT.walkSAT_solver(proposition, 1, 10000)
            if model is not None:
                break
        self.assertNotEqual(model, None, msg="The solver does not generate a model when p = 1.")
        self.assertTrue(evaluate(proposition, model))