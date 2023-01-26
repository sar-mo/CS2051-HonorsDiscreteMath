
# This file contains helper functions for the logic homework.
# Do not modify this file.

from functools import partial, cache
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


def extract_variables(proposition: str):
    """Extracts variables from a proposition.

    Parameters:
        proposition: The proposition to extract variables from.
    
    Returns:
        A sorted list of variables in the proposition.

    Example:
        >>> extract_variables("p0 and q2")
        ['p0', 'q2']
    """
    return sorted(set(re.findall(r'\b[a-z][0-9]*\b', proposition)))

def evaluate(proposition: str, model: dict):
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

@cache
def truth_table(proposition: str):
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
