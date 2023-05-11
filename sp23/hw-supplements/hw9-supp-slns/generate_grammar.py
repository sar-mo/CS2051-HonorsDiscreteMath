# CS 2051 Spring 2023 - HW9 Supplement Parts 2-3: Context-Free Grammars and Syntatical Structures
# instructor: Gerandy Brito
# creator - Sarthak Mohanty

# author - Sarthak Mohanty
# collaborators - N/A

# NOTE: Use [] to describe the empty string

def generate_cfg_example():
    """Generates a CFG for the language {0^n 1^n : n \in N}"""
    cfg = []
    # S generates 0S1
    cfg.append(('S', ['0', 'S', '1']))
    # S generates the empty string
    cfg.append(('S', []))
    return cfg

def generate_cfg_binary():
    """Generates a CFG for the language {s : s has the same number of 1s and 0s}"""
    cfg = []
    cfg.append(('S', ['1', 'S', '0', 'S']))
    cfg.append(('S', ['0', 'S', '1', 'S']))
    cfg.append(('S', []))
    return cfg

def generate_cfg_union():
    """Generates a CFG for the language {a^i b^j c^k : i, j, k \in N and (i = j or i = k)}"""
    cfg = []
    # S generates S1 or S2
    cfg.append(('S', ['S1']))
    cfg.append(('S', ['S2']))

    # i = j
    cfg.append(('S1', ['S1', 'C']))
    cfg.append(('S1', ['a', 'S1', 'b']))
    cfg.append(('S1', []))
    cfg.append(('C', ['c', 'C']))
    cfg.append(('C', []))

    # i = k
    cfg.append(('S2', ['a', 'S2', 'c']))
    cfg.append(('S2', ['B']))
    cfg.append(('B', ['b', 'B']))
    cfg.append(('B', []))

    return cfg

def generate_cfg_rna():
    """Generates a CFG for the language {s : s is a valid stem loop rna sequence}"""
    cfg = []
    bases = ['a', 'u', 'c', 'g']
    base_pairs = [('a', 'u'), ('u', 'a'), ('c', 'g'), ('g', 'c')]

    # stem of len > 2
    for b1, b2 in base_pairs:
        cfg.append(('S', [b1, 'A', b2]))
        cfg.append(('A', [b1, 'B', b2]))
        cfg.append(('B', [b1, 'B', b2]))
    cfg.append(('B', ['C']))

    # candy len > 4
    cfg.append(('C', ['D', 'D', 'D', 'D', 'E']))
    for base in bases:
        cfg.append(('D', [base]))
        cfg.append(('E', [base, 'E']))
    cfg.append(('E', []))

    return cfg

def generate_cfg_tricky():
    """Generates a CFG for the language {1^i 0^j : 2i != 3j + 1}"""
    cfg = []

    # # # See generate_cfg_tricky_sln.pdf for explanation
    
    # Part 1 : 2i > 3j + 1
    cfg.append(('S', ['S1']))
    cfg.append(('S', ['S2']))

    cfg.append(('S1', ['1', '1', '1', 'S1', '0', '0']))
    cfg.append(('S1', ['1', 'S1']))
    cfg.append(('S1', ['1']))

    cfg.append(('S2', ['1', '1', '1', 'S2', '0', '0']))
    cfg.append(('S2', ['1', 'S2']))
    cfg.append(('S2', ['1', '1', '1', '0']))

    # Part 2: 2i < 3j + 1
    cfg.append(('S', ['S3']))
    cfg.append(('S', ['S4']))
    cfg.append(('S', ['S5']))

    cfg.append(('S3', ['1', '1', '1', 'S3', '0', '0']))
    cfg.append(('S3', ['S3', '0']))
    cfg.append(('S3', []))

    cfg.append(('S4', ['1', '1', '1', 'S4', '0', '0']))
    cfg.append(('S4', ['1', '0']))
    cfg.append(('S4', ['S4', '0']))

    cfg.append(('S5', ['1', '1', '1', 'S5', '0', '0']))
    cfg.append(('S5', ['S5', '0']))
    cfg.append(('S5', ['1', '1', '0', '0']))
    
    return cfg

def generate_cfg_logic(atoms):
    """Generates a CFG for the language {s : s is a valid logical expression}"""
    cfg = []

    # Generate atoms
    for atom in atoms:
        cfg.append(('S', [atom]))
    cfg.append(('S', ['T'])) # did not use autograder for this function, so not sure if T is a valid nonterminal here
    cfg.append(('S', ['F']))

    # Generate operators
    cfg.append(('S', ['S', '&', 'S']))
    cfg.append(('S', ['S', '|', 'S']))
    cfg.append(('S', ['!', 'S']))
    cfg.append(('S', ['S', '=', '>', 'S']))
    cfg.append(('S', ['S', '<', '=', '>', 'S']))

    # Generate parentheses to ensure precedence
    cfg.append(('S', ['(', 'S', ')']))
    
    return cfg


def generate_cfg_english(parts_of_speech):
    """Generates a CFG for (some subset of) the language {s : s is a valid English sentence}"""
    cfg = []

    # # # See generate_cfg_english_sln.pdf for explanation

    # Define a mapping from the part of speech to the abbreviation used in the context-free grammar
    part_of_speech_mapping = {
        'singular_noun': 'NN',
        'plural_noun': 'NN',
        'proper_noun': 'NN',
        'pronoun': 'NN',
        'intransitive_verb': 'VI',
        'transitive_verb': 'VT',
        'adjective': 'ADJ',
        'adverb': 'ADV',
        'preposition': 'PREP',
        'conjunction': 'CONJ',
        'article': 'ART'
    }

    # Iterate over each part of speech and its corresponding abbreviation
    for pos, abbreviation in part_of_speech_mapping.items():
        # Iterate over each word in the part of speech
        for word in parts_of_speech[pos]:
            # Add a rule for each character in the word
            cfg.append((abbreviation, list(word)))

    # S -> S CONJ S
    cfg.append(('S', ['S', 'CONJ', 'S']))
    # S -> NP VP
    cfg.append(('S', ['NP', 'VP']))

    # NP -> (ART) (ADJs) NN (NPs)
    cfg.append(('NP', ['ART', 'ADJS', 'NN', 'NPs']))
    cfg.append(('ART', []))
    cfg.append(('ART', ['NN']))
    # ADJs -> ADJ (ADJs)
    cfg.append(('ADJS', ['ADJ', 'ADJS']))
    cfg.append(('ADJS', []))
    # NPs -> CONJ NP
    cfg.append(('NPs', ['CONJ', 'NP']))
    cfg.append(('NPs', []))

    # VP -> VI
    cfg.append(('VP', ['VI', 'PP', 'ADVS1']))
    # VP -> VT NP (PP) (ADVs1)
    cfg.append(('VP', ['VT', 'NP', 'PP', 'ADVS1']))
    # ADVs1 -> ADV (ADVs2)
    cfg.append(('ADVS1', ['ADV', 'ADVS2']))
    cfg.append(('ADVS1', []))
    # ADVs2 -> CONJ ADVs1
    cfg.append(('ADVS2', ['CONJ', 'ADVS1']))
    cfg.append(('ADVS2', []))
    # PP -> PREP NP
    cfg.append(('PP', ['PREP', 'NP']))
    cfg.append(('PP', []))

    return cfg