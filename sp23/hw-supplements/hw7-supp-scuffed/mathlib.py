from math import gcd, ceil
from operator import mul
from functools import reduce

# This function takes as input two integers in non-increasing order
# And returns the corresponding Bezout's coefficients and the gcd 
# in that order
# The algorithm has been adapted from Pseudocode from Wikipedia article
def extended_euclidean_algorithm(a: int, b: int) -> tuple:
    
    # s captures the Bezout's coefficient of a
    # and t does it for b for any number
    # At any point we store the Bezout's representation
    # of the last two values in the algorithm we are considering
    # Here a = a * 1 + b * 0 = a * old_s + b * old_t
    # Similarly, b = a * 0 + b * 1 = a * s + b * t
    s, old_s = 0, 1
    t, old_t = 1, 0

    # r variables do the normal Euclidean algorithm (EA)
    # They start off with b, a
    # As b <= a, we think of the first step of EA as,
    # a = b * q + remainder
    r, old_r = b, a

    # Loop until r becomes 0, at which point old_r = r * q
    # And so old_r will be the gcd
    while (r != 0):

        # Find the quotient on dividing old_r by r
        q = old_r // r

        # This is standard step from EA
        # It holds because gcd(a, b) = gcd(b, a%b)
        old_r, r = r, old_r % r

        # Now we update the Bezout's coefficients for u%v
        # When u = v * q + (u%v) and 
        # u = a * old_s + b * old_t and
        # v = a * s + b * t
        # We get,
        # u%v = (old_s - q * s) * a + (old_t - q * t) * b
        # Thus we get the new set of s and t
        # We forget the old_s and old_t
        # And move s -> old_s adding the newly calculated s to that variable
        # Same for t and old_t
        old_s, s = s, old_s - q * s
        old_t, t = t, old_t - q * t

    # old_r is the gcd 
    # old_s and old_t hold the Bezout's coefficients for old_r = gcd
    # So we return them too
    return old_s, old_t, old_r


def mod_inverse(g: int, n: int) -> int:
    """
    Computes inverse of g mod n.

    :param g: Positive integer g
    :param n: n (n > 1)
    :returns: inverse of g mod n
    """
    
    assert g > 0 and n > 1, "Inappropriate values to compute inverse"

    # g = g mod n
    # The inverse wouldn't change if the input was g or g mod p
    g = g % n

    # Inverse of g exists mod n iff gcd (g,n) == 1
    # In case the inverse exists it is v
    # where v is such that nu + gv = 1
    # This v is the one returned by the extended Euclidean algorithm
    _, v, g = extended_euclidean_algorithm(n, g)

    if g != 1:
        print("Inverse doesn't exist")
        exit()
    else:
        # As v can be negative we take mod n
        # to make it more readable.
        v = v % n
        return v


def solve_linear_congurence(a: int, b: int, m: int):
    """
    Returns the solutions to ax = b (mod m)

    Refer http://www.math.niu.edu/~richard/Math420/lin_cong.pdf

    :param a: a in ax = b (mod m). Positive integer.
    :param b: b in ax = b (mod m). Positive integer.
    :param m: m in ax = b (mod m). m > 1.
    :returns: If the equation is solvable, returns a list of solutions
              Otherwise returns -1.
    """
    
    # Compute the gcd. If gcd does not divide b then no solutions exist
    g = gcd(a, m)
    if b % g != 0:
        print("Recurrence can not be solved")
        return -1

    # Normalize a b and m by dividing by m
    a, b, m = a//g, b//g, m//g

    # Compute a^(-1). Guaranteed to exist as gcd of normalized a and m is 1.
    a_inverse = mod_inverse(a, m)

    # Compute the main solution = b * a^(-1)
    x = (b * a_inverse) % m

    # Generate all the solutions and return
    xs = [x + (i*m) for i in range(0, g)]
    return xs


def chinese_remainder(x : list, m : list, verify : bool = True):
    """
    Computes the solution to x = x[i] % m[i] for all i

    :param x: List of non-negative xs.
    :param m: List of non-negative ms.  
    :param verify: True if the function should test all the ms are mutually coprime
    """

    # Number of equations
    n = len(m)
    assert len(m) == len(x), "List size mismatch in CRT"

    # Verify that all ms are mutually coprime
    if verify:
        assert (all([gcd(m[i], m[j]) == 1 for i in range(n) for j in range(i+1, n)]))
    
    # Product of m list
    M = reduce(mul, m)

    # Compute the answer using the standard algorithm
    answer = 0
    for i in range(n):
        b = M // m[i]
        answer += x[i] * b * mod_inverse(b, m[i])

    return answer % M


def is_prime(n: int) -> bool:
    """
    Checks if n is prime

    :param n: Integer > 1.
    :returns: true if n is prime, false otherwise
    """
    assert n > 1, "Input be is_prime must be > 1"

    if n in [2, 3, 5, 7]:
        # n is prime
        return True
    if n % 2 == 0 or n % 3 == 0:
        # 2 or 3 divides n
        return False
    # sqrt(n) is upper bound for factor
    upper_bound = ceil(n ** 0.5)
    divisor = 5
    # Every prime except 2 and 3 is of the form 6k +- 1
    # So we start with 5 and increment by 6 the divisor
    # If divisior divides then number is composite
    while (divisor <= upper_bound):
        if n % divisor == 0 or n % (divisor +2) == 0:
            return False
        divisor += 6
    return True

def get_generator(p: int) -> int:
    """
    Returns a generator of Zp*

    :param p: Prime number
    :returns: Generator of Zp*
    """
    assert is_prime(p), "p must be prime"

    # We use the fact that if p is prime and p = 2q + 1
    # Then there exists a generator g of Zp* such that
    # g^q != 1 (mod p) and g^(2q) = 1 (mod p)
    # We use this fact to generate a generator
    q = (p - 1) // 2
    g = 2
    while (pow(g, q, p) == 1):
        g += 1
    return g