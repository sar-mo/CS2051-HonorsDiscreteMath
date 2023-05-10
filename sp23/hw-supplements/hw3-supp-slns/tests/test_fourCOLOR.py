# CS 2051 Spring 2023
# HW3 Supplement Helper
# author - Sarthak Mohanty
# collaborators - N/A

# these are the tests for the SAT fourCOLOR_solver

import unittest

from logic_helper import evaluate
import SAT
from fourCOLOR import *

import random
import json

class Test4COLOR(unittest.TestCase):

    def setUp(self) -> None:
        # a list of 50 sample fourCOLOR problems, with the i-th elememt corresponding to a problem with i points
        self.fourCOLOR_problems = json.load(open('tests/fourCOLOR_sample_problems.json', 'r'))

    def test_fourCOLOR_to_SAT(self):
        for i in range(2, 20):
            proposition = self.fourCOLOR_problems[i]['SAT_problem']
            parsed_prop = convert_proposition_to_pySAT_format(proposition)
            vars = set([abs(lit) for clause in parsed_prop for lit in clause])
            orig_model = SAT.pySAT_solver(parsed_prop)
            orig_model = convert_pySAT_output_to_colorMap_format(orig_model, vars)

            model = orig_model.copy()
            neighbors_of_region = []
            # pick random region's color to change
            random_variable = random.choice([var for var in model if model[var]])
            color = random_variable[0]
            region = int(random_variable[1:])

            # Test 1: test that proposition fails when when making two regions the same color
            neighbors = self.fourCOLOR_problems[i]['neighbors']
            neighbors_of_region = neighbors[region][1]
            random_neighbor = random.choice(neighbors_of_region)
            model[color + str(random_neighbor)] = True
            colors = ['r', 'g', 'b', 'y']
            colors.remove(color)
            for other_color in colors:
                model[other_color + str(random_neighbor)] = False
            student_proposition = fourCOLOR_to_SAT(self.fourCOLOR_problems[i]['neighbors'])
            self.assertFalse(eval(student_proposition, model), msg='generated proposition is not correct')

            # Test 2: test that proposition fails when assigning more than one color to a region
            # test could be improved
            colors = ['r', 'g', 'b', 'y']
            colors.remove(color)
            for other_color in colors:
                model = orig_model.copy()
                model[other_color + str(region)] = True
            self.assertFalse(eval(student_proposition, model), msg='generated proposition is not correct')

            # Test 3: test that proposition fails when assigning no color to a region
            model = orig_model.copy()
            colors = ['r', 'g', 'b', 'y']
            for c in colors:
                model[c + str(region)] = False
            self.assertFalse(eval(student_proposition, model), msg='generated proposition is not correct')

            # Test 4: Test that a correct model works with their proposition
            # ensures there are not extra literals
            vor = draw_blank_voronoi_diagram(num_points=i)
            student_proposition = fourCOLOR_to_SAT(get_neighbors(vor))

            parsed_prop = convert_proposition_to_pySAT_format(student_proposition)
            vars = set([abs(lit) for clause in parsed_prop for lit in clause])
            model = SAT.pySAT_solver(parsed_prop)
            model = convert_pySAT_output_to_colorMap_format(model, vars)

            self.assertTrue(eval(student_proposition, model), msg='generated proposition is not correct')
