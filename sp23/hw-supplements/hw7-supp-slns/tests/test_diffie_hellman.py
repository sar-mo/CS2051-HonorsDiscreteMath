# CS 2051 Spring 2023
# author - Sarthak Mohanty
# collaborators - N/A

# these are the tests for diffie hellman

import unittest

from diffie_hellman import *

import json
import time

class TestDiffieHellman(unittest.TestCase):
    def setUp(self) -> None:
        
        with open('tests/sample_diffie_hellman_problems.json', 'r') as f:
            diffie_hellman_problems_json = json.load(f)
        
        self.primes = []
        self.generators = []
        self.alice_private_keys = []
        self.bob_private_keys = []
        self.alice_public_keys = []
        self.bob_public_keys = []
        self.shared_secret_keys = []
        for problem in diffie_hellman_problems_json['easy_problems']:
            self.primes.append(problem['prime'])
            self.generators.append(problem['generator'])
            self.alice_private_keys.append(problem['alice_private_key'])
            self.bob_private_keys.append(problem['bob_private_key'])
            self.alice_public_keys.append(problem['alice_public_key'])
            self.bob_public_keys.append(problem['bob_public_key'])
            self.shared_secret_keys.append(problem['shared_secret_key'])
        self.hard_problems = diffie_hellman_problems_json['hard_problems']

    # 3 points
    def test_actor(self):

        for i in range(len(self.primes)):
            p = self.primes[i]
            g = self.generators[i]
            a = self.alice_private_keys[i]
            b = self.bob_private_keys[i]

            alice = Actor("Alice", p, g, a)
            bob = Actor("Bob", p, g, b)

            # test computePublicKey
            self.assertEqual(alice.computePublicKey(), self.alice_public_keys[i], msg= 'computePublicKey() not working')
            self.assertEqual(bob.computePublicKey(),self.bob_public_keys[i], msg= 'computePublicKey() not working')

            # # test computeSecret
            # 1. check that two secret keys are equal to each other for two communicating actors
            alice.computeSecret(bob.computePublicKey())
            bob.computeSecret(alice.computePublicKey())
            self.assertEqual(alice._secret_key, bob._secret_key, msg= 'incorrect secret key')
            # 2. check that the secret keys are correct
            self.assertEqual(alice._secret_key, self.shared_secret_keys[i], msg= 'incorrect secret key')

    # 4 points
    def test_BadActor(self):

        for i in range(len(self.primes)):
            p = self.primes[i]
            g = self.generators[i]
            a = self.alice_private_keys[i]
            b = self.bob_private_keys[i]

            petty_thief = BadActor("Petty Thief", p, g) 
            crime_boss = BadActor("Crime Boss", p, g) # better thief

            # test brute_force
            self.assertEqual(petty_thief.brute_force(self.alice_public_keys[i]), a,
                                msg='Brute force not working properly')

            # test baby-step giant-step
            self.assertEqual(crime_boss.bsgs(self.alice_public_keys[i]), a,
                            msg='Baby-step giant-step not working properly')
                            
            # test stealSecret
            alice = Actor("Alice", p, g, a)
            bob = Actor("Bob", p, g, b)
            alice.computeSecret(bob.computePublicKey())
            secret = alice._secret_key
            petty_thief.stealSecret(alice, bob, petty_thief.brute_force)
            self.assertEqual(petty_thief._secret_key, secret,
                                msg= 'stealSecret() not working')

    # 3 points
    def testBadActor_efficiency(self):

        for problem in self.hard_problems:
            p = problem['prime']
            g = problem['generator']
            a = problem['alice_private_key']

            alice = Actor("Alice", p, g, a)
            crime_boss = BadActor("Crime Boss", p, g)

            start = time.time()
            crime_boss.bsgs(alice.computePublicKey())
            end = time.time()
            bsgs_time = end - start

            # test that bsgs is 100x faster than brute force
            threshold = problem['time_to_crack']['brute_force'] / 100
            self.assertTrue(bsgs_time < threshold, msg= 'not efficient enough, yours took {} seconds, the threshold was {} seconds'.format(bsgs_time, threshold))
