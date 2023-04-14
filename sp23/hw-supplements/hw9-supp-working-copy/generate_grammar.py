# CS 2051 Spring 2023 - HW9 Supplement Parts 2-3: Context-Free Grammars and Syntatical Structures
# instructor: Gerandy Brito
# creator - Sarthak Mohanty

# author - your name here
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

def generate_cfg_tricky():
    """Generates a CFG for the language {1^i 0^j : 2i != 3j + 1}"""

def generate_cfg_rna():
    """Generates a CFG for the language {s : s is a valid stem loop rna sequence}"""

def generate_cfg_logic(atoms):
    """Generates a CFG for the language {s : s is a valid logical expression}"""

def generate_cfg_english(parts_of_speech):
    """Generates a CFG for (some subset of) the language {s : s is a valid english sentence}"""
