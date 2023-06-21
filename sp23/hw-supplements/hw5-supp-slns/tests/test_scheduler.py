# CS 2051 Spring 2023
# author - Sarthak Mohanty
# collaborators - N/A

# these are the tests for the rules of inference solver

import unittest
from unittest import mock
from io import StringIO

from scheduler import *

import json

class TestScheduler(unittest.TestCase):
    def setUp(self) -> None:

        with open('tests/sample_schedules.json', 'r') as f:
            schedules_json = json.load(f)

        # convert all schedules_json['elements'] to sets
        self.elements = [set(schedule_json['elements']) for schedule_json in schedules_json]

        # convert all lists in schedules_json['poset'] to tuples
        self.posets = []
        for schedule_json in schedules_json:
            schedule_json['poset'] = [tuple(poset) for poset in schedule_json['poset']]
            self.posets.append(schedule_json['poset'])

        self.num_processors = [schedule_json['num_processors'] for schedule_json in schedules_json]
        self.schedules = [schedule_json['schedule'] for schedule_json in schedules_json]

        def is_topological_sort(elements, poset, topological_sort):
                # 1. all elements are in the topological sort
                for element in elements:
                    if element not in topological_sort:
                        return False

                # 2. for each pair, the first element is before the second element in the topological sort
                for pair in poset:
                    if topological_sort.index(pair[0]) > topological_sort.index(pair[1]):
                        return False

                return True

        self.is_topological_sort = is_topological_sort

        self.longMessage = False

    def test_topological_sort(self):
        for i in range(len(self.posets)):
            student_topological_sort = topological_sort(self.elements[i], self.posets[i])
            self.assertTrue(self.is_topological_sort(self.elements[i], self.posets[i], student_topological_sort),\
                            msg=f"Topological sort failed")

    def test_generate_schedule(self):
        for i in range(len(self.posets)):
            elements = self.elements[i]
            poset = self.posets[i]
            num_processors = self.num_processors[i]
            instructor_schedule = self.schedules[i]
            student_schedule = generate_schedule(elements, poset, num_processors)

            # Test 1: Check that the schedule is a valid topological sort
            flattened_student_schedule = [item for sublist in student_schedule for item in sublist]
            self.assertTrue(self.is_topological_sort(elements, poset, flattened_student_schedule), msg=f"schedule not valid")

            # Test 2: Check that the schedule does not use more than num_processors processors
            self.assertTrue(all(len(sublist) <= num_processors for sublist in student_schedule),\
                            msg=f"schedule uses more than {num_processors} processors")
            
            # Test 3: Check that the schedule is optimal
            self.assertTrue(len(student_schedule) == len(instructor_schedule), msg=f"schedule not optimal")