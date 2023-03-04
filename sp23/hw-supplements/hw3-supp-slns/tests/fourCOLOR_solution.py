# CS 2051 Spring 2023 - HW3 Supplement Part 3: Reductions
# instructor: Gerandy Brito
# creator - Sarthak Mohanty

# author - your name here
# collaborators - list collaborators here

# NOTE (s):
# You must use small single letters in [p-z] for your variable names followed by an (optional) number, eg. p, q3, r22
# We strongly discourage the use of GitHub Copilot or ChatGPT to complete this assignment. It will be considered cheating (at least for this semester).

import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d
import random
import SAT as SAT

from logic_helper import *

random.seed(2023)
SIZE = 1

def isPointInRegion(point):
    '''Returns True if the point is in the region, False otherwise. the point is in the region, False otherwise.'''
    return point[0] > 0 and point[0] < SIZE and point[1] > 0 and point[1] < SIZE

def drawBlankVoronoiDiagram(num_points = 15):
    '''Draws a blank Voronoi diagram with the given number of points.'''
    # make up data points
    points = np.random.rand(num_points, 2)

    # add 4 distant dummy points
    points = np.append(points, [[999,999], [-999,999], [999,-999], [-999,-999]], axis = 0)

    # compute Voronoi tesselation
    vor = Voronoi(points)

    # plot it
    voronoi_plot_2d(vor, show_vertices=False, show_points = False, line_colors='black', line_width=5/len(points)**(1/3), line_alpha=0.8)
    for i in range(len(points)):
        plt.text(points[i][0], points[i][1], str(i), fontsize=200/len(points))

    # # fix the range of axes
    plt.xlim([0,SIZE]), plt.ylim([0,SIZE])

    # remove the axis numbers
    plt.xticks([]), plt.yticks([])

    return vor

def getNeighbors(vor):
    """ 
    Returns a list of tuples, where the first element is the index of the region and the second element is a list of the neighboring regions.
    Example:
        [(0, [1, 2, 3]), (1, [0, 2, 3]), (2, [0, 1, 3]), (3, [0, 1, 2])]. 
        (Here there are 4 regions. Region 0 is neighbor to 1, 2, and 3, 1 is neighbor to 0, 2, and 3, etc)
    """
    points = vor.points
    regions = vor.regions
    neighbors = []
    for i in range(len(points)):
        neighbors.append((i, []))
        for j in range(len(points)):
            region1 = regions[vor.point_region[i]]
            region2 = regions[vor.point_region[j]]
            if i != j:
                if intersection := set(region1).intersection(set(region2)):
                    corresponding_points = [vor.vertices[i] for i in intersection]
                    if not all([not isPointInRegion(p) for p in corresponding_points]):
                        neighbors[i][1].append(j)
    # remove the dummy points
    neighbors = neighbors[:-4]
    return neighbors

def parse_proposition(proposition: str):
    """Parses a proposition in CNF into the form accepted by a production level SAT solver (pySAT).
    
    Example:
        >>> parse_proposition('(r1 or r2) and (r1 or r3) and (r2 or r3) and (not r1 or not r2) and (not r1 or not r3) and (not r2 or not r3)')
        ([[1, 2], [1, 3], [2, 3], [-1, -2], [-1, -3], [-2, -3]], {1, 2, 3})
    """
    cnf = []
    var = set()
    color_mapping = {'r': '1', 'b': '2', 'g': '3', 'y': '4'}
    clauses = proposition.split(' and ')
    for clause in clauses:
        cnf_clause = []
        clause = clause[1:-1] # remove the parentheses
        literals = clause.split(' or ')
        for literal in literals:
            is_negative = 1
            literal = literal.replace('(', '').replace(')', '')
            if literal[0:3] == 'not':
                is_negative = -1
                literal = literal.replace('not ', '')
            literal = color_mapping[literal[0]] + literal[1:]
            var.add(int(str(literal)))
            cnf_clause.append(is_negative * int(str(literal)))
        cnf.append(cnf_clause)
    return cnf, var

def repackaged_model(model, vars):
    """Parses the output created by a production level SAT solver (pySAT) to a human-readable format."""
    new_model = {}
    color_mapping = {'r': '1', 'b': '2', 'g': '3', 'y': '4'}
    for val in model:
        if abs(val) in vars:
            val = str(val)
            if val[0] == '-':
                val = list(color_mapping.keys())[list(color_mapping.values()).index(val[1])] + val[2:]
                new_model[val] = False
            else:
                val = list(color_mapping.keys())[list(color_mapping.values()).index(val[0])] + val[1:]
                new_model[val] = True
    return new_model

def colorMap(vor: Voronoi, solver) -> None:
    '''Colors the map according to the 4COLOR solution.'''
    neighbors = getNeighbors(vor)
    prop = fourColoringToSAT(neighbors)

    # solve the SAT problem
    if solver == SAT.pySAT_solver:
        parsed_prop, vars = parse_proposition(prop)
        solution = SAT.pySAT_solver(parsed_prop)
        solution = repackaged_model(solution, vars)
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


def fourColoringToSAT(neighbors: list) -> str:
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