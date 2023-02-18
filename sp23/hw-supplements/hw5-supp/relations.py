# CS 2051 Spring 2023 - HW3 Supplement Parts 1-2: Relations
# instructor: Gerandy Brito
# creator - Sarthak Mohanty

# author - 
# collaborators - list collaborators here

def isReflexive(elements: list, relation: list) -> bool:
    '''Determines if a binary relation is reflexive. Should be done in one line.

    Parameters:
        elements: The domain of the relation.
        relation: A list of tuples (x, y) representing a binary relation.

    Returns:
        True if the relation is reflexive, False otherwise.

    Example:
        >>> isReflexive([(1, 2), (2, 4), (3, 4), (4, 5), (5, 6), (6, 1)])
        False
    '''

def isSymmetric(relation: list) -> bool:
    '''Determines if a binary relation is symmetric. Should be done in one line.

    Parameters:
        relation: A list of tuples (x, y) representing a binary relation.

    Returns:
        True if the relation is symmetric, False otherwise.

    Example:
        >>> isSymmetric([(1, 2), (2, 4), (3, 4), (4, 5), (5, 6), (6, 1)])
        False
    '''

def isAntiSymmetric(relation: list) -> bool:
    '''Determines if a binary relation is anti-symmetric. Should be done in one line.

    Parameters:
        relation: A list of tuples (x, y) representing a binary relation. 

    Returns:
        True if the relation is anti-symmetric, False otherwise.

    Example:
        >>> isAntiSymmetric([(1, 2), (2, 4), (3, 4), (4, 5), (5, 6), (6, 1)])
        True
    '''

def isTransitive(relation: list) -> bool:
    '''Determines if a binary relation is transitive. Should be done in one line.

    Parameters:
        relation: A list of tuples (x, y) representing a binary relation.

    Returns:
        True if the relation is transitive, False otherwise.

    Example:
        >>> isTransitive([(1, 2), (2, 4), (3, 4), (4, 5), (5, 6), (6, 1)])
        False
    '''

def isPartialOrder(elements: list, relation: list) -> bool:
    '''Determines if a binary relation is a partial order.

    Parameters:
        elements: The domain of the relation.
        relation: A list of tuples (x, y) representing a binary relation. Each tuple represents a pair of elements in the relation. The elements are assumed to be integers.

    Returns:
        True if the relation is a partial order, False otherwise.

    Example:
        >>> isPartialOrder([(1, 2), (2, 4), (3, 4), (4, 5), (5, 6), (6, 1)])
        False
    '''

def isEquivalenceRelation(elements: list, relation: list) -> bool:
    '''Determines if a binary relation is an equivalence relation.

    Parameters:
        elements: The domain of the relation.
        relation: A list of tuples (x, y) representing a binary relation. Each tuple represents a pair of elements in the relation. The elements are assumed to be integers.

    Returns:
        True if the relation is an equivalence relation, False otherwise.

    Example:
        >>> isEquivalenceRelation([(1, 2), (2, 4), (3, 4), (4, 5), (5, 6), (6, 1)])
        False
    '''

def partition(elements: list, equiv_relation: bool) -> list[set]: 
    '''Partitions a set of elements into equivalence classes.

    Parameters:
        elements: The domain of the relation.
        equiv_relation: A boolean function that takes two elements and returns True if they are in the same equivalence class.

    Returns:
        A list of sets, where each set is an equivalence class.

    Example:
        >>> partition([1, 2, 3, 4, 5, 6], lambda x, y: x % 2 == y % 2)
        [{1, 3, 5}, {2, 4, 6}]
    '''