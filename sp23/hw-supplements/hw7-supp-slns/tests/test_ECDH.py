# CS 2051 Spring 2023
# author - Sarthak Mohanty
# collaborators - N/A

# these are the tests for Elliptic Curve Diffie-Hellman (ECDH) .py

import unittest

from ECDH import *

import time
import json

class TestECDH(unittest.TestCase):
    def setUp(self) -> None:
        with open('tests/sample_ECDH_problems.json', 'r') as f:
            ECDH_problems_json = json.load(f)
        
        self.curves = []
        self.generators = []
        self.alice_private_keys = []
        self.bob_private_keys = []
        self.alice_public_keys = []
        self.bob_public_keys = []
        self.shared_secret_keys = []
        self.times_to_crack = []
        for problem in ECDH_problems_json:
            self.curves.append(problem['curve_parameters'].values())
            self.generators.append(tuple(problem['generator']))
            self.alice_private_keys.append(problem['alice_private_key'])
            self.bob_private_keys.append(problem['bob_private_key'])
            self.alice_public_keys.append(tuple(problem['alice_public_key']))
            self.bob_public_keys.append(tuple(problem['bob_public_key']))
            self.shared_secret_keys.append(tuple(problem['shared_secret_key']))
            self.times_to_crack.append(problem['time_to_crack'])

    # 3 points
    def test_actor(self):
        for i in range(len(self.curves)):
            curve = self.curves[i]
            P = self.generators[i]
            k1 = self.alice_private_keys[i]
            k2 = self.bob_private_keys[i]

            alice = Actor("Alice", P, k1, *curve)
            bob = Actor("Bob", P, k2, *curve)

            # test computePublicKey
            self.assertEqual(alice.computePublicKey(), self.alice_public_keys[i], msg= 'incorrect computePublicKey')
            self.assertEqual(bob.computePublicKey(),self.bob_public_keys[i], msg= 'incorrect computePublicKey')

            # # test computeSecret
            # 1. check that two secret keys are equal to each other for two communicating actors
            alice.computeSecret(bob.computePublicKey())
            bob.computeSecret(alice.computePublicKey())
            self.assertEqual(alice._secret_key, bob._secret_key, msg= 'incorrect computeSecret')
            # 2. check that the secret keys are correct
            self.assertEqual(alice._secret_key, self.shared_secret_keys[i], msg= 'incorrect computeSecret')

    # 4 points
    def test_BadActor(self):
        for i in range(len(self.curves)):
            curve = self.curves[i]
            P = self.generators[i]
            k1 = self.alice_private_keys[i]
            k2 = self.bob_private_keys[i]

            petty_thief = BadActor("Petty Thief", P, *curve)
            crime_boss = BadActor("Crime Boss", P, *curve)

            # test brute_force
            self.assertEqual(petty_thief.brute_force(self.alice_public_keys[i]), k1,
                                msg='BadActor class not working properly on inputs {}, {}, {}, {}'.format(
                                    curve, P, k1, self.alice_public_keys[i]
                                )
                            )

            # test baby-step giant-step
            self.assertEqual(crime_boss.bsgs(self.alice_public_keys[i]), k1,
                                msg='BadActor class not working properly on inputs {}, {}, {}, {}'.format(
                                    curve, P, k1, self.alice_public_keys[i]
                                )
                            )

            # test stealSecret
            alice = Actor("Alice", P, k1, *curve)
            bob = Actor("Bob", P, k2, *curve)
            alice.computeSecret(bob.computePublicKey())
            secret = alice._secret_key
            petty_thief.stealSecret(alice, bob, petty_thief.brute_force)
            self.assertEqual(petty_thief._secret_key, secret,
                                msg= 'BadActor class not working on input {}, {}, {}, {}'.format(
                                    curve, P, k1, self.alice_public_keys[i]
                                )
                            )

    # 3 points
    def test_BadActor_efficiency(self):

        avg_bsgs_time = 0
        for i in range(len(self.curves)):
            curve = self.curves[i]
            P = self.generators[i]
            k1 = self.alice_private_keys[i]

            alice = Actor("Alice", P, k1, *curve)
            crime_boss = BadActor("Crime Boss", P, *curve)

            start = time.time()
            crime_boss.bsgs(alice.computePublicKey())
            end = time.time()
            bsgs_time = end - start
            avg_bsgs_time += bsgs_time

        avg_bsgs_time /= len(self.curves)

        # test that bsgs is, on average, at least 10x faster than brute force
        threshold = sum([time_to_crack['brute_force'] for time_to_crack in self.times_to_crack]) / (10 * len(self.curves))
        self.assertTrue(bsgs_time < threshold, msg= 'bsgs not efficient enough, yours took {} seconds, the threshold was {} seconds'.format(bsgs_time, threshold))
