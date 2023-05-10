class Grammar(object):
    def __init__(self, rules):

        self.start = 'S'
        ## rules is a set of tuples (left, right)
        self.productions = {}
        for left, right in rules:
            if left not in self.productions:
                self.productions[left] = [right]
            else:
                self.productions[left].append(right)

    def is_terminal(self, symbol):
        return not self.is_nonterminal(symbol)

    def is_nonterminal(self, symbol):
        return symbol in self.productions
