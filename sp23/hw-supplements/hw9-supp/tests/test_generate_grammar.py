# CS 2051 Spring 2023 - HW9 Supplement Part 4 - Earley Parser Tests (Student Version)
# instructor: Gerandy Brito
# creator - Sarthak Mohanty

# these are a modified version of the tests for generate
# still a work in progress

import unittest

from generate_grammar import *
import earleyparser

class TestGenerateGrammar(unittest.TestCase):
    def setUp(self) -> None:
        self.parts_of_speech = {
            "singular_noun": {"dumbbell", "barbell", "ab roller", "treadmill"},
            "plural_noun": {"dumbbells", "barbells", "ab rollers", "treadmills"},
            "proper_noun": {"Reese", "Paul", "Sofia", "Saloni", "Ananya", "Ron"},
            "intransitive verb": {"exercise", "run", "swim", "deadlift", "bench"},
            "transitive verb": {"lift", "carry", "deadlift", "bench"},
            "adjective": {"fit", "athletic", "healthy", "motivated", "resilient"},
            "adverb": {"quickly", "slowly", "eagerly", "steadily", "loudly"},
            "preposition": {"in", "on", "with", "at", "from", "over", "under"},
            "article": {"the", "a", "an"},
            "pronoun": {"he", "she", "they", "it"},
            "conjunction": {"and", "or", "but"}
            }
        # make proper nouns lowercase for easier matching
        self.parts_of_speech["proper_noun"] = {name.lower() for name in self.parts_of_speech["proper_noun"]}
    
    def test_generate_cfg_example(self):
        cfg = generate_cfg_example()
        grammar = earleyparser.Grammar(cfg)
        match_strings = ["01", "0011", "000111", "00001111", ]
        non_match_strings = ["10", "011", "000110", "00001110", ]
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
        match_strings = ["01", "10"] # enter your own strings here
        non_match_strings = ['110'] # enter your own strings here
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
        match_strings = ["gugccacgauucaacguggcac",] # enter your own strings here
        non_match_strings = ["accgu",] # enter your own strings here
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
        cfg = generate_cfg_logic({'p', 'q'})
        grammar = earleyparser.Grammar(cfg)
        match_strings = ["(p&q)"] # enter your own strings here
        non_match_strings = ["()", "(|)"] # enter your own strings here
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
        cfg = generate_cfg_english(self.parts_of_speech)
        for sentence in self.sentences:
            grammar = earleyparser.Grammar(cfg)
            parser = earleyparser.Parser(grammar)
            match_strings = ["the trainer carry the dumbbells"] # enter your own strings here
            match_strings = [string.replace(" ", "") for string in match_strings]
            parser.run(sentence)
            derivations = parser.get_completes()
            assert len(derivations) > 0, sentence