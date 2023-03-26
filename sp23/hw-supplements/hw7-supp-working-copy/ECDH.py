# CS 2051 Spring 2023 - HW7 Supplement Part 4: Elliptic Curve Diffie-Hellman
# instructor: Gerandy Brito
# creator - Sarthak Mohanty

# author - your name here
# collaborators - list collaborators here

from typing import Callable # for type hinting
import math
from elliptic_curves import generate_point_cloud, point_addition, point_scalar_multiplication

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
        self._secret_key = None  # single underscore indicates weak privacy (so autograder can access)

    def computePublicKey(self) -> tuple:
        '''Efficiently computes the public key using the private key and the generator.

        Parameters: none

        Returns: The public key
        '''
        ### YOUR CODE HERE ###
        return NotImplementedError

    def computeSecret(self, offer : tuple) -> None:
        '''Efficiently the secret key using the offer and the private key.

        Parameters:
            offer: The public key of the other actor

        Returns: none. Should set the _secret_key field of the Actor.
        '''
        ### YOUR CODE HERE ###
        return NotImplementedError

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
        self._secret_key = None
    
    def brute(self, Q : tuple) -> int:
        """Brute Force algorithm to solve ECDLP

        Parameters:
            Q : Q of kP = Q (mod n).

        Returns: k of kP = Q (mod n). If not found returns -1.
        """
        ### YOUR CODE HERE ###
        return NotImplementedError

    def bsgs(self, Q : tuple) -> int:
        """Baby-Step Giant-Step algorithm to solve ECDLP

        Parameters:
            P : P of kP = Q (mod n).
            Q : Q of kP = Q (mod n).
            n : n of kP = Q (mod n). Prime number.

        Returns: k of kP = Q (mod n). If not found returns -1.
        """
        ### YOUR CODE HERE ###
        return NotImplementedError

    def stealSecret(self, actor1 : Actor, actor2 : Actor, attack : Callable) -> None:
        """Steals secret key from Actor1 and Actor2.
        Should not use any private fields from Actor1 or Actor2.

        Parameters:
            actor1: Actor1
            actor2: Actor2
            attack: Attack function, either brute_force or bsgs
            
        Returns: none. Should set the _secret_key field of the BadActor.
        """
        ### YOUR CODE HERE ###
        return NotImplementedError