# CS 2051 Spring 2023 - HW7 Supplement Part 4: Elliptic Curve Diffie-Hellman Key Exchange Algorithm
# instructor: Gerandy Brito
# creator - Sarthak Mohanty

# author - your name here
# collaborators - list collaborators here

import math
from elliptic_curves import point_addition, point_scalar_multiplication

class Actor:
    def __init__(self, name : str, n : int, P : tuple, k : int):
        ''' Initialize the actor with a name, a prime number n, a generator g, and a private key k.

        Parameters:
            name: The name of the actor
            n : A prime number
            P : The generator point of the group
            k : The private key of the actor
        '''
        self.name = name
        self.n = n
        self.P = P
        self.__private_key = k
        self.__secret_key = None

    def computePublicKey(self) -> tuple:
        '''Compute the public key using the private key and the generator.
        Should use a doubling algorithm for efficiency

        Parameters: none

        Returns: The public key
        '''

    def computeSecret(self, offer : tuple) -> None:
        '''Compute the secret key using the offer and the private key.
        Again should use a doubling algorithm for efficiency.

        Parameters:
            offer: The public key of the other actor

        Returns: none. Should set the __secret_key field of the Actor.
        '''

class BadActor:
    
    def __init__(self, name):
        self.name = name
        self.__secret_key = None
    
    def brute(self, P : tuple, Q : tuple, n : int) -> int:
        """Brute Force algorithm to solve Discrete Log

        Parameters:
            P : P of k*P = Q (mod n).
            Q : Q of k*P = Q (mod n).
            n : n of k*P = Q (mod n). Prime number.

        Returns: k of k*P = Q (mod n). If not found returns -1.
        """

    def bsgs(self, P : tuple, Q : tuple, n : int) -> int:
        """Baby-Step Giant-Step algorithm to solve Discrete Log Problem

        Parameters:
            P : P of k*P = Q (mod n).
            Q : Q of k*P = Q (mod n).
            n : n of k*P = Q (mod n). Prime number.

        Returns: k of k*P = Q (mod n). If not found returns -1.
        """

    def stealSecret(self, actor1 : Actor, actor2 : Actor, attack : function, P : tuple, n : int) -> None:
        """Steals secret key from Actor1 and Actor2.
        Should not use any private fields from Actor1 or Actor2.

        Parameters:
            actor1: Actor1
            actor2: Actor2
            attack: Attack function, either brute_force or bsgs
            P: P of k*P = Q (mod n).
            n: n of k*P = Q (mod n). Prime number.
            
        Returns: none. Should set the __secret_key field of the BadActor.
        """