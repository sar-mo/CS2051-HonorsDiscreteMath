# CS 2051 Spring 2023 - HW3 Supplement Part 1: Inference
# instructor: Gerandy Brito
# creator - Sarthak Mohanty

# author - your name here
# collaborators - list collaborators here

# NOTE(s):
# Propostional variables are denoted by a single lowercase letter [a-z] followed by an (optional) number, eg. p, q3, r22
# We strongly discourage the use of GitHub Copilot or ChatGPT to complete this assignment. It will be considered cheating (at least for this semester).

from logic_helper import *

def infer(inference_rules: list, conclusion: str):
    """Checks if a conclusion can be proved using given inference rules.
    
    Parameters:
        inference_rules: list of strings representing inference rules.
        conclusion: conclusion to prove.

    Returns: 
        True iff the conclusion can be proved using the given inference rules, False otherwise
    
    Examples:
        >>> infer(['p |implies| q', 'q |implies| r'], 'p |implies| r')
        True
        >>> infer(['p |implies| q', 'q |implies| r'], 'r |implies| p')
        False
    """
    # if no inference rules, return true if conclusion is a tautology
    if len(inference_rules) == 0:
        return all(val for _model, val in truth_table(conclusion))
    # else, create a big proposition checking if the conjunction of all the inference rules implies the conclusion
    inference = '((' + ') and ('.join(inference_rules) + f')) |implies| ({conclusion})'
    return all(val for _model, val in truth_table(inference))

