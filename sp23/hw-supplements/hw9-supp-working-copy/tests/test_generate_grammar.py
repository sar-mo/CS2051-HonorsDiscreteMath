# CS 2051 Spring 2023 - HW9 Supplement Part 4 - Earley Parser Tests (Student Version)
# instructor: Gerandy Brito
# creator - Sarthak Mohanty

# these are a modified version of the tests for generate
# still a work in progress

import unittest

from generate_grammar_solution import *
import earleyparser

class TestGenerateGrammar(unittest.TestCase):
    # def setUp(self) -> None:

    def test_generate_cfg_example(self):
        cfg = generate_cfg_example()
        grammar = earleyparser.Grammar(cfg)
        match_strings = ["01", "0011", "000111", "00001111", ] # enter your own strings here
        non_match_strings = ["10", "011", "000110", "00001110", ] # enter your own strings here
        for string in match_strings:
            parser = earleyparser.Parser(grammar)
            parser.run(string)
            derivations = parser.get_completes()
            assert len(derivations) > 0, string
        for string in non_match_strings:
            parser = earleyparser.Parser(grammar)
            parser.run(string)
            derivations = parser.get_completes()
            assert len(derivations) == 0, string


    def test_generate_cfg_binary(self):
        cfg = generate_cfg_binary()
        grammar = earleyparser.Grammar(cfg)
        match_strings = ["01"] # enter your own strings here
        non_match_strings = ["10"] # enter your own strings here
        for string in match_strings:
            parser = earleyparser.Parser(grammar)
            parser.run(string)
            derivations = parser.get_completes()
            assert len(derivations) > 0, string
        for string in non_match_strings:
            parser = earleyparser.Parser(grammar)
            parser.run(string)
            derivations = parser.get_completes()
            assert len(derivations) == 0, string

    def test_generate_cfg_union(self):
        cfg = generate_cfg_union()
        grammar = earleyparser.Grammar(cfg)
        match_strings = ["aabbc",] # enter your own strings here
        non_match_strings = ["abbcc",] # enter your own strings here
        for string in match_strings:
            parser = earleyparser.Parser(grammar)
            parser.run(string)
            derivations = parser.get_completes()
            assert len(derivations) > 0, string
        for string in non_match_strings:
            parser = earleyparser.Parser(grammar)
            parser.run(string)
            derivations = parser.get_completes()
            assert len(derivations) == 0, string


    def test_generate_cfg_rna(self):
        cfg = generate_cfg_rna()
        grammar = earleyparser.Grammar(cfg)
        match_strings = ["GUGCCACGAUUCAACGUGGCAC",] # enter your own strings here
        non_match_strings = ["ACCGU",] # enter your own strings here
        for string in match_strings:
            parser = earleyparser.Parser(grammar)
            parser.run(string)
            derivations = parser.get_completes()
            assert len(derivations) > 0, string
        for string in non_match_strings:
            parser = earleyparser.Parser(grammar)
            parser.run(string)
            derivations = parser.get_completes()
            assert len(derivations) == 0, string
        
    def test_generate_cfg_tricky(self):
        cfg = generate_cfg_tricky()
        grammar = earleyparser.Grammar(cfg)
        match_strings = ["1110",]
        non_match_strings = ["110",]
        for string in match_strings:
            parser = earleyparser.Parser(grammar)
            parser.run(string)
            derivations = parser.get_completes()
            assert len(derivations) > 0, string
        for string in non_match_strings:
            parser = earleyparser.Parser(grammar)
            parser.run(string)
            derivations = parser.get_completes()
            assert len(derivations) == 0, string

    def test_generate_cfg_logic(self):
        cfg = generate_cfg_logic()
        grammar = earleyparser.Grammar(cfg)
        match_strings = [] # enter your own strings here
        non_match_strings = [] # enter your own strings here
        for string in match_strings:
            parser = earleyparser.Parser(grammar)
            parser.run(string)
            derivations = parser.get_completes()
            assert len(derivations) > 0, string
        for string in non_match_strings:
            parser = earleyparser.Parser(grammar)
            parser.run(string)
            derivations = parser.get_completes()
            assert len(derivations) == 0, string

    def test_generate_cfg_english(self):
        cfg = generate_cfg_english()
        grammar = earleyparser.Grammar(cfg)
        match_strings = ["1110",]
        non_match_strings = ["110",]
        for string in match_strings:
            parser = earleyparser.Parser(grammar)
            parser.run(string)
            derivations = parser.get_completes()
            assert len(derivations) > 0, string
        for string in non_match_strings:
            parser = earleyparser.Parser(grammar)
            parser.run(string)
            derivations = parser.get_completes()
            assert len(derivations) == 0, string
