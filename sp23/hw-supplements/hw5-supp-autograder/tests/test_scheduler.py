# CS 2051 Spring 2023
# author - Sarthak Mohanty
# collaborators - N/A

# these are the tests for the rules of inference solver

from gradescope_utils.autograder_utils.decorators import weight, number

import unittest
from unittest import mock
from io import StringIO

import scheduler_solution as sol
from scheduler import *

class TestScheduler(unittest.TestCase):

    def setUp(self) -> None:
        poset1 = [{1, 2, 3, 4, 5, 6}, {(1, 2), (2, 4), (3, 4), (4, 5), (5, 6)}]

        poset2 = [{'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'}, {('Sun', 'Mon'), ('Mon', 'Tue'), ('Tue', 'Wed'), ('Wed', 'Thu'), ('Thu', 'Fri'), ('Fri', 'Sat')}]

        poset3 = [{"CS 1301", "CS 1331", "CS 1332", "CS 2110"}, {("CS 1301", "CS 1331"), ("CS 1331", "CS 1332"), ("CS 1331", "CS 2110")}]

        # poset4 = [{"Completion", "Interior fixtures", "Exterior fixtures", "Interior painting", "Exterior painting", "Wall-board", "Wiring", "Exterior siding", "Roof", "Framing", "Foundation", "Carpeting", "Flooring", "Plumbing"}]
        poset4 = [{1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14}, 
                  {(1, 2), (1, 3), (3, 5), (2, 4), (1, 12), (12, 13), (13, 14), (14, 8), (8, 9), (9, 10), (10, 11), (4, 13), (6, 14), (6, 7), (7, 8), (5, 8), (4, 6)}]
        
        # poset5 =[{"Completion", "test1", "Integrate modules", "Develop module B", "Develop module C", "Set up test sites", "Write functional requirements", "Determine user needs", "test2", "Develop module A", "Write documentation", "Develop system requirements"}]
        poset5 = [{1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12}, 
                  {(1, 2), (2, 6), (6, 7), (7, 8), (12, 7), (11, 12), (9, 11), (2, 9), (9, 3), (3, 4), (3, 5), (3, 10), (4, 12), (10, 12), (5, 12)}]
        
        poset6 = [{'1301', '1331', '1332', '4641', '2051', '3600', '3511'},
                {('1301', '1331'), ('1331', '1332'), ('1332', '4641'),\
                ('2051', '3511'), ('1332', '3511'), ('1332', '3600')}]
        
        self.posets = [poset1, poset2, poset3, poset4, poset5, poset6]


        layers1 = [{1, 3}, {2}, {4}, {5}, {6}]
        layers2 = [{'Mon'}, {'Tue'}, {'Wed'}, {'Thu'}, {'Fri'}, {'Sat'}, {'Sun'}]
        layers3 = [{"CS 1301"}, {"CS 1331"}, {"CS 1332", "CS 2110"}]
        # See Rosen Exercises under "Partial Orderings" for visual representation of the following layers
        layers4 = [{1}, {2, 3, 12}, {4, 5}, {13, 6}, {14, 7}, {8}, {9}, {10}, {11}]
        layers5 = [{1}, {2}, {9}, {11, 3, 6}, {10, 4, 5}, {12}, {7}, {8}]

        self.layers = [layers1, layers2, layers3, layers4, layers5]

        def is_topological_sort(elements, relations, topological_sort):
                # ensure that the topological sort is a valid topological sort
                # 1. all elements are in the topological sort
                # 2. for each relation, the first element is before the second element in the topological sort
                for element in elements:
                    if element not in topological_sort:
                        return False

                for relation in relations:
                    if topological_sort.index(relation[0]) > topological_sort.index(relation[1]):
                        return False

                return True

        self.is_topological_sort = is_topological_sort

        self.longMessage = False


    @weight(10)
    @number("3")
    def test_topological_sort(self):
        with mock.patch('sys.stdout', new = StringIO()) as std_out:
            with mock.patch('scheduler.generate_schedule') as mock_generate_schedule:
                sample_topological_sort = topological_sort(self.posets[0][0], self.posets[0][1])
                self.assertFalse(mock_generate_schedule.called, msg="No cheating! You can't use the generate_schedule method for the topological_sort method.")
            
            for i in range(len(self.posets)):
                # test to make sure that generate_schedule is not being called
                student_topological_sort = topological_sort(self.posets[i][0], self.posets[i][1])

                self.assertTrue(self.is_topological_sort(self.posets[i][0], self.posets[i][1], student_topological_sort), msg=f"Topological sort failed")

    @weight(5)
    @number("4.1")
    def test_generate_schedule(self):
        with mock.patch('sys.stdout', new = StringIO()) as std_out:
            def is_valid_schedule(elements, relations, student_schedule, instructor_schedule):
                # ensure that the schedule is a valid schedule


                flattened_schedule = [item for sublist in student_schedule for item in sublist]
                # 1. all elements are in the schedule
                for element in elements:
                    if element not in flattened_schedule:
                        return False
                        # assert False, f"{element} not in schedule on poset {self.posets[i]}"

                # 2. flattened schedule is a topological sort
                if not self.is_topological_sort(elements, relations, flattened_schedule):
                    return False
                    # assert False, f"Schedule is not a topological sort"

                # 3. uses optimal number of layers
                if len(student_schedule) != len(instructor_schedule):
                    return False
                    # assert False, f"Schedule does not use optimal number of layers"

                return True

            for i in range(len(self.posets)):
                for j in range(1, len(self.posets[i][0])):
                    student_schedule = generate_schedule(self.posets[i][0], self.posets[i][1], j)
                    instructor_schedule = sol.generate_schedule(self.posets[i][0], self.posets[i][1], j)

                    # is_valid_schedule(self.posets[i][0], self.posets[i][1], student_schedule, instructor_schedule)

                    self.assertTrue(is_valid_schedule(self.posets[i][0], self.posets[i][1], student_schedule, instructor_schedule), msg=f"Schedule failed")

    @weight(5)
    @number("4.2")
    def test_generate_schedule_hidden(self):
        with mock.patch('sys.stdout', new = StringIO()) as std_out:
            def is_valid_schedule(elements, relations, student_schedule):
                # ensure that the schedule is a valid schedule


                flattened_schedule = [item for sublist in student_schedule for item in sublist]
                # 1. all elements are in the schedule
                for element in elements:
                    if element not in flattened_schedule:
                        return False
                        # assert False, f"{element} not in schedule on poset {self.posets[i]}"

                # 2. flattened schedule is a topological sort
                if not self.is_topological_sort(elements, relations, flattened_schedule):
                    return False
                    # assert False, f"Schedule is not a topological sort"

                return True
            
            hidden_poset1 = ({'1301', '1331', '1332', '4641', '2110', '2340', '2051', '3600', '3511'},
                                {('1301', '1331'), ('1331', '1332'), ('1332', '4641'),\
                                ('2051', '3511'), ('1332', '3511'), ('1332', '3600'),
                                ('1331', '2110'), ('1331', '2340')})
            hidden_poset2 = ({1, 2, 3, 4, 5, 6}, {(1, 5), (2, 5), (3, 4), (4, 5), (6, 5)})


            edge_case_01 = ({1, 2, 3, 4, 5}, {(1, 5), (2, 5), (3, 4), (4, 5)})
            edge_case_02 = ({1, 2, 3, 4, 5}, {(2, 5), (1, 5), (3, 4), (4, 5)})
            edge_case_03 = ({1, 2, 3, 4, 5}, {(1, 5), (2, 5), (4, 3), (3, 5)})
            edge_case_04 = ({1, 2, 3, 4, 5}, {(5, 1), (5, 2), (4, 3), (3, 1)})
            edge_case_05 = ({5, 4, 3, 2, 1}, {(1, 5), (2, 5), (3, 4), (4, 5)})
            edge_case_06 = ({5, 4, 3, 2, 1}, {(5, 1), (2, 1), (4, 3), (3, 1)})
            edge_case_07 = ({1, 2, 3, 4, 5}, {(4, 3), (2, 3), (5, 1), (1, 3)})
            edge_case_08 = ({1, 2, 3, 4, 5}, {(3, 4), (2, 4), (1, 5), (5, 4)})
            edge_case_09 = ({1, 2, 3, 4, 5}, {(4, 1), (2, 1), (5, 3), (3, 1)})
            edge_case_10 = ({1, 2, 3, 4, 5}, {(1, 5), (2, 5), (3, 4), (4, 5)})

            
            edge_case_11 = ({1, 2, 3, 4, 5}, {(1, 5), (2, 5), (4, 3), (3, 5)})
            edge_case_12 = ({1, 2, 3, 4, 5}, {(1, 5), (3, 4), (2, 5), (4, 5)})
            edge_case_13 = ({1, 2, 3, 4, 5}, {(1, 5), (3, 4), (4, 5), (2, 5)})
            edge_case_14 = ({1, 2, 3, 4, 5}, {(1, 5), (4, 3), (2, 5), (4, 5)})
            edge_case_15 = ({1, 2, 3, 4, 5}, {(1, 5), (4, 3), (4, 5), (2, 5)})
            edge_case_16 = ({1, 2, 3, 4, 5}, {(2, 5), (1, 5), (3, 4), (4, 5)})
            edge_case_17 = ({1, 2, 3, 4, 5}, {(2, 5), (1, 5), (4, 3), (3, 5)})
            edge_case_18 = ({1, 2, 3, 4, 5}, {(2, 5), (3, 4), (1, 5), (4, 5)})
            edge_case_19 = ({1, 2, 3, 4, 5}, {(2, 5), (3, 4), (4, 5), (1, 5)})
            edge_case_20 = ({1, 2, 3, 4, 5}, {(2, 5), (4, 3), (1, 5), (4, 5)})
            edge_case_21 = ({1, 2, 3, 4, 5}, {(2, 5), (4, 3), (4, 5), (1, 5)})
            edge_case_22 = ({1, 2, 3, 4, 5}, {(3, 4), (1, 5), (2, 5), (4, 5)})
            edge_case_23 = ({1, 2, 3, 4, 5}, {(3, 4), (1, 5), (4, 5), (2, 5)})
            edge_case_24 = ({1, 2, 3, 4, 5}, {(3, 4), (2, 5), (1, 5), (4, 5)})
            edge_case_25 = ({1, 2, 3, 4, 5}, {(3, 4), (2, 5), (4, 5), (1, 5)})
            edge_case_26 = ({1, 2, 3, 4, 5}, {(3, 4), (4, 5), (1, 5), (2, 5)})


            edge_cases = [edge_case_01, edge_case_02, edge_case_03, edge_case_04, edge_case_05, edge_case_06, edge_case_07, edge_case_08, edge_case_09, edge_case_10, edge_case_11, edge_case_12, edge_case_13, edge_case_14, edge_case_15, edge_case_16, edge_case_17, edge_case_18, edge_case_19, edge_case_20, edge_case_21, edge_case_22, edge_case_23, edge_case_24, edge_case_25, edge_case_26]

            student_schedule = generate_schedule(hidden_poset1[0], hidden_poset1[1], 2)

            self.assertTrue(is_valid_schedule(hidden_poset1[0], hidden_poset1[1], student_schedule), msg=f"Schedule not valid")
            self.assertTrue(len(student_schedule) == 5, msg=f"Schedule not optimal")

            student_schedule = generate_schedule(hidden_poset2[0], hidden_poset2[1], 3)
            
            self.assertTrue(is_valid_schedule(hidden_poset2[0], hidden_poset2[1], student_schedule), msg=f"Schedule not valid")
            self.assertTrue(len(student_schedule) == 3, msg=f"Schedule not optimal")

            for edge_case in edge_cases:
                student_schedule = generate_schedule(edge_case[0], edge_case[1], 2)

                self.assertTrue(is_valid_schedule(edge_case[0], edge_case[1], student_schedule), msg=f"Schedule not valid")
                self.assertTrue(len(student_schedule) == 3, msg=f"Schedule not optimal")
