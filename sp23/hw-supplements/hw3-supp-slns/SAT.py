# CS 2051 Spring 2023
# HW3 Supplement Part 2: Satisfiability
# author - Sarthak Mohanty
# collaborators - N/A

# NOTE (s):
# You must use small single letters in [p-z] for your variable names followed by an (optional) number, eg. p, q3, r22
# we strongly discourage the use of GitHub Copilot or ChatGPT to complete this assignment. It will be considered cheating.

############## IMPLEMENT THE FOLLOWING FUNCTIONS  ##############
############## Do not modify function definitions ##############

from logic_helper import *

def brute_force_SAT_solver(proposition: str) -> dict:
    """Finds a satisfying assignment for a given set of clauses.
    
    Parameters:
        proposition: proposition to solve.
        
    Returns:
        A satisfying assignment for a given set of clauses, or None if no such assignment exists.
        
    Examples:
        >>> brute_force_SAT_solver((p or q) and ((not p) or (not q))
        {p: True, q: False}
    """
    for row in truth_table(proposition):
        if row[1]:
            return row[0]
    return None

def walkSAT_solver(proposition: str, p: float, maxFlips: int) -> dict:
    """Finds a satisfying assignment for a given set of clauses using the WalkSAT algorithm (see instructions for details)

    Parameters:
        proposition: proposition to solve.

    Returns:
        A satisfying assignment for a given set of clauses, or None if no such assignment exists.

    Examples:
        >>> walkSAT_solver((p or q) and ((not p) or (not q), 0.2)
        {p: True, q: False}
    """
    import random

    # start with a random assignment
    vars = extract_variables(proposition)
    random_assignment = { var: random.choice([True, False]) for var in vars }

    # perform maxFlips iterations:
    for _ in range(maxFlips):
        if evaluate(proposition, random_assignment.copy()):
            return random_assignment

        # find number of satisfying clauses and unsatisfied clauses
        unsatisfied_clauses = []
        satisfied_clauses = []
        for clause in proposition.split(' and '):
            if not evaluate(clause, random_assignment.copy()):
                unsatisfied_clauses.append(clause)
            else:
                satisfied_clauses.append(clause)

        # pick a random unsatisfied clause
        random_clause = random.choice(unsatisfied_clauses)
        clause_vars = extract_variables(random_clause)

        # with probability p, flip a random variable in the clause
        if random.random() < p:
            var = random.choice(clause_vars)
            random_assignment[var] = not random_assignment[var]

        # with probability 1-p, flip a variable in the clause which will result in the fewest previously satisfied clauses to be unsatisfied
        else:
            min_num_sat_to_unsat = float('inf')
            min_var = None
            for var in clause_vars:
                random_assignment[var] = not random_assignment[var] # flip the variable
                num_sat_to_unsat = 0
                for clause in satisfied_clauses:
                    if not evaluate(clause, random_assignment.copy()):
                        num_sat_to_unsat += 1
                if num_sat_to_unsat < min_num_sat_to_unsat:
                    min_num_sat_to_unsat = num_sat_to_unsat
                    min_var = var
                random_assignment[var] = not random_assignment[var] # unflip the variable
            random_assignment[min_var] = not random_assignment[min_var]
    return None


def pySAT_solver(proposition: str) -> list:
    """Finds a satisfying assignment for a given set of clauses using the pySAT_solver (see https://pysathq.github.io/ for details)
    
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

    # print(parsed)
    cnf = CNF(from_clauses= proposition)

    # create a SAT solver for this formula:
    with Solver(bootstrap_with=cnf) as solver:
        solver.solve()
        model = solver.get_model()
        return model