import math
from mathlib import *
import matplotlib.pyplot as plt
import numpy as np

INFINITY = float('inf')

def f(x, a, b, *p):
    """Compute the y-value of a point on an elliptic curve.

    Parameters
    ----------
    x : int
        The x-value of the point.
    a : int
        The a coefficient of the curve.
    b : int
        The b coefficient of the curve.
    p : int
        An optional prime modulus of the field. If not provided, the point is
        assumed to be over the field of real numbers.
    
    Returns
    -------
    int
        The two y-values of the point.
    """ 
    if p:
        return (math.sqrt(x**3 + a*x + b) % p, -math.sqrt(x**3 + a*x + b) % p)
    else:
        return (math.sqrt(x**3 + a*x + b), -math.sqrt(x**3 + a*x + b))
    
# add two points on an elliptic curve
def point_addition(P, Q, a, b):
    """Add two distinct points on an elliptic curve.

    Parameters
    ----------
    P : tuple
        A point on the curve.
    Q : tuple
        A point on the curve.
    a : int
        The a coefficient of the curve.
    b : int
        The b coefficient of the curve.
    p : int
        An optional prime modulus of the field. If not provided, the point is
        assumed to be over the field of real numbers.
    
    Returns
    -------
    tuple
        The sum of the two points.
    """ 
    if p:
        return NotImplementedError
    else:
        return NotImplementedError

# multiply a point on an elliptic curve
def point_multiplication(P, n, a, b, *p):

    """Multiply a point on an elliptic curve.

    Parameters
    ----------
    P : tuple
        A point on the curve.
    n : int
        The number of times to multiply the point. Assume positive integer.
    a : int
        The a coefficient of the curve.
    b : int
        The b coefficient of the curve.
    p : int
        An optional prime modulus of the field. If not provided, the point is
        assumed to be over the field of real numbers.
    
    Returns
    -------
    tuple
        The product of the point and the number.
    """
    if p:
        return NotImplementedError
    else:
        return NotImplementedError


####################### everything below this line doesn't really work yet

def visualize_curve(a, b, *p):
    """Visualize an elliptic curve.

    Parameters
    ----------
    a : int
        The a coefficient of the curve.
    b : int
        The b coefficient of the curve.
    p : int
        An optional prime modulus of the field. If not provided, the point is
        assumed to be over the field of real numbers.
    """ 
    if p:
        x = np.linspace(0, p, 1000)
        y = f(x, a, b, p)
        plt.plot(x, y, 'b')
        plt.plot(x, -y, 'b')
        plt.show()

    else:
        x = np.linspace(0, 10, 1000)
        y = f(x, a, b)
        plt.plot(x, y, 'b')
        plt.plot(x, -y, 'b')
        plt.show()

def visualize_addition(plot, P, Q, a, b, *p):
    """Visualize point addition with two distinct points on an elliptic curve.

    Parameters
    ----------
    plot: matplotlib.pyplot
        The plot to add the points to.
    P : tuple
        A point on the curve. if p is provided, P must be in the field.
    Q : tuple
        A point on the curve. if p is provided, Q must be in the field.
    a : int
        The a coefficient of the curve.
    b : int
        The b coefficient of the curve.
    p : int
        An optional prime modulus of the field. If not provided, the point is
        assumed to be over the field of real numbers.
    """ 
    if p:
        R = point_addition(P, Q, a, b, p)
        # to do: add line from P to Q
        
    else:
        R = point_addition(P, Q, a, b)
        # to do: add line from P to Q

    plt.plot(P[0], P[1], label='P', marker='o')
    plt.annotate('P', P)
    plt.plot(Q[0], Q[1], label='Q', marker='o')
    plt.annotate('Q', Q)
    plt.plot(R[0], R[1], label='R', marker='o')
    plt.annotate('R', R)

    return plot

def visualize_multiplication(plot, P, n, a, b, p):
    """Visualize point multiplication on an elliptic curve.

    Parameters
    ----------
    plot: matplotlib.pyplot
        The plot to add the points to.
    P : tuple
        A point on the curve. if p is provided, P must be in the field.
    Q : tuple
        A point on the curve. if p is provided, Q must be in the field.
    a : int
        The a coefficient of the curve.
    b : int
        The b coefficient of the curve.
    p : int
        An optional prime modulus of the field. If not provided, the point is
        assumed to be over the field of real numbers.
    """ 
    if p:
        R = point_multiplication(P, n, a, b, p)
        # to do: add line from P
    else:
        R = point_multiplication(P, n, a, b)
        # to do: add line from P
        
    plt.plot(P[0], P[1], label='P', marker='o')
    plt.annotate('P', P)
    plt.plot(R[0], R[1], label='R', marker='o')
    plt.annotate('R', R)

    return plot