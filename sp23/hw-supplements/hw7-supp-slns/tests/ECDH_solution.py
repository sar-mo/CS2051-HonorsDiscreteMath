# CS 2051 Spring 2023 - HW7 Supplement Part 4: Elliptic Curve Diffie-Hellman
# instructor: Gerandy Brito
# creator - Sarthak Mohanty

# author - Sarthak Mohanty
# collaborators - N/A

from typing import Callable # for type hinting
import math
from elliptic_curves_solution import point_addition, point_scalar_multiplication

class Actor:
    def __init__(self, name : str, P : tuple, k : int, a : int, b : int, n : int):
        ''' Initialize the actor with a name a private key, the public generator point,
        and the public curve parameters.

        Parameters:
            name: The name of the actor
            P : The generator point of the group
            k : The private key of the actor
            a : The a coefficient of the curve.
            b : The b coefficient of the curve.
            n : The prime modulus of a field.
        '''
        self.name = name
        self.P = P
        self.curve = (a, b, n)
        self.__private_key = k
        self._secret_key = None # single underscore indicates weak privacy (so autograder can access)

    def computePublicKey(self) -> tuple:
        '''Efficiently computes the public key using the private key and the generator.

        Parameters: none

        Returns: The public key
        '''
        return point_scalar_multiplication(self.P, self.__private_key, *self.curve)

    def computeSecret(self, offer):
        '''Efficiently the secret key using the offer and the private key.

        Parameters:
            offer: The public key of the other actor

        Returns: none. Should set the _secret_key field of the Actor.
        '''
        self._secret_key = point_scalar_multiplication(offer, self.__private_key, *self.curve)

class BadActor:
    
    def __init__(self, name : str, P : int, a : int, b : int, n : int):
        ''' Initialize the actor with a name, the public generator point,
            and the public curve parameters.
        
        Parameters:
            name: The name of the actor
            P : The generator point of the group
            a : The a coefficient of the curve.
            b : The b coefficient of the curve.
            n : The prime modulus of a field.
        '''
        self.name = name
        self.P = P
        self.curve = (a, b, n)
        self._secret_key = None # single underscore indicates weak privacy (so autograder can access)
    
    def brute_force(self, Q : tuple) -> int:
        """Brute Force algorithm to solve Discrete Log

        Parameters:
            Q : Q of kP = Q (mod n).

        Returns: k of kP = Q (mod n). If not found returns -1.
        """
        P, curve = self.P, self.curve
        # Iterate over all kP
        R = (None, None)
        for k in range(2 * curve[2]):
            if R == Q:
                return k
            R = point_addition(self.P, R, *self.curve)
        return -1

    def bsgs(self, Q : tuple) -> int:
        """Baby-Step Giant-Step algorithm to solve Discrete Log Problem

        Parameters:
            P : P of kP = Q (mod n).
            Q : Q of kP = Q (mod n).
            n : n of kP = Q (mod n). Prime number.

        Returns: k of kP = Q (mod n). If not found returns -1.
        """

        # # # Efficiency matters here, so solution is a bit longer.
        # # # Based off rewriting the equation kP = Q (mod n) as  Q - amP = bP (mod n)

        a, b, n = self.curve
        m = math.ceil(math.sqrt(n))

        # Calculate all bP
        # To do so we first compute all bP and store them in a dictionary
        baby_steps = {(None, None) : 0}
        bP = self.P
        for b in range(1, m + 1):
            baby_steps[bP] = b
            bP = point_addition(bP, self.P, *self.curve)

        # # Alternatively, we can use a dictionary comprehension that is a bit slower
        # baby_steps = {point_scalar_multiplication(self.P, b, *self.curve): b for b in range(0, m)}

        # Now we have to compute Q - amP and check if it is in the table
        # To do so first we compute Q - mp and then continously subtract mp. We do this for a total of "a" times.
        # (Alternatively, we can use a list comprehension that is a bit slower)
        giant_step = Q
        amP = point_scalar_multiplication(self.P, m, *self.curve)
        for a in range(m):
            if giant_step in baby_steps:
                return a * m + baby_steps[giant_step]
            else:
                negative_amP = (amP[0], -amP[1] % n) # -amP
                giant_step = point_addition(giant_step, negative_amP, *self.curve) # Q - amP
        return -1

    def stealSecret(self, actor1 : Actor, actor2 : Actor, attack : Callable) -> None:
        """Steals secret key from Actor1 and Actor2.
        Should not use any private fields from Actor1 or Actor2.

        Parameters:
            actor1: Actor1
            actor2: Actor2
            attack: Attack function, either brute_force or bsgs
            
        Returns: none. Should set the _secret_key field of the BadActor.
        """
        a = attack(actor1.computePublicKey())
        b = attack(actor2.computePublicKey())
        self._secret_key = point_scalar_multiplication(self.P, a * b, *self.curve)