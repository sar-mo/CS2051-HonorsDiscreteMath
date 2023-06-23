# CS 2051 Spring 2023 - HW7 Supplement Parts 2-3: Elliptic Curves
# instructor: Gerandy Brito
# creator - Sarthak Mohanty

# author - Sarthak Mohanty
# collaborators - N/A

import math
import matplotlib.pyplot as plt
import numpy as np

def f(x : int, a : int, b : int) -> tuple:
    '''Compute the y-value(s) of a point on an elliptic curve given in Weierstrass form.

    Parameters:
        x : The x-value of the point.
        a : The a coefficient of the curve.
        b : The a coefficient of the curve.

    Returns:
        The positive and negative y-values of the point. If the point doesn't exist, return (None, None)

    Examples:
        >>> f(3, -9, 16)
        (3, 4)
        >>> f(-6, -9, 16)
        (None, None)
    '''
    if x**3 + a*x + b < 0:
        return (None, None) # point doesn't exist
    else:
        return (math.sqrt(x**3 + a*x + b), -math.sqrt(x**3 + a*x + b))
    
def point_addition(P : tuple, Q : tuple, a : int, b : int, p : int = None) -> tuple:
    '''Add two points on an elliptic curve.

    Parameters:
        P : A point on the curve. Assume values are integers.
            If over a galois field, assume point is in generated point cloud
        Q : A point on the curve. Assume values are integers.
            If over a galois field, assume point is in generated point cloud
        a : The a coefficient of the curve.
        b : The b coefficient of the curve.
        p : (optional) The prime modulus of a field. If not provided, assume
            calculations are over the field of real numbers.

    Returns:
        The sum of the two points. return (None, None) if there is no third point

    Examples:
        >>> point_addition((-2, 2), (2, 4), -1, 10)
        (0.25, -3.125)
        >>> point_addition((2, 3), (5, 2), -1, 10, 7)
        (4, 0)
    '''
    if P == (None, None):
        return Q
    if Q == (None, None):
        return P
    if P == Q:
        if P[1] == 0:
            return (None, None)
        elif p:
            m = (3 * P[0] ** 2 + a) * pow((2 * P[1]) % p, -1, p) % p
            x = (m ** 2 - 2 * P[0]) % p
            y = (m * (P[0] - x) - P[1]) % p
        else:
            m = (3 * P[0] ** 2 + a) / (2 * P[1])
            x = m ** 2 - 2 * P[0]
            y = m * (P[0] - x) - P[1]
    else:
        if P[0] == Q[0]: # meaning P[1] != Q[1]
            return (None, None)
        if p:
            m = (Q[1] - P[1]) * pow((Q[0] - P[0]) % p, -1, p) % p
            x = (m ** 2 - P[0] - Q[0]) % p
            y = (m * (P[0] - x) - P[1]) % p
        else:
            m = (Q[1] - P[1]) / (Q[0] - P[0])
            x = m ** 2 - P[0] - Q[0]
            y = m * (P[0] - x) - P[1]
    return x, y

def point_scalar_multiplication(P : tuple, k : int, a : int, b : int, p : int = None) -> tuple:
    '''Multiply a point on an elliptic curve a given number of times.

    Parameters:
        P : A point on the curve. Assume values are integers. 
            If over a galois field, assume point is in generated point cloud
        k : The number of times to multiply the point. Assume positive integer.
        a : The a coefficient of the curve.
        b : The b coefficient of the curve.
        p : (optional) The prime modulus of a field. If not provided, assume
            calculations are over the field of real numbers.

    Returns:
        The product of the point and the number. return (None, None) if there is no third point

    Examples:
        >>> point_scalar_multiplication((3, 5), 3, -3, 7)
        (-2.28883, -1.36964)
        >>> point_scalar_multiplication((55, 36), 4, 23, 3, 61)
        (21, 29)
    '''
    def get_curve():
        if p:
            return (a, b, p)
        else:
            return (a, b)

    # Square and Multiply Method
    bin_k = bin(k)[2:]
    Q = P
    for i in range(1, len(bin_k)):
        Q = point_addition(Q, Q, *get_curve())
        if bin_k[i] == '1':
            Q = point_addition(Q, P, *get_curve())
    return Q

def generate_point_cloud(a : int, b : int, p = None) -> set:
    '''Generate a point cloud of a curve.

    Parameters:
        a : The a coefficient of the curve.
        b : The b coefficient of the curve.
        p : (optional) The prime modulus of a field. If not provided, assume
            calculations are over the field of real numbers.

    Returns:
        A set of points on the curve over the field F_{p}.
        Points should be in the range ([0, p-1], [0, p-1])

    Example:
        >>> generate_point_cloud(-1, 10, 11)
        {(None, None), (2, 4), (2, 7), (3, 1), (3, 10), (4, 2), (4, 9), (5, 3), (5, 8), (6, 0), (7, 4), (7, 7), (9, 2), (9, 9)}
    '''
    # efficient
    lookup = {}
    for x in range(p):
        residue = x**2 % p
        lookup.setdefault(residue, [])
        lookup[residue].append(x)
    
    points = set()
    points.add((None, None))
    for x in range(p):
        y_squared = (x**3 + a * x + b) % p
        if y_squared in lookup:
            for y in lookup[y_squared]:
                points.add((x, y))
    
    return points

###################### Visualization Functions ######################

def visualize_curve(ax, a : int, b : int, p : int = None, domain = (-5, 5)) -> None:
    """Visualize an elliptic curve.

    Parameters:
        ax : The axis to plot the curve on.
        a : The a coefficient of the curve.
        b : The b coefficient of the curve.
        domain : (optional) The domain of the curve. Default is (-5, 5).
        p : (optional) The prime modulus of a field. If not provided, assume
            calculations are over the field of real numbers.
    """ 
    if p:
        list_of_points = list(generate_point_cloud(a, b, p))
        x = [i[0] for i in list_of_points]
        y = [i[1] for i in list_of_points]

        ax.grid(True, which='both')
        ax.scatter(x, y, s=30)
    else:
        x = np.linspace(domain[0], domain[1], 10000)
        y1 = [f(i, a, b)[0] for i in x]
        y2 = [f(i, a, b)[1] for i in x]

        ax.grid(True, which='both')
        ax.plot(x, y1, 'r')
        ax.plot(x, y2, 'r')

        ax.set_xlim(domain[0], domain[1])
    
if __name__ == '__main__':
    # sample curve
    curve = {"a": 0, "b": 7}
    fig, ax = plt.subplots()
    visualize_curve(ax, *curve.values())

    # sample curve over prime field
    curve = {"a": 0, "b": 7, "p": 97}
    fig, ax = plt.subplots()
    visualize_curve(ax, *curve.values())

    plt.show()