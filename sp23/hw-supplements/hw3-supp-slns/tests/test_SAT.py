# CS 2051 Spring 2023
# HW3 Supplement Helper
# author - Sarthak Mohanty
# collaborators - N/A

# these are the tests for the rules of inference solver

import unittest

# to hide the output of the print statements
from unittest import mock
from io import StringIO

import fourCOLOR_solution as sol
from logic_helper import *
import SAT

class TestSAT(unittest.TestCase):

    def test_walkSAT(self):
        with mock.patch('sys.stdout', new = StringIO()) as std_out:
            # test to make sure that the pySAT method is not being called using mock
            with mock.patch('SAT.pySAT_solver') as mock_pySAT_solver:
                i = 5
                vor = sol.drawBlankVoronoiDiagram(num_points=i)
                proposition = sol.fourColoringToSAT(sol.getNeighbors(vor))
                model = SAT.walkSAT_solver(proposition, 0.5, 10000)
                self.assertNotEqual(model, None, msg="The solver does not work at all.")
                self.assertFalse(mock_pySAT_solver.called, msg="No cheating! You can't use the pySAT_solver method for the walkSAT_solver method.")

            # test best performance when p = 0.5
            for i in range(40, 50):
                vor = sol.drawBlankVoronoiDiagram(num_points=i)
                proposition = sol.fourColoringToSAT(sol.getNeighbors(vor))
                model = SAT.walkSAT_solver(proposition, 0.5, 10000)
                self.assertNotEqual(model, None, msg="The solver does not perform good enough when p = 0.5, cannot solve four coloring problem for 40-50 regions.")
                self.assertTrue(evaluate(proposition, model))

            # test probability 1
            for i in range(15, 30):
                vor = sol.drawBlankVoronoiDiagram(num_points=i)
                proposition = sol.fourColoringToSAT(sol.getNeighbors(vor))
                model = SAT.walkSAT_solver(proposition, 1, 10000)
                if model is not None:
                    break
            self.assertNotEqual(model, None, msg="The solver does not generate a model when p = 1.")
            self.assertTrue(evaluate(proposition, model))