# CS 2051 Spring 2023 - HW3 Supplement Part 3: Reductions
# instructor: Gerandy Brito
# creator - Sarthak Mohanty

# author - your name here
# collaborators - list collaborators here

# NOTE(s):
# Propostional variables are denoted by a single lowercase letter [a-z] followed by an (optional) number, eg. p, q3, r22.
# We strongly discourage the use of GitHub Copilot or ChatGPT to complete this assignment. It will be considered cheating (at least for this semester).

import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d
import random
import SAT

random.seed(2023)
SIZE = 1
DUMMY_POINTS = [[999, 999], [-999, 999], [999, -999], [-999, -999]] # used to ensure that all regions are bounded

# ********************** Helper functions, DO NOT MODIFY ********************** #

def is_point_in_region(point):
    '''Returns True if the point is in the region, False otherwise.'''
    x, y = point
    return 0 < x < SIZE and 0 < y < SIZE

def draw_blank_voronoi_diagram(num_points=15):
    '''Draws a blank Voronoi diagram with the given number of points.'''

    points = np.append(np.random.rand(num_points, 2), DUMMY_POINTS, axis=0)
    
    vor = Voronoi(points)

    voronoi_plot_2d(vor, show_vertices=False, show_points=False, line_colors='black', line_width=5/len(points)**(1/3), line_alpha=0.8)
    for i, point in enumerate(points):
        plt.text(*point, str(i), fontsize=200/len(points))

    plt.xlim([0, SIZE]), plt.ylim([0, SIZE])  # fix the range of axes
    plt.xticks([]), plt.yticks([])  # remove the axis numbers

    return vor

def get_neighbors(vor):
    """ 
    Returns a list of tuples, where the first element is the index of the region and the second element is a list of the neighboring regions.
    Example:
        [(0, [1, 2, 3]), (1, [0, 2, 3]), (2, [0, 1, 3]), (3, [0, 1, 2])]. 
        (Here there are 4 regions. Region 0 is neighbor to 1, 2, and 3, 1 is neighbor to 0, 2, and 3, etc)
    """
    points = vor.points
    regions = vor.regions
    neighbors = [(i, []) for i in range(len(points))]

    # if there are only 2 points, then they are neighbors
    if len(points) - len(DUMMY_POINTS) == 2:
        neighbors[0][1].append(1)
        neighbors[1][1].append(0)
        return neighbors[:-len(DUMMY_POINTS)]

    for i in range(len(points)):
        for j in range(len(points)):
            if i != j:
                region1 = set(regions[vor.point_region[i]])
                region2 = set(regions[vor.point_region[j]])
                intersection = region1.intersection(region2)
                if intersection and any(is_point_in_region(vor.vertices[i]) for i in intersection):
                    neighbors[i][1].append(j)

    return neighbors[:-len(DUMMY_POINTS)] # remove the dummy points

def convert_proposition_to_pySAT_format(proposition: str):
    """Parses a proposition in CNF into the form accepted by a production level SAT solver (pySAT)."""
    color_mapping = {'r': '1', 'b': '2', 'g': '3', 'y': '4'}
    
    def process_literal(literal):
        """Process a literal and return its integer representation."""
        is_negative = -1 if literal.startswith('not ') else 1
        literal = literal.replace('not ', '')
        return is_negative * int(color_mapping[literal[0]] + literal[1:])

    cnf = []
    for clause in proposition.split(' and '):
        literals = clause[1:-1].split(' or ')  # remove parentheses and split on ' or '
        processed_literals = [process_literal(lit) for lit in literals]
        cnf.append(processed_literals)

    return cnf

def convert_pySAT_output_to_colorMap_format(model, vars):
    """Parses the output created by a production level SAT solver (pySAT) to the form accepted by colorMap."""
    new_model = {}
    color_mapping = {'r': '1', 'b': '2', 'g': '3', 'y': '4'}
    reversed_color_mapping = {v: k for k, v in color_mapping.items()}

    for val in model:
        if abs(val) in vars:
            color_number = str(abs(val))
            color, number = reversed_color_mapping[color_number[0]], color_number[1:]
            new_model[color + number] = val > 0

    return new_model

