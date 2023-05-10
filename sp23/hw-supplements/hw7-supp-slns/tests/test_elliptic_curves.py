# CS 2051 Spring 2023
# author - Sarthak Mohanty
# collaborators - N/A

# these are the tests for elliptic_curves.py

import unittest
from unittest import mock
from io import StringIO

import elliptic_curves_solution as sol
from elliptic_curves import *

import random

class TestEllipticCurves(unittest.TestCase):
    def setUp(self) -> None:
        # curve1 = (-15, 10)
        curve2 = (-2, 3)
        curve3 = (-7, 10)
        curve4 = (3, 10)
        curve5 = (4, 3)

        self.curves = [curve2, curve3, curve4, curve5]
        self.primes = [3, 5, 7, 11, 73, 151, 157, 251, 503, 311, 797, 811]

        self.longMessage = False

    def test_point_addition(self):
        with mock.patch('sys.stdout', new = StringIO()) as std_out:
            for curve in self.curves:
                a, b = curve[0], curve[1]
                
                for _ in range(100):
                    # choose random valid points in range from -100 and 100
                    while True:
                        x1 = random.randint(-100, 100)
                        if f(x1, a, b) != (None, None):
                            P = (x1, f(x1, a, b)[0])
                            break
                    while True:
                        x2 = random.randint(-100, 100)
                        if f(x2, a, b) != (None, None) and x2 != x1:
                            Q = (x2, f(x2, a, b)[0])
                            break
                    student_R = point_addition(P, Q, *curve)
                    solution_R = sol.point_addition(P, Q, *curve)
                    self.assertAlmostEqual(student_R[0], solution_R[0], places=3)
                    self.assertAlmostEqual(student_R[1], solution_R[1], places=3)

                # test point addition with point at infinity
                while True:
                    x = random.randint(-100, 100)
                    if f(x, a, b) != (None, None):
                        P = (x, f(x, a, b)[0])
                        Q = (x, f(x, a, b)[1])
                        break
                self.assertEqual(point_addition(P, Q, *curve), (None, None) , msg = "edge case")

    def test_point_addition_over_field(self):
        with mock.patch('sys.stdout', new = StringIO()) as std_out:
            for curve in self.curves:
                for prime in self.primes:
                    curve_over_field = (*curve, prime)
                    points = sol.generate_point_cloud(*curve_over_field)
                    for _ in range(10):
                        P, Q = random.sample(list(points), 2)
                        student_R = point_addition(P, Q, *curve_over_field)
                        solution_R = sol.point_addition(P, Q, *curve_over_field)
                        self.assertAlmostEqual(student_R[0], solution_R[0], places=3)
                        self.assertAlmostEqual(student_R[1], solution_R[1], places=3)

            # test point addition with point at infinity
            curve = (2, 3, 97)
            P = (17, 10)
            Q = (17, 87)
            self.assertEqual(point_addition(P, Q, *curve), (None, None), msg = "edge case")

    def test_point_multiplication(self):
        with mock.patch('sys.stdout', new = StringIO()) as std_out:
            for curve in self.curves:
                a, b = curve[0], curve[1]
                for _ in range(100):
                # choose random points in range from -200 to 200
                    while True:
                        x = random.randint(-200, 200)
                        if f(x, a, b) != (None, None):
                            P = (x, f(x, a, b)[0])
                            break
                    k = random.randint(1, 10)
                    student_R = point_scalar_multiplication(P, k, *curve)
                    solution_R = sol.point_scalar_multiplication(P, k, *curve)
                    self.assertAlmostEqual(student_R[0], solution_R[0], places=3, msg=f"wrong for curve parameters {curve} and point {P} and scalar {k}, student output {student_R}, solution output {solution_R}")
                    self.assertAlmostEqual(student_R[1], solution_R[1], places=3)
                
            # test point multiplication with point at infinity
            curve = (-6, 9)
            P = (-3, 0)
            k = 2
            self.assertEqual(point_scalar_multiplication(P, k, *curve), (None, None), msg = "edge case")
            self.assertEqual(point_scalar_multiplication(P, k + 1, *curve), P, msg = "edge case")

    def test_point_multiplication_over_field(self):
        with mock.patch('sys.stdout', new = StringIO()) as std_out:
            for curve in self.curves:
                for prime in self.primes:
                    curve_over_field = (*curve, prime)
                    points = sol.generate_point_cloud(*curve_over_field)
                    for _ in range(10):
                        P = random.choice(list(points))
                        k = random.randint(1, 100)
                        self.assertEqual(point_scalar_multiplication(P, k, *curve_over_field), sol.point_scalar_multiplication(P, k, *curve_over_field))

            # test point addition with point at infinity
            curve = (-4, 3, 89)
            P = (10, 42)
            k = 8
            self.assertEqual(point_scalar_multiplication(P, k, *curve), (None, None), msg = "edge case")
            self.assertAlmostEqual(point_scalar_multiplication(P, k + 1, *curve)[0], P[0], msg = "edge case")
            self.assertAlmostEqual(point_scalar_multiplication(P, k + 1, *curve)[1], P[1], msg = "edge caes")

    def test_generate_point_cloud(self):
        with mock.patch('sys.stdout', new = StringIO()) as std_out:
            for curve in self.curves:
                for prime in self.primes:
                    curve_over_field = (*curve, prime)
                    student_points = generate_point_cloud(*curve_over_field)
                    instructor_points = sol.generate_point_cloud(*curve_over_field)
                    # point at infinity should be in both, but I forgot to mention it in pdf
                    # so I will remove it from both lists and then compare
                    if (None, None) in student_points:
                        student_points.remove((None, None))
                    if (None, None) in instructor_points:
                        instructor_points.remove((None, None))
                    for point in list(instructor_points):
                        self.assertIn(point, student_points,msg="missing some points")
                    for point in list(student_points):
                        self.assertIn(point, instructor_points,msg="extra points")