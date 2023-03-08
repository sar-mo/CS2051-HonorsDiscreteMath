# CS 2051 Spring 2023
# author - Sarthak Mohanty
# collaborators - N/A

# these are the tests for the rules of inference solver

import unittest
from unittest import mock
from io import StringIO
import inspect

import relations
import relations_solution as sol
from relations import *

class TestRelations(unittest.TestCase):
    def setUp(self) -> None:

        relation01 = [(0, 0), (1, 1), (2, 2), (3, 3)]
        relation02 = [(0, 0), (1, 1), (2, 0), (2, 2), (2, 3), (3, 2), (3, 3)]
        relation03 = [(0, 0), (1, 1), (1, 2), (2, 2), (3, 3)]
        relation04 = [(0, 0), (1, 1), (1, 2), (1, 3), (2, 2), (2, 3), (3, 3)]
        relation05 = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 2), (3, 3)]
        relation06 = [(0, 0), (2, 2), (3, 3)]
        relation07 = [(0, 0), (1, 1), (2, 0), (2, 2), (2, 3), (3, 3)]
        relation08 = [(0, 0), (1, 1), (1, 2), (2, 2), (3, 1), (3, 3)]
        relation09 = [(0, 0), (1, 1), (1, 2), (1, 3), (2, 0), (2, 2), (2, 3), (3, 0), (3, 3)]
        relation10 = [(0, 0), (0, 1), (0, 2), (0, 3), (1, 0), (1, 1), (1, 2), (1, 3), (2, 0), (2, 2), (3, 3)]
        relation11 = [(0, 0)]
        relation12 = [(1, 1), (2, 2), (0, 0), (3, 3), (1, 2), (2, 1)]
        relation13 = []

        self.relations = [relation01, relation02, relation03, relation04, relation05, relation06, relation07, relation08, relation09, relation10, relation11, relation12, relation13]
        self.elements = {0, 1, 2, 3}

        # test to make sure all methods are one line
        def test_allMethodOneLine():
            for method in [isReflexive, isSymmetric, isAntiSymmetric, isTransitive, isEquivalenceRelation, isPartialOrder]:
                source_lines = inspect.getsource(method).strip().split('\n')
                assert len(source_lines) == 2 or len(source_lines) == 1, f"{method.__name__} is not one line long."
        
        # test to make sure only allowed methods are there
        def test_allowedMethods():
            allowed_methods = ["isReflexive", "isSymmetric", "isAntiSymmetric", "isTransitive", "isEquivalenceRelation", "isPartialOrder", "partition"]
            for name, obj in inspect.getmembers(relations):
                if name not in allowed_methods and inspect.isfunction(obj):
                    assert False, f"{relations.__name__} contains an unauthorized method {name}."
                elif name in allowed_methods and not inspect.isfunction(obj):
                    assert False, f"{relations.__name__} does not contain method {name}."
            assert True

        self.test_allMethodOneLine = test_allMethodOneLine
        self.test_allowedMethods = test_allowedMethods

        self.longMessage = False

    def test_isPartialOrder(self):
        with mock.patch('sys.stdout', new = StringIO()) as std_out:
            self.test_allMethodOneLine()
            self.test_allowedMethods()
            for i in range(len(self.relations)):
                self.assertEqual(isPartialOrder(self.elements, self.relations[i]), sol.isPartialOrder(self.elements, self.relations[i]), msg='isPartialOrder failed')
            # edge case with no elements in domain
            self.assertEqual(isPartialOrder({}, {}), True, msg="Failed, look at the *formal* definition of reflexivity, antisymmetry, and transitivity.")

    def test_isEquivalence_Relation(self):
        with mock.patch('sys.stdout', new = StringIO()) as std_out:
            self.test_allMethodOneLine()
            self.test_allowedMethods()
            for i in range(len(self.relations)):
                self.assertEqual(isEquivalenceRelation(self.elements, self.relations[i]), sol.isEquivalenceRelation(self.elements, self.relations[i]), msg='isEquivalenceRelation failed')
            # edge case with no elements in domain
            self.assertEqual(isPartialOrder({}, {}), True, msg="Failed, look at the *formal* definition of reflexivity, antisymmetry, and transitivity.")
    
    def test_partition(self):
        # equivalence relation on set of integers
        # such that x R y if and only if x = y
        elements1 = {-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5}
        equiv_relation1 = lambda x, y: x == y

        # equivalence relation on set of positive integers
        # such that x R y if and only if x and y have the same parity
        elements2 = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}
        equiv_relation2 = lambda x, y: x % 2 == y % 2

        # equivalence relation on set of ordered pairs of positive integers
        # such that ((a, b), (c, d)) are equivalent if a + b = c + d
        elements3 = {(1, 2), (2, 1), (1, 1), (2, 2), (2, 3)}
        equiv_relation3 = lambda x, y: x[0] + x[1] == y[0] + y[1]

        # equivalence relation on set of ordered pairs of positive integers
        # such that ((a, b), (c, d)) are equivalent if ab = cd
        elements4 = {(1, 2), (2, 1), (1, 1), (2, 2), (2, 3)}
        equiv_relation4 = lambda x, y: x[0] * x[1] == y[0] * y[1]

        # equivalence relation on set of all bit strings such that 
        # s R t if and only if s and t have the same number of 1's
        elements5 = {'000', '001', '010', '011', '100', '101', '110', '111', '0000'}
        equiv_relation5 = lambda x, y: x.count('1') == y.count('1')

        # equivalence relation on set of all bit strings of length three
        # or more such that x R y iff x and y agree in their first and third bits
        elements6 = {'000', '001', '010', '011', '100', '101', '110', '111', '0000'}
        equiv_relation6 = lambda x, y: x[0] == y[0] and x[2] == y[2]

        elements = [elements1, elements2, elements3, elements4, elements5, elements6]
        equiv_relations = [equiv_relation1, equiv_relation2, equiv_relation3, equiv_relation4, equiv_relation5, equiv_relation6]

        for i in range(len(elements)):
            instructor_list = sol.partition(elements[i].copy(), equiv_relations[i])
            student_list = partition(elements[i].copy(), equiv_relations[i])
            self.assertTrue(all(student_set in instructor_list for student_set in student_list))