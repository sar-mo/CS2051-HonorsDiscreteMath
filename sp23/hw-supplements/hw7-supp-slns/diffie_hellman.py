# CS 2051 Spring 2023 - HW7 Supplement Part 1: Diffie-Hellman Key Exchange Algorithm
# instructor: Gerandy Brito
# creator - Sarthak Mohanty

# author - Sarthak Mohanty
# collaborators - N/A

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
        self._secret_key = None # single underscore indicates weak private indicator (so autograder can access)

    def computePublicKey(self):
        '''Efficiently computes the public key using the private key and the generator.

        Parameters: none

        Returns: The public key
        '''
        return pow(self.g, self.__private_key, self.p)

    def computeSecret(self, offer):
        '''Efficiently computes the secret key using the offer and the private key.

        Parameters:
            offer: The public key of the other actor

        Returns: none. Should set the _secret_key field of the Actor.
        '''
        self._secret_key = pow(offer, self.__private_key, self.p)

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
            y : y of g^x = y (mod p).

        Returns: x of g^x = y (mod p). Assume x is non-negative integer.
          If not found returns -1.
        """
        g, p = self.g, self.p

        # Iterate over all g^i
        g_raised_to_i = 1
        for i in range(0, p-1):
            if g_raised_to_i == y:
                return i
            g_raised_to_i = (g_raised_to_i * g) % p
        return -1

    def bsgs(self, y : int) -> int:
        """Baby-Step Giant-Step algorithm to solve Discrete Log Problem

        Parameters:
            y : y of g^x = y (mod p). Non-negative integer.
            
        Returns: x of g^x = y (mod p). If not found returns -1.
        """

        # # # Efficiency matters here, so solution is a bit longer.
        # # # Based off rewriting the equation g^x = y (mod p) as g^a = y * g^(-bm) (mod p)

        g, p = self.g, self.p
        m = math.ceil(math.sqrt(self.p))

        # Calculate all g^a and fill the table
        # To do so we first compute g^0 by continuously raising its power
        baby_steps = {}
        g_raised_to_b = 1
        for b in range(0, m):
            baby_steps[g_raised_to_b] = b
            g_raised_to_b = (g_raised_to_b * g) % p

        # # Alternatively, we can use a dictionary comprehension that is a bit slower
        # baby_steps = {pow(self.g, a, p) : a for a in range(m)}

        # Now we have to compute y * g^(-bm) and check if it is in the table
        # To do so first we compute g^(-m) and continuously raise its power
        # (Alternatively, we can use a list comprehension that is a bit slower)
        big_step = y
        g_raised_to_minus_m = pow(g, -m, p)
        for a in range(m):
            if big_step in baby_steps:
                return a * m + baby_steps[big_step]
            else:
                big_step = (big_step * g_raised_to_minus_m) % p
        
        return -1
    
    def stealSecret(self, actor1 : Actor, actor2 : Actor, attack : Callable) -> None:
        """Steals secret key from Actor1 and Actor2.
        Should not use any private fields from Actor1 or Actor2.

        Parameters:
            actor1: Actor1
            actor2: Actor2
            # attack: Name of the attack function, either 'brute_force' or 'bsgs'
            attack: Attack function to be used, either (brute_force or bsgs)
            
        Returns: none. Should set the _secret_key field of the BadActor.
        """
        # attack = getattr(BadActor, attack)
        a = attack(actor1.computePublicKey())
        b = attack(actor2.computePublicKey())
        self._secret_key = pow(self.g, a * b, self.p)