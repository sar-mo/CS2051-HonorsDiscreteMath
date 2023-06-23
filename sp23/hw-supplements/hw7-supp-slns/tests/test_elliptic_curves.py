# CS 2051 Spring 2023
# author - Sarthak Mohanty
# collaborators - N/A

# these are the tests for elliptic_curves.py

import unittest

from elliptic_curves import *

import json

class TestEllipticCurves(unittest.TestCase):
    def setUp(self) -> None:
        with open('tests/sample_elliptic_curve_problems.json', 'r') as f:
            self.curve_problems = json.load(f)
        
        # convert every point to tuple
        for curve_problem in self.curve_problems:
            curve_problem["point_cloud"] = set([tuple(point) for point in curve_problem["point_cloud"]])
            for addition_problem in curve_problem["sample_point_addition_problems"]:
                addition_problem["P"] = tuple(addition_problem["P"])
                addition_problem["Q"] = tuple(addition_problem["Q"])
                addition_problem["R"] = tuple(addition_problem["R"])
            for multiplication_problem in curve_problem["sample_point_multiplication_problems"]:
                multiplication_problem["P"] = tuple(multiplication_problem["P"])
                multiplication_problem["Q"] = tuple(multiplication_problem["Q"])

    def test_point_addition_over_field(self):
        for curve_problem in self.curve_problems:
            curve = tuple(curve_problem["curve_parameters"].values())
            for addition_problem in curve_problem["sample_point_addition_problems"]:
                P = addition_problem["P"]
                Q = addition_problem["Q"]
                R = addition_problem["R"]
                self.assertEqual(point_addition(P, Q, *curve), R)

        # test point addition with point at infinity
        curve = (2, 3, 97)
        P = (17, 10)
        Q = (17, 87)
        self.assertEqual(point_addition(P, Q, *curve), (None, None),
                         msg = "failed edge case, think about what happens when the two points have the same x-coordinate")

    def test_point_multiplication_over_field(self):
        for curve_problem in self.curve_problems:
            curve = tuple(curve_problem["curve_parameters"].values())
            for multiplication_problem in curve_problem["sample_point_multiplication_problems"]:
                P = multiplication_problem["P"]
                k = multiplication_problem["k"]
                Q = multiplication_problem["Q"]
                self.assertEqual(point_scalar_multiplication(P, k, *curve), Q)
        
        # test point multiplication with point at infinity
        curve = (-4, 3, 89)
        P = (10, 42)
        k = 8
        self.assertEqual(point_scalar_multiplication(P, k, *curve), (None, None), msg = 'failed edge case')
        self.assertAlmostEqual(point_scalar_multiplication(P, k + 1, *curve)[0], P[0], msg = 'failed edge case')
        self.assertAlmostEqual(point_scalar_multiplication(P, k + 1, *curve)[1], P[1], msg = "failed edge case")

    def test_generate_point_cloud(self):
        for curve_problem in self.curve_problems:
            curve = tuple(curve_problem["curve_parameters"].values())
            point_cloud = curve_problem["point_cloud"]
            self.assertEqual(generate_point_cloud(*curve), point_cloud)