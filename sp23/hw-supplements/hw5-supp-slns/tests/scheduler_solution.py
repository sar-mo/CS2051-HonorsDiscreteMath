# CS 2051 Spring 2023 - HW3 Supplement Parts 3-4: Scheduling
# instructor: Gerandy Brito
# creator - Sarthak Mohanty

# author - Sarthak Mohanty
# collaborators - N/A


def topological_sort(elements: set, poset: set) -> list:
    """Returns a topological sort of the given poset using a modified version of Kahn's algorithm.
    
    Parameters:
        elements: The domain of the relation.
        poset: A set of tuples (x, y) representing a binary relation.
        
    Returns:
        A list of elements in topological order.
        
    Example:
    >>> topological_sort({1, 2, 3, 4, 5, 6}, {(1, 2), (2, 4), (3, 4), (4, 5), (5, 6)})
    [1, 3, 2, 4, 5, 6]
    """

    result = []
    
    def is_minimal(element):
        return all(element != v for _u, v in poset)

    min_elements = set(element for element in elements if is_minimal(element))
    while min_elements:
        u = min_elements.pop()
        result.append(u)

        # list of all elements that depend on u
        u_dependencies = [v for _u, v in poset if _u == u]

        for v in u_dependencies:
            # check if all dependencies of v are in result
            if all(u in result for u, _v in poset if _v == v):
                min_elements.add(v)
    
    return result

def generate_schedule(elements: set, poset: set, num_processors: int) -> list[list]:
    """Returns an optimal schedule for the given poset using the given number of processors.
    
    Parameters:
        elements: The domain of the relation.
        poset: A set of tuples (x, y) representing a binary relation.
        num_processors: The number of processors available
        
    Returns:
        A list of lists of elements representing the schedule.

    Example:
    >>> optimal_scheduling({1, 2, 3, 4, 5, 6}, {(1, 2), (2, 4), (3, 4), (4, 5), (5, 6)}, 2)
    [[1, 3], [2], [4], [5], [6]]
    """

    scheduled_tasks = set()
    schedule = list()

    # Compute the height of each element
    heights = { x: 0 for x in elements }
    for x in topological_sort(elements, poset)[::-1]:
        dependents = [ v for _u, v in poset if _u == x ]
        if dependents:
            heights[x] = 1 + max(heights[y] for y in dependents)
 
    while(len(scheduled_tasks) != len(elements)):
        tasks = []
        
        # Look at all elements in the poset and check if they are not in scheduled_tasks
        # and if they are not dependent on any elements in scheduled_tasks
        tasks = [v for v in elements if v not in scheduled_tasks\
                 and all(u in scheduled_tasks for u, _v in poset if _v == v)]

        # Sort the elements by their depth in the poset
        tasks = sorted(tasks, key=lambda x: heights[x], reverse=True)

        # Take the first num_processors elements
        tasks = tasks[:num_processors]

        # Add the elements in tasks to scheduled_tasks
        scheduled_tasks = scheduled_tasks.union(tasks)

        schedule += [tasks]
    
    return schedule