# CS 2051 Spring 2023
# HW3 Supplement Helper
# author - Sarthak Mohanty
# collaborators - N/A

# these are the tests for the SAT fourCOLOR_solver

import unittest
from fourCOLOR import *
import fourCOLOR_solution as fourCOLOR_sol
import SAT_solution as SAT_sol
from logic_helper import *
import random

class Test4COLOR(unittest.TestCase):

    def test_fourColoringToSAT(self):
        # test that my model works with their proposition:
        for i in range(2, 15):
            vor = fourCOLOR_sol.drawBlankVoronoiDiagram(num_points=i)
            student_proposition = fourColoringToSAT(fourCOLOR_sol.getNeighbors(vor))

            parsed_prop, vars = fourCOLOR_sol.parse_proposition(student_proposition)
            model = SAT_sol.pySAT_solver(parsed_prop)
            model = fourCOLOR_sol.repackaged_model(model, vars)

            self.assertTrue(evaluate(student_proposition, model), msg='generated proposition is not correct')
        
        for i in range(2, 15):
            vor = fourCOLOR_sol.drawBlankVoronoiDiagram(num_points=i)
            
            for _ in range(10):
                proposition = fourCOLOR_sol.fourColoringToSAT(fourCOLOR_sol.getNeighbors(vor))
                parsed_prop, vars = fourCOLOR_sol.parse_proposition(proposition)
                model = SAT_sol.pySAT_solver(parsed_prop)
                model = fourCOLOR_sol.repackaged_model(model, vars)
                while evaluate(proposition, model):
                    # flip random variable in model
                    var = random.choice(list(model.keys()))
                    model[var] = not model[var]

                student_proposition = fourColoringToSAT(fourCOLOR_sol.getNeighbors(vor))
                self.assertFalse(evaluate(student_proposition, model), msg='generated proposition is not correct')

        # make sure neighbors are correct
        for i in range(2, 15):
            vor = fourCOLOR_sol.drawBlankVoronoiDiagram(num_points=i)
            for _ in range(10):
                proposition = fourCOLOR_sol.fourColoringToSAT(fourCOLOR_sol.getNeighbors(vor))
                parsed_prop, vars = fourCOLOR_sol.parse_proposition(proposition)
                model = SAT_sol.pySAT_solver(parsed_prop)
                model = fourCOLOR_sol.repackaged_model(model, vars)

                # pick random variable that is true in model
                random_variable = random.choice([var for var in model if model[var]])
                color = random_variable[0]
                region = int(random_variable[1:])
                neighbors = fourCOLOR_sol.getNeighbors(vor)[region][1]
                if len(neighbors) != 0:
                    random_neighbor = random.choice(neighbors)
                    model[color + str(random_neighbor)] = True
                    student_proposition = fourColoringToSAT(fourCOLOR_sol.getNeighbors(vor))
                    self.assertFalse(evaluate(student_proposition, model), msg='generated proposition is not correct')
    
        # test that their model works with my proposition:
        for i in range(2, 15):
            vor = fourCOLOR_sol.drawBlankVoronoiDiagram(num_points=i)
            proposition = fourCOLOR_sol.fourColoringToSAT(fourCOLOR_sol.getNeighbors(vor))

            parsed_prop, vars = fourCOLOR_sol.parse_proposition(proposition)
            model = SAT_sol.pySAT_solver(parsed_prop)
            model = fourCOLOR_sol.repackaged_model(model, vars)

            self.assertTrue(evaluate(proposition, model), msg='generated proposition is not correct')