# CS 2051 Spring 2023 - HW3 Supplement Parts 3-4: Scheduling
# instructor: Gerandy Brito
# creator - Sarthak Mohanty

# author - 
# collaborators - list collaborators here


def topological_sort(poset):
    """Returns a topological sort of the given poset using a modified version of Kahn's algorithm.
    
    Parameters:
        poset: A list of tuples (x, y) representing a binary relation.
        
    Returns:
        A list of elements in topological order.
        
    Example:
    >>> topological_sort([(1, 2), (2, 4), (3, 4), (4, 5), (5, 6)])
    [1, 3, 2, 4, 5, 6]
    """

def generate_schedule(poset, num_processors):
    """Returns an optimal schedule for the given poset using the given number of processors.
    
    Parameters:
        poset: A list of tuples (x, y) representing a binary relation.
        num_processors: The number of processors available
        
    Returns:
        A list of lists of elements representing the schedule.

    Example:
    >>> optimal_scheduling([(1, 2), (2, 4), (3, 4), (4, 5), (5, 6)], 2)
    [[1, 3], [2], [4], [5], [6]]
    """
