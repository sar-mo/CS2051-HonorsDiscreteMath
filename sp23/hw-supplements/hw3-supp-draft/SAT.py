# CS 2051 Spring 2023 - HW3 Supplement Part 2: Satisfiability
# instructor: Gerandy Brito
# creator - Sarthak Mohanty

# author - your name here
# collaborators - list collaborators here

# NOTE (s):
# You must use small single letters in [p-z] for your variable names followed by an (optional) number, eg. p, q3, r22
# We strongly discourage the use of GitHub Copilot or ChatGPT to complete this assignment. It will be considered cheating (at least for this semester).

from logic_helper import *
import random

def brute_force_SAT_solver(proposition: str) -> dict:
    """Finds a satisfying assignment for a given set of clauses.
    
    Parameters:
        proposition: proposition to solve.
        
    Returns:
        A satisfying assignment for a given set of clauses, or None if no such assignment exists.
        
    Examples:
        >>> brute_force_SAT_solver((p or q) and ((not p) or (not q)))
        {p: True, q: False}
    """
    for row in truth_table(proposition):
        if row[1]:
            return row[0]
    return None

def walkSAT_solver(proposition: str, p: float) -> dict:
    """Finds a satisfying assignment for a given set of clauses using the WalkSAT algorithm (see instructions for details).

    Parameters:
        proposition: proposition to solve.
        p: probability of flipping a random variable.

    Returns:
        A satisfying assignment for a given set of clauses, or None if no such assignment exists.

    Examples:
        >>> walkSAT_solver((p or q) and ((not p) or (not q)), 0.2)
        {p: True, q: False}
    """
    raise NotImplementedError

def pySAT_solver(proposition: str) -> list:
    """Finds a satisfying assignment for a given set of clauses using the PySAT library (see https://pysathq.github.io/ for details).
    
    Parameters:
        proposition: proposition to solve.
        
    Returns:
        A satisfying assignment for a given set of clauses, or None if no such assignment exists.
        
    Example:
        >>> pySAT_solver([1, 2], [-1, -2])
        [1, -2]
    """
    # the standard way to import PySAT:
    from pysat.formula import CNF
    from pysat.solvers import Solver

    # create a CNF object from the proposition:
    cnf = CNF(from_clauses= proposition)

    # create a SAT solver for this formula:
    with Solver(bootstrap_with=cnf) as solver:
        solver.solve()
        model = solver.get_model()
        return model
    