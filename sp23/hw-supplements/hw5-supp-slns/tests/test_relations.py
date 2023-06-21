# CS 2051 Spring 2023
# author - Sarthak Mohanty
# collaborators - N/A

# these are the tests for the rules of inference solver

import unittest
import inspect

import relations
from relations import *

import json

class TestRelations(unittest.TestCase):
    def setUp(self) -> None:

        with open('tests/sample_relations.json', 'r') as f:
            relations_json = json.load(f)
        # convert all relations_json['elements'] to sets
        self.elements = [set(relation_json['elements']) for relation_json in relations_json]
        # convert all lists in relations_json['relations'] to tuples
        self.binary_relations = []
        for relation_json in relations_json:
            relation_json['relation'] = [tuple(relation) for relation in relation_json['relation']]
            self.binary_relations.append(relation_json['relation'])
        self.is_partial_order = [relation_json['partial order'] for relation_json in relations_json]
        self.is_equivalence_relation = [relation_json['equivalence relation'] for relation_json in relations_json]

        with open('tests/sample_partitions.json', 'r') as f:
            partitions_json = json.load(f)
        # convert all partitions_json['domain'] to sets, and sets of tuples if domain is a list of lists
        self.domains = [set(partition_json['domain']) for partition_json in partitions_json]
        # get equivalence relation as function
        self.equivalence_relations = [eval(partition_json['relation']) for partition_json in partitions_json]
        # convert all lists in partitions_json['partition'] to sets
        self.sample_partitions = []
        for partition_json in partitions_json:
            partition_json['sample_partition'] = [set(l) for l in partition_json['sample_partition']]
            self.sample_partitions.append(partition_json['sample_partition'])

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
        self.test_allMethodOneLine()
        self.test_allowedMethods()
        for i in range(len(self.binary_relations)):
            self.assertEqual(isPartialOrder(self.elements[i], self.binary_relations[i]), self.is_partial_order[i], msg='isPartialOrder failed')
        self.assertEqual(isPartialOrder({}, {}), True, msg="Failed, look at the *formal* definition of reflexivity, antisymmetry, and transitivity.")

    def test_isEquivalenceRelation(self):
        self.test_allMethodOneLine()
        self.test_allowedMethods()
        for i in range(len(self.binary_relations)):
            self.assertEqual(isEquivalenceRelation(self.elements[i], self.binary_relations[i]), self.is_equivalence_relation[i], msg='isEquivalenceRelation failed')
        # edge case with no elements in domain
        self.assertEqual(isEquivalenceRelation({}, {}), True, msg="Failed, look at the *formal* definition of reflexivity, symmetry, and transitivity.")
    
    def test_partition(self):
        for i in range(len(self.domains)):
            student_partition = partition(self.domains[i], self.equivalence_relations[i])
            self.assertTrue(all(student_set in self.sample_partitions[i] for student_set in student_partition), msg=f'{student_partition}, {self.sample_partitions[i]}')