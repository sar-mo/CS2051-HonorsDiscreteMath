import math
from mathlib import *
from elliptic_curves_solution import point_addition, point_scalar_multiplication

class Actor:
    def __init__(self, name, p, g, a):
        self.name = name
        self.p = p
        self.g = g
        self.private_key = a
        self.public_key = None
        self.secret_key = None

    def computePublicKey(self):
        '''
        Compute the public key using the private key and the generator
        '''

    def computeSecret(self, offer):
        '''
        Compute the secret key using the offer and the private key
        '''

class BadActor:
    
    def __init__(self, name):
        self.name = name
    
    def brute(self, g, y, n):
        '''
        Brute Force to solve Discrete Log with Elliptic Curves

        :param g: g of g^x = y (mod n). g > 0.
        :param y: y of g^x = y (mod n). Non-negative integer.
        :param n: n of g^x = y (mod n). n > 1.
        :returns: x of g^x = y (mod n). If not found returns -1.
        '''

    def bsgs(self, g, y, p, max_power=None, verify: bool = True):
        """
        Baby-Step Giant-Step algorithm to solve Discrete Log Problem with Elliptic Curves

        :param g: g of g^x = y (mod n). g > 0.
        :param y: y of g^x = y (mod n). Non-negative integer.
        :param p: p of g^x = y (mod p). Prime number.
        :param max_power: restricts the search of x between [1, max_power). Useful for Pohling_Hellman
        :param verify: Checks if p is prime when True
        :returns: x of g^x = y (mod n). If not found returns -1.
        # """