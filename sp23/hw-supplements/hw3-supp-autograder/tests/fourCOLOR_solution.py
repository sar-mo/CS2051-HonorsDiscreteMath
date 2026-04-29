# CS 2051 Spring 2023
# HW3 Supplement Part 3: Reductions
# creator - Sarthak Mohanty
# author - your name here
# collaborators - put any names of collaborators here

# NOTE (s):
# You must use small single letters in [p-z] for your variable names, eg. p, q, r
# we strongly discourage the use of GitHub Copilot or ChatGPT to complete this assignment. It will be considered cheating.

######## Do not modify the following block of code ########
# ********************** BEGIN *******************************

import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d
import random
import SAT

random.seed(2023)
SIZE = 1

def isPointInRegion(point):
    '''Returns True if the point is in the region, False otherwise. the point is in the region, False otherwise.'''
    return point[0] > 0 and point[0] < SIZE and point[1] > 0 and point[1] < SIZE

def drawBlankVoronoiDiagram(num_points = 15):
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
        Here there are 4 regions, 0 is neighbor to 1, 2, and 3, 1 is neighbor to 0, 2, and 3, etc
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

def colorMap(vor: Voronoi) -> None:
    '''Colors the map according to the 4COLOR solution.'''
    neighbors = getNeighbors(vor)
    prop = fourColoringToSAT(neighbors)

    ## Magic SAT Solver
    parsed_prop, vars = parse_proposition(prop)
    solution = SAT.pySAT_solver(parsed_prop)
    solution = repackaged_model(solution, vars)

    # solution = SAT.walkSAT_solver(prop, 0.2)

    for variable, value in solution.items():
        if value:
            region = int(variable[1:])
            polygon = [vor.vertices[i] for i in vor.regions[vor.point_region[region]]]
            plt.fill(*zip(*polygon), alpha=0.4, color=variable[0])

# ********************** END *******************************

############## IMPLEMENT THE FOLLOWING FUNCTION  ##############
############## Do not modify function definitions ##############


def fourColoringToSAT(neighbors: list) -> str:
    '''Returns a SAT problem that is equivalent to the 4-coloring problem
    NOTE: make sure you use the variable names ri, bi, gi, yi! The code will not work otherwise.

    Parameters:
        neighbors: A list of tuples, where the first element is the index of the region and the second element is a list of the neighboring regions.
    
    Returns:
        A SAT problem that is equivalent to the 4-coloring problem.
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

    assignment = fourColoringToSAT(getNeighbors(drawBlankVoronoiDiagram()))

    vor = drawBlankVoronoiDiagram(num_points=100)
    plt.savefig('blank_map.pdf')
    print('blank map generated')
    
    colorMap(vor)
    print('colors assigned')
    plt.savefig('colored_map.pdf')
    print('colored map generated')


