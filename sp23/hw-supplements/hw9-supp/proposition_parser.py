# CS 2051 Spring 2023 - HW9 Supplement Part 1: (Optional) Introduction to Recursion
# instructor: Gerandy Brito
# creator - Sarthak Mohanty

# author - your name here
# collaborators - N/A

from typing import Optional, TypeVar

Formula = TypeVar('Formula')

class Formula:
    """An immutable propositional formula in tree representation, composed from
    variable names, and operators applied to them.
    Attributes:
    root: the constant, variable name, or operator at the root of the
    formula tree.
    first: the first operand of the root, if the root is a unary or binary
    operator.
    second: the second operand of the root, if the root is a binary
    operator.
    """
    root: str
    first: Optional[Formula]
    second: Optional[Formula]

    def __init__(self, root: str, first: Optional[Formula] = None, second: Optional[Formula] = None):
        """Initializes a `Formula` from its root and root operands.
        Parameters:
        root: the root for the formula tree.
        first: the first operand for the root, if the root is a unary or
        binary operator.
        second: the second operand for the root, if the root is a binary
        operator.
        """

def parse(string: str) -> Formula:
    """Parses the given valid string representation into a formula.

    Parameters:
    string: string to parse.

    Returns:
    A formula whose standard string representation is the given string.
    """
    
def evaluate(formula: Formula, model: set) -> bool:
    """Calculates the truth value of the given formula in the given model.

    Parameters:
        formula: formula to calculate the truth value of.
        model: model over (possibly a superset of) the variables of the formula,
            to calculate the truth value in.

    Returns:
        The truth value of the given formula in the given model.
    """