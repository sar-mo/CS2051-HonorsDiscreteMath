# CS 2051 Spring 2023 - HW3 Supplement Parts 3-4: Scheduling
# instructor: Gerandy Brito
# creator - Sarthak Mohanty

# author - Sarthak Mohanty
# collaborators - N/A


def topological_sort(elements, poset):
    """Returns a topological sort of the given poset using a modified version of Kahn's algorithm.
    
    Parameters:
        poset: A set of tuples (x, y) representing a binary relation.
        
    Returns:
        A list of elements in topological order.
        
    Example:
    >>> topological_sort({(1, 2), (2, 4), (3, 4), (4, 5), (5, 6)})
    [1, 3, 2, 4, 5, 6]
    """

    result = []
    def is_minimal(element):
        return all((element != v) or (u in result) for u, v in poset)

    minimal = set(element for element in elements if is_minimal(element))
    while minimal:
        u = minimal.pop()
        result.append(u)
        u_dependencies = (v for _u, v in poset if u == _u)
        for v in u_dependencies:
            if is_minimal(v):
                minimal.add(v)
    return result

def generate_schedule(elements, poset, num_processors):
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
    root_distance = {e: 0 for e in elements}
    for element in topological_sort(elements, poset)[::-1]:
        for u, v in poset:
            if v == element:
                root_distance[u] = root_distance[v] + 1
    
    removed = set()
    def is_minimal(element):
        return all((element != v) or (u in removed) for u, v in poset)
    
    def sort_key(element):
        return root_distance[element]

    result = []
    minimal = sorted((element for element in elements if is_minimal(element)), key=sort_key)
    while minimal:
        cur_removed = []
        while minimal and len(cur_removed) < num_processors:
            cur_removed.append(minimal.pop())
        result.append(cur_removed)
        removed.update(cur_removed)
        
        u_dependencies = set(v for u, v in poset if u in cur_removed)
        for v in u_dependencies:
            if is_minimal(v):
                minimal.append(v)
        minimal.sort(key=sort_key)
    return result