# CS 2051 Spring 2023
# author - Sarthak Mohanty
# collaborators - N/A

# these are the tests for diffie hellman

import unittest
from unittest import mock
from io import StringIO

import diffie_hellman_solution as sol
from diffie_hellman import *
import random

import time

class TestDiffieHellman(unittest.TestCase):
    def setUp(self) -> None:
        
        def get_generators(p: int) -> list:
            """
            Brute force algorithm that returns the generators of Zp*
            """
            generators = []
            values = {i for i in range(1, p)}
            for g in range(1, p):
                storage = set()
                for i in range(1, p):
                    storage.add(pow(g, i, p))
                if storage == values:
                    generators.append(g)
            return generators
        
        self.primes = [5, 7, 11, 73, 151, 157, 251, 283, 503, 311, 797, 811]
        self.generators = [random.choice(get_generators(p)) for p in self.primes]
        self.private_keys1 = [random.randint(2, self.primes[i] - 1) for i in range(len(self.primes))]
        self.private_keys2 = [random.randint(2, self.primes[i] - 1) for i in range(len(self.primes))]

        self.longMessage = False

    # 3 points
    def test_actor(self):
        with mock.patch('sys.stdout', new = StringIO()) as std_out:
            for i in range(len(self.primes)):
                p = self.primes[i]
                g = self.generators[i]
                a = self.private_keys1[i]
                b = self.private_keys2[i]

                alice = Actor("Alice", p, g, a)
                sol_alice = sol.Actor("Alice", p, g, a)
                bob = Actor("Bob", p, g, b)
                sol_bob = sol.Actor("Bob", p, g, b)

                # test computePublicKey()
                self.assertEqual(alice.computePublicKey(), sol_alice.computePublicKey(), msg= 'Actor class not working')
                self.assertEqual(bob.computePublicKey(), sol_bob.computePublicKey(), msg= 'Actor class not working')

                # # test computeSecret
                # check that two secret keys are equal to each other for two communicating actors
                alice.computeSecret(bob.computePublicKey())
                bob.computeSecret(alice.computePublicKey())
                self.assertEqual(alice._secret_key, bob._secret_key, msg= 'Actor class not working')

                # check that the secret keys are correct
                sol_bob.computeSecret(sol_alice.computePublicKey())
                self.assertEqual(bob._secret_key, sol_bob._secret_key, msg= 'Actor class not working')

    # 4 points
    def test_BadActor(self):
        with mock.patch('sys.stdout', new = StringIO()) as std_out:

            for i in range(len(self.primes)):
                p = self.primes[i]
                g = self.generators[i]
                a = self.private_keys1[i]
                b = self.private_keys2[i]

                sol_alice = sol.Actor("Alice", p, g, a)
                sol_bob = sol.Actor("Bob", p, g, b)

                petty_thief = BadActor("Petty Thief", p, g) 
                sol_petty_thief = sol.BadActor("Petty Thief", p, g)
                crime_boss = BadActor("Crime Boss", p, g) # better thief
                sol_crime_boss = sol.BadActor("Crime Boss", p, g)

                # test brute_force
                self.assertEqual(petty_thief.brute_force(sol_alice.computePublicKey()),\
                                    sol_petty_thief.brute_force(sol_alice.computePublicKey()), msg= 'BadActor class not working properly on inputs {}, {}, {}, {}'.format(p, g, a, sol_alice.computePublicKey()))

                # test baby-step giant-step
                self.assertEqual(crime_boss.bsgs(sol_alice.computePublicKey()),\
                                    sol_crime_boss.bsgs(sol_alice.computePublicKey()), msg= 'BadActor class not working properly on inputs {}, {}, {}, {}'.format(p, g, a, sol_alice.computePublicKey()))
                
                # test stealSecret
                sol_alice.computeSecret(sol_bob.computePublicKey())
                secret = sol_alice._secret_key
                petty_thief.stealSecret(sol_alice, sol_bob, petty_thief.brute_force)
                self.assertEqual(petty_thief._secret_key, secret, msg= 'BadActor class not working on input {}, {}, {}, {}'.format(p, g, a, sol_alice.computePublicKey()))

    # 3 points
    def testBadActor_efficiency(self):

            # to do this, first we need a better way to generate a generator
            def get_generator_improved(p):
                # get generator of Zp* using Euler's theorem
                # https://en.wikipedia.org/wiki/Euler%27s_theorem

                # get prime factors of p-1
                factors = []
                n = p - 1
                i = 2
                while i * i <= n:
                    if n % i:
                        i += 1
                    else:
                        n //= i
                        factors.append(i)
                if n > 1:
                    factors.append(n)
                
                # get generator
                for g in range(2, p):
                    if all(pow(g, (p - 1) // f, p) != 1 for f in factors):
                        return g

            big_primes = [351416641, 388737889, 535619719, 735890717]

            for p in big_primes:
                g = get_generator_improved(p)
                a = random.randint(p//3, p//2)

                alice = Actor("Alice", p, g, a)
                petty_thief = sol.BadActor("Petty Thief", p, g)
                crime_boss = BadActor("Crime Boss", p, g)

                start = time.time()
                petty_thief.brute_force(alice.computePublicKey())
                end = time.time()
                time1 = end - start

                start = time.time()
                crime_boss.bsgs(alice.computePublicKey())
                end = time.time()
                time2 = end - start

                # test that bsgs is 100x faster than brute force
                self.assertEqual(time1 > 100*time2, True, msg= 'not efficient enough, yours took {} seconds, the threshold was {} seconds'.format(time2, time1/100))
