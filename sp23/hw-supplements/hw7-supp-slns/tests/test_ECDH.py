# CS 2051 Spring 2023
# author - Sarthak Mohanty
# collaborators - N/A

# these are the tests for Elliptic Curve Diffie-Hellman

import unittest
from unittest import mock
from io import StringIO

import ECDH_solution as sol
import elliptic_curves_solution as sol_ec
from ECDH import *

import random
import time

class TestECDH(unittest.TestCase):
    def setUp(self) -> None:

        self.tinycurve = (1, -1, 10177)
        self.generators = []
        for _ in range(5):
            valid_points = sol_ec.generate_point_cloud(*self.tinycurve)
            valid_points.remove((None, None))
            self.generators.append(random.choice(list(valid_points)))
        self.private_keys1 = [random.randint(2, self.tinycurve[2] - 1) for _ in range(5)] # upper bound is given by Hasse's theorem
        self.private_keys2 = [random.randint(2, self.tinycurve[2] - 1) for _ in range(5)] # upper bound is given by Hasse's theorem

        self.longMessage = False

    # 3 points
    def test_actor(self):
        with mock.patch('sys.stdout', new = StringIO()) as std_out:
            for i in range(len(self.generators)):
                curve = self.tinycurve
                P = self.generators[i]
                k1 = self.private_keys1[i]
                k2 = self.private_keys2[i]

                alice = Actor("Alice", P, k1, *curve)
                sol_alice = sol.Actor("Alice", P, k1, *curve)
                bob = Actor("Bob", P, k2, *curve)
                sol_bob = sol.Actor("Bob", P, k2, *curve)

                # test computePublicKey()
                self.assertEqual(alice.computePublicKey(), sol_alice.computePublicKey(), msg= 'Actor class not working properly.')
                self.assertEqual(bob.computePublicKey(), sol_bob.computePublicKey(), msg= 'Actor class not working properly.')

                # # test computeSecret
                # check that two secret keys are equal to each other for two communicating actors
                alice.computeSecret(bob.computePublicKey())
                bob.computeSecret(alice.computePublicKey())
                self.assertEqual(alice._secret_key, bob._secret_key, msg= 'Actor class not working properly.')

                # check that the secret keys are correct
                sol_bob.computeSecret(sol_alice.computePublicKey())
                self.assertEqual(bob._secret_key, sol_bob._secret_key, msg= 'Actor class not working properly.')

    # 4 points
    def test_BadActor(self):
        with mock.patch('sys.stdout', new = StringIO()) as std_out:
            curve = self.tinycurve
            P = self.generators[0]
            k1 = self.private_keys1[0]
            k2 = self.private_keys2[0]

            sol_alice = sol.Actor("Alice", P, k1, *curve)
            sol_bob = sol.Actor("Bob", P, k2, *curve)

            petty_thief = BadActor("Petty Thief", P, *curve)
            sol_petty_thief = sol.BadActor("Petty Thief", P , *curve)
            crime_boss = BadActor("Crime Boss", P, *curve)
            sol_crime_boss = sol.BadActor("Crime Boss", P, *curve)

            # test brute_force
            self.assertEqual(petty_thief.brute_force(sol_alice.computePublicKey()),\
                                sol_petty_thief.brute_force(sol_alice.computePublicKey()), msg= 'BadActor class not working properly.')

            # test baby-step giant-step
            self.assertEqual(crime_boss.bsgs(sol_alice.computePublicKey()),\
                                sol_crime_boss.bsgs(sol_alice.computePublicKey()), msg= 'BadActor class not working properly.')
            
            # test stealSecret
            sol_alice.computeSecret(sol_bob.computePublicKey())
            secret = sol_alice._secret_key
            petty_thief.stealSecret(sol_alice, sol_bob, petty_thief.brute_force)
            self.assertEqual(petty_thief._secret_key, secret, msg= 'BadActor class not working properly.')

    # 3 points
    def test_BadActor_efficiency(self):
        for i in range(len(self.generators)):
            curve = self.tinycurve
            P = self.generators[i]

            ## run it 10 times and average the time
            time1_avg = 0
            time2_avg = 0
            num_iterations = 100
            for _ in range(num_iterations):
                k = random.randint(2, self.tinycurve[2] - 1) # upper bound is given by Hasse's theorem

                alice = Actor("Alice", P, k, *curve)
                petty_thief = sol.BadActor("Petty Thief", P, *curve)
                crime_boss = BadActor("Crime Boss", P, *curve)

                start = time.time()
                petty_thief.brute_force(alice.computePublicKey())
                end = time.time()
                time1 = end - start

                start = time.time()
                crime_boss.bsgs(alice.computePublicKey())
                end = time.time()
                time2 = end - start

                time1_avg += time1
                time2_avg += time2

            time1_avg /= num_iterations
            time2_avg /= num_iterations

        # test that bsgs is 10x faster than brute force
        self.assertEqual(time1_avg > 10*time2_avg, True, msg= 'BSGS not efficient enough, yours took {} seconds, the threshold was {} seconds'.format(time2_avg, time1_avg/10))
