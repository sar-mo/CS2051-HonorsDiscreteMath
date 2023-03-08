# CS 2051 Spring 2023
# author - Sarthak Mohanty
# collaborators - N/A

# these are the tests for the rules of inference solver

import unittest
from unittest import mock
from io import StringIO

from scheduler import *
import scheduler_solution as sol

class TestScheduler(unittest.TestCase):
    def setUp(self) -> None:
        poset1 = [{1, 2, 3, 4, 5, 6}, {(1, 2), (2, 4), (3, 4), (4, 5), (5, 6)}]

        poset2 = [{'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'}, {('Sun', 'Mon'), ('Mon', 'Tue'), ('Tue', 'Wed'), ('Wed', 'Thu'), ('Thu', 'Fri'), ('Fri', 'Sat')}]

        poset3 = [{"CS 1301", "CS 1331", "CS 1332", "CS 2110"}, {("CS 1301", "CS 1331"), ("CS 1331", "CS 1332"), ("CS 1331", "CS 2110")}]

        # See Rosen Exercises under "Partial Orderings" for visual representation of the following posets

        # poset4 = [{"Completion", "Interior fixtures", "Exterior fixtures", "Interior painting", "Exterior painting", "Wall-board", "Wiring", "Exterior siding", "Roof", "Framing", "Foundation", "Carpeting", "Flooring", "Plumbing"}]
        poset4 = [{1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14}, 
                  {(1, 2), (1, 3), (3, 5), (2, 4), (1, 12), (12, 13), (13, 14), (14, 8), (8, 9), (9, 10), (10, 11), (4, 13), (6, 14), (6, 7), (7, 8), (5, 8), (4, 6)}]
        
        # poset5 =[{"Completion", "test1", "Integrate modules", "Develop module B", "Develop module C", "Set up test sites", "Write functional requirements", "Determine user needs", "test2", "Develop module A", "Write documentation", "Develop system requirements"}]
        poset5 = [{1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12}, 
                  {(1, 2), (2, 6), (6, 7), (7, 8), (12, 7), (11, 12), (9, 11), (2, 9), (9, 3), (3, 4), (3, 5), (3, 10), (4, 12), (10, 12), (5, 12)}]
        
        poset6 = [{'1301', '1331', '1332', '4641', '2051', '3600', '3511'},
                {('1301', '1331'), ('1331', '1332'), ('1332', '4641'),\
                ('2051', '3511'), ('1332', '3511'), ('1332', '3600')}]
        
        hidden_poset1 = ({'1301', '1331', '1332', '4641', '2110', '2340', '2051', '3600', '3511'},
                            {('1301', '1331'), ('1331', '1332'), ('1332', '4641'),\
                            ('2051', '3511'), ('1332', '3511'), ('1332', '3600'),
                            ('1331', '2110'), ('1331', '2340')})
        hidden_poset2 = ({1, 2, 3, 4, 5, 6}, {(1, 5), (2, 5), (3, 4), (4, 5), (6, 5)})
        
        self.posets = [poset1, poset2, poset3, poset4, poset5, poset6]
        self.hidden_posets = [hidden_poset1, hidden_poset2]

        def is_topological_sort(elements, poset, topological_sort):
                # 1. all elements are in the topological sort
                for element in elements:
                    if element not in topological_sort:
                        return False

                # 2. for each relation, the first element is before the second element in the topological sort
                for relation in poset:
                    if topological_sort.index(relation[0]) > topological_sort.index(relation[1]):
                        return False

                return True
        
        def is_optimal_schedule(elements, poset, num_processors, student_schedule):
            instructor_schedule = sol.generate_schedule(elements, poset, num_processors)
            if len(student_schedule) != len(instructor_schedule):
                return False
            return True

        self.is_topological_sort = is_topological_sort
        self.is_optimal_schedule = is_optimal_schedule

        self.longMessage = False


    def test_topological_sort(self):
        with mock.patch('sys.stdout', new = StringIO()) as std_out:
            for i in range(len(self.posets)):
                student_topological_sort = topological_sort(*self.posets[i])
                self.assertTrue(self.is_topological_sort(*self.posets[i], student_topological_sort), msg=f"Topological sort failed")

    def test_generate_schedule(self):
        with mock.patch('sys.stdout', new = StringIO()) as std_out:
            for i in range(len(self.posets)):
                for j in range(1, len(self.posets[i][0])):
                    student_schedule = generate_schedule(*self.posets[i], j)
                    flattened_student_schedule = [item for sublist in student_schedule for item in sublist]

                    self.assertTrue(self.is_topological_sort(*self.posets[i], flattened_student_schedule), msg=f"schedule not valid")
                    self.assertTrue(self.is_optimal_schedule(*self.posets[i], j, student_schedule), msg=f"schedule not optimal")

    def test_generate_schedule_hidden(self):
        with mock.patch('sys.stdout', new = StringIO()) as std_out:
            # edge cases are to prevent non-deterministic behavior
            # I don't know if there is a better way to do this plz tell me if there is
            edge_case_01 = ({(1, 5), (2, 5), (3, 4), (4, 5)})
            edge_case_02 = ({(2, 5), (1, 5), (3, 4), (4, 5)})
            edge_case_03 = ({(1, 5), (2, 5), (4, 3), (3, 5)})
            edge_case_04 = ({(5, 1), (5, 2), (4, 3), (3, 1)})
            edge_case_05 = ({(1, 5), (2, 5), (3, 4), (4, 5)})
            edge_case_06 = ({(5, 1), (2, 1), (4, 3), (3, 1)})
            edge_case_07 = ({(4, 3), (2, 3), (5, 1), (1, 3)})
            edge_case_08 = ({(3, 4), (2, 4), (1, 5), (5, 4)})
            edge_case_09 = ({(4, 1), (2, 1), (5, 3), (3, 1)})
            edge_case_10 = ({(1, 5), (2, 5), (3, 4), (4, 5)})
            edge_case_11 = ({(1, 5), (2, 5), (4, 3), (3, 5)})
            edge_case_12 = ({(1, 5), (3, 4), (2, 5), (4, 5)})
            edge_case_13 = ({(1, 5), (3, 4), (4, 5), (2, 5)})
            edge_case_14 = ({(1, 5), (4, 3), (2, 5), (4, 5)})
            edge_case_15 = ({(1, 5), (4, 3), (4, 5), (2, 5)})
            edge_case_16 = ({(2, 5), (1, 5), (3, 4), (4, 5)})
            edge_case_17 = ({(2, 5), (1, 5), (4, 3), (3, 5)})
            edge_case_18 = ({(2, 5), (3, 4), (1, 5), (4, 5)})
            edge_case_19 = ({(2, 5), (3, 4), (4, 5), (1, 5)})
            edge_case_20 = ({(2, 5), (4, 3), (1, 5), (4, 5)})
            edge_case_21 = ({(2, 5), (4, 3), (4, 5), (1, 5)})
            edge_case_22 = ({(3, 4), (1, 5), (2, 5), (4, 5)})
            edge_case_23 = ({(3, 4), (1, 5), (4, 5), (2, 5)})
            edge_case_24 = ({(3, 4), (2, 5), (1, 5), (4, 5)})
            edge_case_25 = ({(3, 4), (2, 5), (4, 5), (1, 5)})
            edge_case_26 = ({(3, 4), (4, 5), (1, 5), (2, 5)})
            edge_case_27 = ({(2, 5), (1, 5), (3, 4), (4, 5)})
            edge_case_28 = ({(1, 5), (3, 5), (2, 4), (4, 5)})
            edge_case_29 = ({(1, 5), (2, 5), (4, 3), (3, 5)})
            edge_case_30 = ({(1, 4), (2, 4), (3, 5), (5, 4)})
            edge_case_31 = ({(5, 1), (2, 1), (3, 4), (4, 1)})
            edge_case_32 = ({(3, 5), (2, 5), (1, 4), (4, 5)})
            edge_case_33 = ({(4, 5), (2, 5), (3, 1), (1, 5)})
            edge_case_34 = ({(1, 5), (4, 5), (3, 2), (2, 5)})
            edge_case_35 = ({(1, 5), (5, 2), (3, 4), (4, 2)})

            edge_cases = [edge_case_01, edge_case_02, edge_case_03, edge_case_04, edge_case_05, edge_case_06, edge_case_07, edge_case_08, edge_case_09, edge_case_10
                            , edge_case_11, edge_case_12, edge_case_13, edge_case_14, edge_case_15, edge_case_16, edge_case_17, edge_case_18, edge_case_19, edge_case_20
                            , edge_case_21, edge_case_22, edge_case_23, edge_case_24, edge_case_25, edge_case_26, edge_case_27, edge_case_28, edge_case_29, edge_case_30
                            , edge_case_31, edge_case_32, edge_case_33, edge_case_34, edge_case_35]
            edge_case_elements = {1, 2, 3, 4, 5}

            
            hidden_poset = self.hidden_posets[0]
            student_schedule = generate_schedule(hidden_poset[0], hidden_poset[1], 2)
            flattened_student_schedule = [item for sublist in student_schedule for item in sublist]
            self.assertTrue(self.is_topological_sort(*hidden_poset, flattened_student_schedule), msg=f"Schedule not valid")
            self.assertTrue(self.is_optimal_schedule(*hidden_poset, 2, student_schedule), msg=f"Schedule not optimal")

            hidden_poset = self.hidden_posets[1]
            student_schedule = generate_schedule(hidden_poset[0], hidden_poset[1], 3)
            flattened_student_schedule = [item for sublist in student_schedule for item in sublist]
            self.assertTrue(self.is_topological_sort(*hidden_poset, flattened_student_schedule), msg=f"Schedule not valid")
            self.assertTrue(self.is_optimal_schedule(*hidden_poset, 3, student_schedule), msg=f"Schedule not optimal")         

            for edge_case in edge_cases:
                student_schedule = generate_schedule(edge_case_elements, edge_case, 2)
                flattened_student_schedule = [item for sublist in student_schedule for item in sublist]
                self.assertTrue(self.is_topological_sort(edge_case_elements, edge_case, flattened_student_schedule), msg=f"Schedule not valid")
                self.assertTrue(len(student_schedule) == 3, msg=f"Schedule not optimal")