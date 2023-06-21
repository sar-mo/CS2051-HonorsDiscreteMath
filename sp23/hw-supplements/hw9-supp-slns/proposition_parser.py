# CS 2051 Spring 2023 - HW9 Supplement Part 1: (Optional) Introduction to Recursion
# instructor: Gerandy Brito
# creator - Sarthak Mohanty

# author - Sarthak Mohanty
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

    # convert the string into a list of tokens
    proposition = proposition.replace('(', ' ( ').replace(')', ' ) ') 
    tokens = proposition.split()

    def parse_tokens(tokens):

        # current implementation has time complexity O(n^2), could be improved to O(n)
        def trim_extra_tokens(tokens):
            if tokens[0] == '(' and tokens[-1] == ')':
                # Check if the remaining tokens are balanced
                balanced_factor = 0
                for i in range(1, len(tokens) - 1):
                    if tokens[i] == '(':
                        balanced_factor += 1
                    elif tokens[i] == ')':
                        balanced_factor -= 1
                    elif balanced_factor < 0:
                        break
                # if the parentheses are balanced, then remove the extra parentheses
                if balanced_factor == 0:
                    return trim_extra_tokens(tokens[1:-1])
            return tokens

        # remove extra spaces from the beginning and end of the string
        tokens = trim_extra_tokens(tokens)

        # if the formula is an atomic proposition
        if len(tokens) == 1:
            return Formula(tokens[0])
        # if the formula starts with a unary operator
        if tokens[0] == 'not':
            return Formula(tokens[0], parse_tokens(tokens[1:]))
        
        # if the formula is a binary operation
        binary_operators = ['and', 'or', 'implies', 'iff']
        open_parentheses_count = 0
        close_parentheses_count = 0
        for i, token in enumerate(tokens):
            if token == '(':
                open_parentheses_count += 1
            elif token == ')':
                close_parentheses_count += 1
            elif token in binary_operators:
                # if the binary operator is at the top level (i.e., not nested within parentheses)
                if open_parentheses_count == close_parentheses_count:
                    return Formula(tokens[i], parse_tokens(tokens[:i]), parse_tokens(tokens[i+1:]))
        
        raise ValueError("Invalid formula")
        
    return parse_tokens(tokens)

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
    formula = parse(proposition)

    def evaluate_helper(formula: Formula, model: set) -> bool:
        if formula.root == 'not':
            return not evaluate_helper(formula.first, model)
        elif formula.root == 'and':
            return evaluate_helper(formula.first, model) and evaluate_helper(formula.second, model)
        elif formula.root == 'or':
            return evaluate_helper(formula.first, model) or evaluate_helper(formula.second, model)
        elif formula.root == 'implies':
            return (not evaluate_helper(formula.first, model)) or evaluate_helper(formula.second, model)
        elif formula.root == 'iff':
            return evaluate_helper(formula.first, model) == evaluate_helper(formula.second, model)
        elif formula.root == 'True':
                return True
        elif formula.root == 'False':
            return False
        else:
            return model[formula.root]
    
    return evaluate_helper(formula, model)