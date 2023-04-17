import earleyparser


# Builds the following grammar:
# S -> 0S | 1S | 0 | 1
#
# Meaning it only accepts binary numbers
#
rules = [
    ('S', ['0', 'S']),
    ('S', ['1', 'S']),
    ('S', ['0']),
    ('S', ['1']),
]
grammar = earleyparser.Grammar(rules)
parser = earleyparser.Parser(grammar)
parser.run('101011')

#
# Checks if a word is accepted by a grammar
#
derivations = parser.get_completes()
if len(derivations) == 0:
    print('Not accepted')
else:
    print('Accepted!')

parser.run('101011')

#
# Checks if a word is accepted by a grammar
#
derivations = parser.get_completes()
if len(derivations) == 0:
    print('Not accepted')
else:
    print('Accepted!')