# CS 2051 Spring 2023 - HW7 Supplement Part 1: Diffie-Hellman Key Exchange Algorithm
# instructor: Gerandy Brito
# creator - Sarthak Mohanty

# author - your name here
# collaborators - list collaborators here

from typing import Callable # for type hinting
import math

class Actor:
    def __init__(self, name : str, p : int, g : int, a : int):
        ''' Initialize the actor with a name, the public parameters p and g, and a private key a.

        Parameters:
            name: The name of the actor
            p: A prime number
            g: A generator of the group
            a: The private key of the actor
        '''
        self.name = name
        self.p = p
        self.g = g
        self.__private_key = a
        self._secret_key = None # single underscore indicates weak privacy (so autograder can access)

    def computePublicKey(self) -> int:
        '''Efficiently computes the public key using the private key and the generator.

        Parameters: none

        Returns: The public key
        '''
        ### YOUR CODE HERE ###
        return NotImplementedError

    def computeSecret(self, offer : int) -> None:
        '''Efficiently computes the secret key using the offer and the private key.

        Parameters:
            offer: The public key of the other actor

        Returns: none. Should set the _secret_key field of the Actor.
        '''
        ### YOUR CODE HERE ###
        return NotImplementedError

class BadActor:
    
    def __init__(self, name : str, p : int, g : int):
        ''' Initialize the actor with a name and the public parameters p and g.

        Parameters:
            name: The name of the actor
            p: A prime number
            g: A generator of the group
        '''
        self.name = name
        self.p = p
        self.g = g
        self._secret_key = None
    
    def brute_force(self, y):
        """Brute Force algorithm to solve Discrete Log Problem

        Parameters:
            y : y of g^x = y (mod p). Non-negative integer.

        Returns: x of g^x = y (mod p). If not found returns -1.
        """
        ### YOUR CODE HERE ###
        return NotImplementedError

    def bsgs(self, y : int) -> int:
        """Baby-Step Giant-Step algorithm to solve Discrete Log Problem

        Parameters:
            y : y of g^x = y (mod p). Non-negative integer.
            
        Returns: x of g^x = y (mod p). If not found returns -1.
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