# CS 2051 Spring 2023 - HW7 Supplement Part 1: Diffie-Hellman Key Exchange Algorithm
# instructor: Gerandy Brito
# creator - Sarthak Mohanty

# author - your name here
# collaborators - list collaborators here


import math

class Actor:
    def __init__(self, name : str, p : int, g : int, a : int):
        ''' Initialize the actor with a name, a prime number p, a generator g, and a private key a.

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
        self.__secret_key = None

    def computePublicKey(self) -> int:
        '''Compute the public key using the private key and the generator.
        Should use a doubling algorithm for efficiency

        Parameters: none

        Returns: The public key
        '''

    def computeSecret(self, offer : int) -> None:
        '''Compute the secret key using the offer and the private key.
        Again should use a doubling algorithm for efficiency.

        Parameters:
            offer: The public key of the other actor

        Returns: none. Should set the __secret_key field of the Actor.
        '''

class BadActor:
    
    def __init__(self, name : str):
        self.name = name
        self.__secret_key = None
    
    def brute(self, g, y, p):
        """Brute Force algorithm to solve Discrete Log

        Parameters:
            g : g of g^x = y (mod p). g > 0.
            y : y of g^x = y (mod p). Non-negative integer.
            p : p of g^x = y (mod p). Prime number.

        Returns: x of g^x = y (mod p). If not found returns -1.
        """

    def bsgs(self, g : int, y : int, p : int) -> int:
        """Baby-Step Giant-Step algorithm to solve Discrete Log Problem

        Parameters:
            g : g of g^x = y (mod p). g > 0.
            y : y of g^x = y (mod p). Non-negative integer.
            p : p of g^x = y (mod p). Prime number.
            
        Returns: x of g^x = y (mod p). If not found returns -1.
        """

    def stealSecret(self, actor1 : Actor, actor2 : Actor, attack : function, g : int, p : int) -> None:
        """Steals secret key from Actor1 and Actor2.
        Should not use any private fields from Actor1 or Actor2.

        Parameters:
            actor1: Actor1
            actor2: Actor2
            attack: Attack function, either brute_force or bsgs
            g : g of g^x = y (mod p). g > 0.
            p : p of g^x = y (mod p). Prime number.
            
        Returns: none. Should set the __secret_key field of the BadActor.
        """