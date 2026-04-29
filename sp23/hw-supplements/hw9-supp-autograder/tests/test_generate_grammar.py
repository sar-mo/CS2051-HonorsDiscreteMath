# CS 2051 Spring 2023 - HW9 Supplement Part 2-3 - Earley Parser Tests (Student Version)
# instructor: Gerandy Brito
# creator - Sarthak Mohanty

# test suite for CFG generation

from gradescope_utils.autograder_utils.decorators import weight, number
import unittest
import itertools

from generate_grammar import *
import earleyparser

class TestGenerateGrammar(unittest.TestCase):
    def setUp(self) -> None:
        self.parts_of_speech = {
            "singular_noun": {"woman", "man", "dumbbell", "barbell", "ab-roller", "treadmill", "trainer", "jump-rope", "bar", "protein-shake", "fellow"},
            "plural_noun": {"dumbbells", "barbells", "ab-rollers", "treadmills", "weights"},
            "proper_noun": {"Reese", "Paul", "Sofia", "Saloni", "Ananya", "Ron"},
            "intransitive verb": {"exercise", "run", "swim", "deadlift", "bench"},
            "transitive verb": {"eat", "lift", "drop", "carry", "deadlift", "bench", "exercise", "give"},
            "adjective": {"fit", "athletic", "healthy", "motivated", "resilient", "cold", "delicious", "unmotivated", "very", "extremely", "tall", "intelligent"},
            "adverb": {"quickly", "slowly", "eagerly", "steadily", "loudly", "enthusiastically"},
            "preposition": {"in", "on", "with", "at", "from", "over", "under", "to"},
            "article": {"the", "a", "an"},
            "pronoun": {"he", "she", "they", "it", "his", "her", "their", "its", "them"},
            "conjunction": {"and", "or", "but"}
            }
        # make proper nouns lowercase for easier matching
        self.parts_of_speech["proper_noun"] = {name.lower() for name in self.parts_of_speech["proper_noun"]}
    
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

    @weight(2.5)
    @number("1.1")
    def test_generate_cfg_binary(self):
        cfg = generate_cfg_binary()
        grammar = earleyparser.Grammar(cfg)
        # generate all binary strings with length less than or equal to 10
        strings = [bin(i)[2:] for i in range(1024)]
        # match strings are those which have the same number of 0s and 1s
        match_strings = [string for string in strings if string.count("0") == string.count("1")]
        # non-match strings are those which do not have the same number of 0s and 1s
        non_match_strings = [string for string in strings if string.count("0") != string.count("1")]
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

    @weight(2.5)
    @number("1.2")
    def test_generate_cfg_union(self):
        cfg = generate_cfg_union()
        grammar = earleyparser.Grammar(cfg)

        def generate_strings():
            ### generate all combinations of a^{i}b^{j}c^{k} where i + j + k <= 10
            strings = ["a" * i + "b" * j + "c" * k for i in range(11) for j in range(11) for k in range(11) if i + j + k <= 10]
            return strings
        
        # match strings are those which satisfy (i = j or i = k)
        match_strings = [string for string in generate_strings() if string.count("a") == string.count("b") or string.count("a") == string.count("c")]
        # non-match strings are those which do not satisfy (i = j or i = k)
        non_match_strings = [string for string in generate_strings() if string.count("a") != string.count("b") and string.count("a") != string.count("c")]
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

    @weight(2.5)
    @number("1.3")
    def test_generate_cfg_rna(self):
        cfg = generate_cfg_rna()
        grammar = earleyparser.Grammar(cfg)

        def generate_strings(n):
            letters = ['u', 'c', 'g', 'u']
            words = [''.join(i) for i in itertools.product(letters, repeat=n)]
            return words


        def is_matching(s, n):
            for i in (2, n // 2 - 1):
                x = s[:i]
                y = s[i:n-i]
                z = s[n-i:]
                if len(y) >= 4:
                    z_reversed = z[::-1]
                    if all((c1, c2) in {('a', 'u'), ('u', 'a'), ('c', 'g'), ('g', 'c')} for c1, c2 in zip(x, z_reversed)):
                        return True
            return False

        strings = []
        match_strings = []
        for i in range(1, 8):
            strings += generate_strings(i)
            match_strings += [string for string in strings if is_matching(string, i)]
        non_match_strings = list(set(strings) - set(match_strings))
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
    
    @weight(2.5)
    @number("1.4")
    def test_generate_cfg_tricky(self):
        cfg = generate_cfg_tricky()
        grammar = earleyparser.Grammar(cfg)
        # binary strings of length less than or equal to 15
        strings = [bin(i)[2:] for i in range(2**15)]
        def is_1i0j(string):
            import re
            return re.match(r'^(1*)0*$', string) is not None
        # match strings are those which are in the form 1^i 0^j and  2i != 3j + 1 
        match_strings = [string for string in strings if is_1i0j(string) and 2 * string.count('1') != 3 * string.count('0') + 1]
        non_match_strings = list(set(strings) - set(match_strings))
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