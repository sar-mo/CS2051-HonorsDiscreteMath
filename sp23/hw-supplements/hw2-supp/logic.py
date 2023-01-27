# CS 2051 Spring 2023
# HW2 Supplement - Logic Playground
# creator - Sarthak Mohanty
# collaborators - N/A

# NOTE (s):
# You must use small single letters in [p-z] for your variable names, eg. p, q, r
# we strongly discourage the use of GitHub Copilot or ChatGPT to complete this assignment. It will be considered cheating.

######## Do not modify the following block of code ########
# ********************** BEGIN *******************************

from functools import partial
import re

class Infix(object):
    def __init__(self, func):
        self.func = func
    def __or__(self, other):
        return self.func(other)
    def __ror__(self, other):
        return Infix(partial(self.func, other))
    def __call__(self, v1, v2):
        return self.func(v1, v2)

@Infix
def implies(p, q):
    return (not p) or q

@Infix
def iff(p, q):
    return (p |implies| q) and (q |implies| p)


def extract_variables(proposition: str) -> list:
    """Extracts variables from a proposition.

    Parameters:
        proposition: The proposition to extract variables from.
    
    Returns:
        A sorted list of variables in the proposition.

    Example:
        >>> extract_variables("p and q")
        ['p', 'q']
    """
    return sorted(set(re.findall(r'\b[a-z]\b', proposition)))

def evaluate(proposition: str, model: dict) -> bool:
    """Evaluates a proposition given a model.

    Parameters:
        proposition: The proposition to evaluate.
        model: A dictionary mapping variables to their assignments.

    Returns:
        The truth value of the proposition.

    Example:
        >>> evaluate("p and (q |implies| r)", {'p': True, 'q': False, 'r': True}
        True
    """
    model['iff'] = iff
    model['implies'] = implies
    return eval(proposition, model)

def truth_table(proposition: str) -> list:
    """Generates a truth table for a given proposition.

    Parameters:
        proposition: The proposition to generate a truth table for.
    
    Returns:
        A truth table as a list of tuples (dictionary, bool).

    Example:
        >>> truth_table("p and q")
        [({'p': True, 'q': True}, True), 
         ({'p': True, 'q': False}, False), 
         ({'p': False, 'q': True}, False), 
         ({'p': False, 'q': False}, False)]
    
    """
    variables = extract_variables(proposition)
    truth_table = []

    # generate all possible combinations of variables
    for i in range(2**len(variables)):
        row = {}
        for j in range(len(variables)):
            row[variables[j]] = (i >> j) % 2 == 1
        truth_table.append(row)

    # evaluate the proposition for each combination of variables
    for i in range(len(truth_table)):
        val = evaluate(proposition, truth_table[i].copy())
        truth_table[i] = (truth_table[i], val)
    return truth_table

# *********************** END ***************************


############## IMPLEMENT THE FOLLOWING FUNCTIONS  ##############
############## Do not modify function definitions ##############

def count_satisfying(proposition: str) -> int:
    """Count the number of satisfying models in a proposition.
        
    Parameters:
        proposition: proposition to count the number of satisfying models for.
        
    Returns:
        The number of satisfying models in the proposition.
        
    Examples:
        >>> count_satisfying('p and q')
        1
        >>> count_satisfying('p or q')
        3
    """

def are_equivalent(prop1: str, prop2: str) -> bool:
    """Checks if two propositions are logically equivalent.
        
    Parameters:
        prop1: first proposition to check.
        prop2: second proposition to check.
        
    Returns:
        True if the propositions are logically equivalent, False otherwise.
        
    Examples:
        >>> are_equivalent('p |implies| q', '(not p) or q')
        True
        >>> are_equivalent('p and q', '(not p) or q')
        False
    """

def is_tautology(proposition: str) -> bool:
    """Checks if a proposition is a tautology.
        
    Parameters:
        proposition: proposition to check.
        
    Returns:
        True if the proposition is a tautology, False otherwise.
        
    Examples:
        >>> is_tautology('p |implies| q')
        False
        >>> is_tautology('(not p) |implies| (p or (not p))')
        True
    """

def is_contradiction(proposition: str) -> bool:
    """Checks if a proposition is a contradiction.
        
    Parameters:
        proposition: proposition to check.
        
    Returns:
        True if the proposition is a contradiction, False otherwise.
        
    Examples:
        >>> is_contradiction('p |implies| q')
        False
        >>> is_contradiction('p and (not p)')
        True
    """

def is_contingency(proposition: str) -> bool:
    """Checks if a proposition is a contingency.
        
    Parameters:
        proposition: proposition to check.
        
    Returns:
        True if the proposition is a contingency, False otherwise.
        
    Examples:
        >>> is_contingency('p |implies| q')
        True
        >>> is_contingency('p and (not p)')
        False
    """

def model_fitting(truth_table: list) -> str:
    """Fits a proposition to a truth table.
        
    Parameters:
        truth_table: truth table to fit a proposition to.
        
    Returns:
        A string representing the proposition.
        
    Examples: 
        None, try to think of some yourself!
    
    Note: 
        If the truth table is of the form {{}, True}, then return 'True'. 
        If the truth table is of the form {{}, False}, then return 'False'.
    """

# *********************** END ***************************