def color_map(vor: Voronoi, solver) -> None:
    '''Colors the map according to the 4COLOR solution.'''
    neighbors = get_neighbors(vor)
    prop = fourCOLOR_to_SAT(neighbors)

    # solve the SAT problem
    if solver == SAT.pySAT_solver:
        parsed_prop = convert_proposition_to_pySAT_format(prop)
        vars = set([abs(lit) for clause in parsed_prop for lit in clause])
        solution = SAT.pySAT_solver(parsed_prop)
        solution = convert_pySAT_output_to_colorMap_format(solution, vars)
    elif solver == SAT.walkSAT_solver:
        solution = solver(prop, 1, 10000)
    else:
        solution = solver(prop)

    # plot the solution
    for variable, value in solution.items():
        if value:
            region = int(variable[1:])
            polygon = [vor.vertices[i] for i in vor.regions[vor.point_region[region]]]
            plt.fill(*zip(*polygon), alpha=0.4, color=variable[0])

# ********************** END *******************************

def fourCOLOR_to_SAT(neighbors: list) -> str:
    '''Returns a SAT problem that is equivalent to the 4-coloring problem.
    NOTE: make sure you use the variable names r0, b0, g0, y0, r1, b1, ...,  etc.! The code will not work otherwise.

    Parameters:
        neighbors: A list of tuples, where the first element is the index of the region and the second element is a list of the neighboring regions.
    
    Returns:
        A SAT problem that is equivalent to the 4-coloring problem.

    Example:
        >>> fourColoringToSAT([(0, [1, 2]), (1, [0]), (2, [0])])
        "(r0 or b0 or g0 or y0) and (not r0 or not b0) and (not r0 or not g0) and (not r0 or not y0) and (not b0 or not g0)
        and (not b0 or not y0) and (not g0 or not y0) and (not r0 or not r1) and (not b0 or not b1) and (not g0 or not g1)
        and (not y0 or not y1) and (not r0 or not r2) and (not b0 or not b2) and (not g0 or not g2) and (not y0 or not y2)
        and (r1 or b1 or g1 or y1) and (not r1 or not b1) and (not r1 or not g1) and (not r1 or not y1) and (not b1 or not g1)
        and (not b1 or not y1) and (not g1 or not y1) and (not r1 or not r0) and (not b1 or not b0) and (not g1 or not g0)
        and (not y1 or not y0) and (r2 or b2 or g2 or y2) and (not r2 or not b2) and (not r2 or not g2) and (not r2 or not y2)
        and (not b2 or not g2) and (not b2 or not y2) and (not g2 or not y2) and (not r2 or not r0) and (not b2 or not b0)
        and (not g2 or not g0) and (not y2 or not y0)"
    '''
    prop = ''
    for i in range(len(neighbors)):
        # ensure at least one of the four colors is chosen
        prop += f'(r{i} or b{i} or g{i} or y{i}) and '
        # for every pair of colors, we ensure that they are not both chosen
        prop += f'(not r{i} or not b{i}) and (not r{i} or not g{i}) and (not r{i} or not y{i}) and (not b{i} or not g{i}) and (not b{i} or not y{i}) and (not g{i} or not y{i}) and '
        # for every pair of neighboring regions, we ensure that they are not both the same color
        for j in neighbors[i][1]:
            prop += f'(not r{i} or not r{j}) and (not b{i} or not b{j}) and (not g{i} or not g{j}) and (not y{i} or not y{j}) and '
    return prop[:-5] # remove the last 'and '

if __name__ == "__main__":
    vor = draw_blank_voronoi_diagram(num_points=20)
    print(get_neighbors(vor))
    plt.savefig('blank_map.pdf')
    print('blank map generated')
    
    color_map(vor, solver=SAT.pySAT_solver)
    print('colors assigned')
    plt.savefig('colored_map.pdf')
    print('colored map generated')