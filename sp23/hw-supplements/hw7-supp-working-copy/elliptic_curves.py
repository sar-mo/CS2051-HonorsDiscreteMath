import math
from mathlib import *
import numpy as np
import matplotlib.pyplot as plt

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
    
def point_addition(P : tuple, Q : tuple, a : int, b : int, p = None) -> tuple:
    '''Add two distinct points on an elliptic curve.

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
    if p:
        ### YOUR CODE HERE ###
        return NotImplementedError
    else:
        ### YOUR CODE HERE ###
        return NotImplementedError

def point_scalar_multiplication(P : tuple, k : int, a : int, b : int, p = None) -> tuple:
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
        >>> point_scalar_multiplication((7, 19), 3, -3, 8)
        (1.496, 2.198)
        >>> point_scalar_multiplication((31, 29), 4, 23, 3, 91)
        (73, 85)
    '''
    if p:
        ### YOUR CODE HERE ###
        return NotImplementedError
    else:
        ### YOUR CODE HERE ###
        return NotImplementedError

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
        {(6, 2), (2, 7), (6, 5), (2, 0), (1, 4), (1, 3)}
    '''
    ### YOUR CODE HERE ###
    return NotImplementedError

###################### Visualization Functions, not finalized yet ######################

def visualize_curve(ax, domain : tuple, a : int, b : int, p = None) -> None:
    """Visualize an elliptic curve.

    Parameters:
    ax : The axis to plot the curve on.
    domain : The domain of the curve
    a : The a coefficient of the curve.
    b : The b coefficient of the curve.
    p : (optional) The prime modulus of a field. If not provided, assume
        calculations are over the field of real numbers.
    """ 
    if p:
        list_of_points = list(generate_point_cloud(a, b, p))
        x = [i[0] for i in list_of_points]
        y = [i[1] for i in list_of_points]

        ax.grid(True, which='both')
        ax.set_xlim(domain[0], domain[1])
        ax.scatter(x, y, s=30)
    else:
        x = np.linspace(domain[0], domain[1], 1000)
        y1 = [ f(i, a, b)[0] for i in x]
        y2 = [ f(i, a, b)[1] for i in x]

        ax.grid(True, which='both')
        ax.plot(x, y1, 'r')
        ax.plot(x, y2, 'r')

        ax.set_xlim(domain[0], domain[1])
    return ax

def visualize_addition(ax, P : tuple, Q : tuple, a : int, b : int, p = None) -> None:
    """Visualize point addition with two distinct points on an elliptic curve.

    Parameters
    ----------
    ax : The axis to plot the curve on.
    P : A point on the curve. if p is provided, P must be in the field.
    Q : A point on the curve. if p is provided, Q must be in the field.
    a : The a coefficient of the curve.
    b : The b coefficient of the curve.
    p : (optional) The prime modulus of a field. If not provided, assume
        calculations are over the field of real numbers.
    """ 
    if p:
        R = point_addition(P, Q, a, b, p)
        
    else:
        R = point_addition(P, Q, a, b)
        ax.plot([P[0], Q[0]], [P[1], Q[1]], color='yellow')

    # change domain to include all three points
    ax.set_xlim(min(P[0], Q[0], R[0]) - 1, max(P[0], Q[0], R[0]) + 1)
    ax.plot(P[0], P[1], label='P', marker='o')
    ax.annotate('P', P)
    ax.plot(Q[0], Q[1], label='Q', marker='o')
    ax.annotate('Q', Q)
    ax.plot(R[0], R[1], label='R', marker='o')
    ax.annotate('R', R)

    return ax

def visualize_multiplication(ax, P : tuple, n : int, a : int, b : int, p = None) -> None:
    """Visualize point multiplication on an elliptic curve.

    Parameters
    ----------
    ax : The axis to plot the curve on.
    P : A point on the curve. if p is provided, P must be in the field.
    Q : A point on the curve. if p is provided, Q must be in the field.
    a : The a coefficient of the curve.
    b : The b coefficient of the curve.
    p : (optional) The prime modulus of a field. If not provided, assume
        calculations are over the field of real numbers.
    """ 
    if p:
        R = point_scalar_multiplication(P, n, a, b, p)
        # to do: add line from P
    else:
        R = point_scalar_multiplication(P, n, a, b)
        print(R)
        # to do: add line from P
        
    plt.plot(P[0], P[1], label='P', marker='o')
    plt.annotate('P', P)
    plt.plot(R[0], R[1], label='R', marker='o')
    plt.annotate('R', R)

