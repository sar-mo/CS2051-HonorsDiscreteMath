# CS 2051 Spring 2023 - HW9 Supplement Part 1: (Optional) Introduction to Recursion
# instructor: Gerandy Brito
# creator - Sarthak Mohanty

# author - your name here
# collaborators - N/A

# NOTE: Assume all formulas are valid

from typing import Optional, TypeVar

Formula = TypeVar('Formula')

class Formula:
    """An propositional formula in tree representation, composed from
    variable names, and operators applied to them."""
    root: str
    first: Optional[Formula]
    second: Optional[Formula]

    def __init__(self, root: str, first: Optional[Formula] = None, second: Optional[Formula] = None):
        """Initializes a `Formula` from its root and root operands.

        Parameters:
            root: the root for the formula tree.
            first: the first operand for the root, if the root is a unary or binary operator.
            second: the second operand for the root, if the root is a binary operator.
        """
        self.root = root
        self.first = first
        self.second = second

    def __repr__(self) -> str:
        """Computes a comprehensive object-based representation of the formula."""
        if self.first is None:
            return f"Formula('{self.root}')"
        elif self.second is None:
            return f"Formula('{self.root}', {repr(self.first)})"
        else:
            return f"Formula('{self.root}', {repr(self.first)}, {repr(self.second)})"

    def __str__(self) -> str:
        """Computes a human-readable string representation of the formula."""
        if self.first is None:  # root is a variable
            return self.root
        elif self.second is None:  # root is a unary operator
            return f'({self.root} {str(self.first)})'
        else:  # root is a binary operator
            return f'({str(self.first)} {self.root} {str(self.second)})'


def parse(proposition: str) -> Formula:
    """Parses the given valid string representation into a formula.

    Parameters:
        string: string to parse.

    Returns:
        A Formula object representing the given string.

    Example:
        >>> parse('p and ( (not p) or q)')
        Formula('and', Formula('p'), Formula('or', Formula('not', Formula('p')), Formula('q')))
        >>> parse('p and q and (r)')
        Formula('and', Formula('p'), Formula('and', Formula('q'), Formula('r')))
    """
    raise NotImplementedError

def evaluate(proposition: str, model: set) -> bool:
    """Calculates the truth value of the given formula in the given model.
    Should work exactly like the built-in function `eval`, as well as support
    the additional operators `implies` and `iff`.

    Parameters:
        formula: formula to calculate the truth value of.
        model: model over (possibly a superset of) the variables of the formula,
            to calculate the truth value in.

    Returns:
        The truth value of the given formula in the given model.

    Example:
        >>> evaluate('p and ((not p) or q)', {'p': True, 'q': False})
        False
        >>> evaluate('p implies r', {'p': True, 'r': True})
        True
    """
    raise NotImplementedError