# Author: Sarthak Mohanty
# these are the test cases for hw0-supplement
import unittest
from proposition import Proposition, Implication, Equivalence, extract_variables

class TestPropositions(unittest.TestCase):
    def setUp(self):
        prop1 = Proposition('p and q')
        prop2 = Proposition('not s')
        prop3 = Proposition('p and q and r')
        prop4 = Proposition('((p) and q) or (not t)')
        prop5 = Proposition('(((((p and q) or (not r)) and s) and t) or u) and ((not v) and (w and x))')
        self.props = [prop1, prop2, prop3, prop4, prop5]

        imp1 = Implication(self.props[0], self.props[1])
        imp2 = Implication(self.props[2], self.props[3])
        imp3 = Implication(self.props[4], self.props[0])
        imp4 = Implication(self.props[1], self.props[3])
        imp5 = Implication(self.props[1], self.props[0])
        self.imps = [imp1, imp2, imp3, imp4, imp5]

        eq1 = Equivalence(self.props[0], self.props[1])
        eq2 = Equivalence(self.props[2], self.props[3])
        eq3 = Equivalence(self.props[4], self.props[0])
        eq4 = Equivalence(self.props[1], self.props[3])
        eq5 = Equivalence(self.props[1], self.props[0])
        self.eqs = [eq1, eq2, eq3, eq4, eq5]

    def test_proposition_structure(self):
        # check that the proposition has one attribute named func
        prop = Proposition("p")
        self.assertTrue(hasattr(prop, 'func'), 'Proposition class does not have an attribute named func')

    def test_implication_structure(self):
        imp = Implication(Proposition('p'), Proposition('q'))
        # check that the implication has one attribute named func
        self.assertTrue(hasattr(imp, 'func'), 'Implication class does not have an attribute named func')
        # check that the implication inherits from Proposition
        self.assertTrue(issubclass(Implication, Proposition), 'Implication class does not inherit from Proposition class')

    def test_equivalence_structure(self):
        eq = Equivalence(Proposition('p'), Proposition('q'))
        # check that the equivalence has one attribute named func    
        self.assertTrue(hasattr(eq, 'func'), 'Equivalence class does not have an attribute named func')
        # check that the equivalence inherits from Proposition
        self.assertTrue(issubclass(Equivalence, Proposition), 'Equivalence class does not inherit from Proposition class')

    def test_proposition_functionality(self):
        self.assertEqual(self.props[0].func, 'p and q')
        self.assertEqual(self.props[1].func, 'not s')
        self.assertEqual(self.props[2].func, 'p and q and r')
        self.assertEqual(self.props[3].func, '((p) and q) or (not t)')    
        self.assertEqual(self.props[4].func, '(((((p and q) or (not r)) and s) and t) or u) and ((not v) and (w and x))')
    
    def test_implication_functionality(self):
        assert self.imps[0].func == "not (" + self.props[0].func + ") or " + self.props[1].func \
                or '(not ' + self.props[1].func + ") or " + self.props[0].func \
                or '(not ' + self.props[1].func + ") or (" + self.props[0].func + ')', \
            "Implication class does not work correctly, should be " + "not (" + self.props[0].func + ") or (" + self.props[1].func + ')'

        assert self.imps[1].func == "not (" + self.props[2].func + ") or " + self.props[3].func \
                or '(not ' + self.props[3].func + ") or " + self.props[2].func \
                or '(not ' + self.props[3].func + ") or (" + self.props[2].func + ')', \
            "Implication class does not work correctly, should be " + "not (" + self.props[2].func + ") or (" + self.props[3].func + ')'

        assert self.imps[2].func == "not (" + self.props[4].func + ") or " + self.props[0].func \
                or '(not ' + self.props[0].func + ") or " + self.props[4].func \
                or '(not ' + self.props[0].func + ") or (" + self.props[4].func + ')', \
            "Implication class does not work correctly, should be " + "not (" + self.props[4].func + ") or (" + self.props[0].func + ')'

        assert self.imps[3].func == "not (" + self.props[1].func + ") or " + self.props[3].func \
                or '(not ' + self.props[3].func + ") or " + self.props[1].func \
                or '(not ' + self.props[3].func + ") or (" + self.props[1].func + ')', \
            "Implication class does not work correctly, should be " + "not (" + self.props[1].func + ") or (" + self.props[3].func + ')'

        assert self.imps[4].func == "not (" + self.props[1].func + ") or " + self.props[0].func \
                or '(not ' + self.props[0].func + ") or " + self.props[1].func \
                or '(not ' + self.props[0].func + ") or (" + self.props[1].func + ')', \
            "Implication class does not work correctly, should be " + "not (" + self.props[1].func + ") or (" + self.props[0].func + ')'

    def test_equivalence_functionality(self):
        assert self.eqs[1].func == "(not " + self.props[2].func + ") or " + self.props[3].func + " and " + self.props[2].func + " or (not " + self.props[3].func + ")" \
                    or "(not " + self.props[3].func + ") or " + self.props[2].func + " and " + self.props[3].func + " or (not " + self.props[2].func + ")", \
                "Equivalence class does not work correctly, should be " + "(not " + self.props[2].func + ") or " + self.props[3].func + " and " + self.props[2].func + " or (not " + self.props[3].func + ")" \
                    + "or " + "(not " + self.props[3].func + ") or " + self.props[2].func + " and " + self.props[3].func

        assert self.eqs[2].func == "(not " + self.props[4].func + ") or " + self.props[0].func + " and " + self.props[4].func + " or (not " + self.props[0].func + ")" \
                    or "(not " + self.props[0].func + ") or " + self.props[4].func + " and " + self.props[0].func + " or (not " + self.props[4].func + ")", \
                "Equivalence class does not work correctly, should be " + "(not " + self.props[4].func + ") or " + self.props[0].func + " and " + self.props[4].func + " or (not " + self.props[0].func + ")" \
                    + "or " + "(not " + self.props[0].func + ") or " + self.props[4].func + " and " + self.props[0].func

        assert self.eqs[3].func == "(not " + self.props[1].func + ") or " + self.props[3].func + " and " + self.props[1].func + " or (not " + self.props[3].func + ")" \
                    or "(not " + self.props[3].func + ") or " + self.props[1].func + " and " + self.props[3].func + " or (not " + self.props[1].func + ")", \
                "Equivalence class does not work correctly, should be " + "(not " + self.props[1].func + ") or " + self.props[3].func + " and " + self.props[1].func + " or (not " + self.props[3].func + ")" \
                    + "or " + "(not " + self.props[3].func + ") or " + self.props[1].func + " and " + self.props[3].func

        assert self.eqs[4].func == "(not " + self.props[1].func + ") or " + self.props[0].func + " and " + self.props[1].func + " or (not " + self.props[0].func + ")" \
                    or "(not " + self.props[0].func + ") or " + self.props[1].func + " and " + self.props[0].func + " or (not " + self.props[1].func + ")", \
                "Equivalence class does not work correctly, should be " + "(not " + self.props[1].func + ") or " + self.props[0].func + " and " + self.props[1].func + " or (not " + self.props[0].func + ")" \
                    + "or " + "(not " + self.props[0].func + ") or " + self.props[1].func + " and " + self.props[0].func

    def test_extract_variables_functionality(self):
        self.assertEqual(extract_variables(self.props[0]), {'p', 'q'})
        self.assertEqual(extract_variables(self.props[1]), {'s'})
        self.assertEqual(extract_variables(self.props[2]), {'p', 'q', 'r'})
        self.assertEqual(extract_variables(self.props[3]), {'p', 'q', 't'})
        self.assertEqual(extract_variables(self.props[4]), {'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x'})

        self.assertEqual(extract_variables(self.imps[0]), {'p', 'q', 's'})
        self.assertEqual(extract_variables(self.imps[1]), {'p', 'q', 'r', 't'})
        self.assertEqual(extract_variables(self.imps[2]), {'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x'})
        self.assertEqual(extract_variables(self.imps[3]), {'p', 'q', 's', 't'})
        self.assertEqual(extract_variables(self.imps[4]), {'p', 'q', 's'})

        self.assertEqual(extract_variables(self.eqs[0]), {'p', 'q', 's'})
        self.assertEqual(extract_variables(self.eqs[1]), {'p', 'q', 'r', 't'})
        self.assertEqual(extract_variables(self.eqs[2]), {'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x'})
        self.assertEqual(extract_variables(self.eqs[3]), {'p', 'q', 's', 't'})
        self.assertEqual(extract_variables(self.eqs[4]), {'p', 'q', 's'})
