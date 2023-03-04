# CS 2051 Spring 2023
# HW3 Supplement Helper
# author - Sarthak Mohanty
# collaborators - N/A

# these are the tests for the rules of inference solver

import unittest

# to hide the output of the print statements
from unittest import mock
from io import StringIO

from inference import infer

class TestInference(unittest.TestCase):
    def test_infer(self):
        with mock.patch('sys.stdout', new = StringIO()) as std_out:
            inference_rule1 = ['(not p) and q', 'r |implies| p', '(not r) |implies| s', 's |implies| t']
            inference_rule2 = ['p |iff| q', 'p |implies| (not r)']
            inference_rule3 = ['p |implies| q', '(not p) |implies| r', 'r |implies| s']
            inference_rule4 = ['(p and t) |implies| (r or s)', 'q |implies| (u and t)', 'u |implies| p', 'not s']
            inference_rule5 = ['p |implies| q', 'q |implies| r', 'p |implies| r', 'p |implies| s', 's |implies| t', 'p |implies| t', 't |implies| u', 'u |implies| v', 'p |implies| v', 'v |implies| w', 'w |implies| x', 'p |implies| x', 'x |implies| y', 'y |implies| z', 'p |implies| z']
            inference_rule6 = ['True']
            inference_rule7 = ['False']
            
            inference_rules = [inference_rule1, inference_rule2, inference_rule3, inference_rule4, inference_rule5, inference_rule6, inference_rule7]

            self.assertEqual(infer(inference_rules[0], 't'), True)
            self.assertEqual(infer(inference_rules[1], 'q or r'), False)
            self.assertEqual(infer(inference_rules[2], '(not q) |implies| s'), True)
            self.assertEqual(infer(inference_rules[3], 'q |implies| r'), True)
            self.assertEqual(infer(inference_rules[4], 'p |implies| z'), True)
            self.assertEqual(infer(inference_rules[5], 'False'), False)
            self.assertEqual(infer(inference_rules[6], 'True'), True)
            self.assertEqual(infer([], 'False'), False, msg="Almost there! Missing an edge case")
            self.assertEqual(infer([], 'True'), True, msg="Almost there! Missing an edge case")
            self.assertEqual(infer([], '((r and s) |implies| t) |iff| (r |implies| (s |implies| t))'), True, msg="Almost there! Missing an edge case")
            self.assertEqual(infer([], 'p and q'), False, msg="Almost there! Missing an edge case")
