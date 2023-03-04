# Course: CS 2051, Spring 2023
# Instructor: Gerandy Brito
# Author: Sarthak Mohanty
# Assignment: Homework 0 Supplement

# First, create a class called Proposition.
# It takes in a string as an argument.
# Assume the string is a valid propositional formula that uses the variables p - z and the operators 'and', 'or', and 'not
# Examples of such strings are:
    # "p and (q or r)"
    # "p or q"
    # "not p"
    # "p and q and r"
    # "(p) or q or (not r)"
# The string should be stored as an instance variable called self.func.

# Next, create two subclasses of Proposition called Implication and Equivalence.
# These classes should take in two Proposition objects as arguments.
# WLOG, assume the first Proposition object is the antecedent (p) and the second is the consequent (q).
# self.func should be set equivalent to the string "p implies q" or "p iff q" respectively.
# However, since the Propsition class does not support the implies and iff operators,
# you will need to represent these string using the operators and, or, and not.
# make sure to use parentheses appropriately.

# Finally, create a method called extract_variables.
# This method should take in a Proposition object and return a Set of all the variables in the proposition.
# For example, if the proposition is "p and (q or r)", the method should return the set {"p", "q", "r"}.
# Challenge: Can you do it in one line? (Hint: try importing the re class)

import re

class Proposition:
    def __init__(self, func):
        self.func = func

class Implication(Proposition):
    def __init__(self, prop1, prop2):
        self.func = "(not " + prop1.func + ") or " + prop2.func
    
class Equivalence(Proposition):
    def __init__(self, prop1, prop2):
        self.func = "((" + prop1.func + ") and (" + prop2.func + ")) or ((not " + prop1.func + ") and (not " + prop2.func + "))"

def extract_variables(prop):
    # solution 1: remove all operators and return the rest
    prop = prop.replace("(", "").replace(")", "").replace("not ", "").replace(" and ", "").replace(" or ", "")
    return set(list(prop.split()))

    # # solution 2: use regex to find variables directly
    # return set(re.findall(r'\b[p-z]\b', prop.func))