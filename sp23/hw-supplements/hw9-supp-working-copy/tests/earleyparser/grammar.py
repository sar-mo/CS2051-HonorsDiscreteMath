# -*- encoding: utf-8 -*-

class Grammar(object):
    def __init__(self, rules):
        # self.productions = productions
        # self.start = start

        self.start = 'S'
        ## rules is a set of tuples (left, right)
        self.productions = {}
        for left, right in rules:
            if left not in self.productions:
                self.productions[left] = [right]
            else:
                self.productions[left].append(right)
        


    # def add(self, left, right):
    #     if left not in self.productions:
    #         self.productions[left] = [right]
    #     else:
    #         self.productions[left].append(right)

    # def set_start(self, nonterminal):
    #     self.start = nonterminal

    def is_terminal(self, symbol):
        return not self.is_nonterminal(symbol)

    def is_nonterminal(self, symbol):
        return symbol in self.productions
