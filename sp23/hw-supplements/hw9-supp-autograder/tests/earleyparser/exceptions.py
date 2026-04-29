class EmptyGrammarError(Exception):
    def __init__(self):
        self.strerror = 'Empty grammar'
        super(EmptyGrammarError, self).__init__(self.strerror)

class InvalidNonterminalError(Exception):
    def __init__(self):
        self.strerror = 'Invalid nonterminal variable'
        super(InvalidNonterminalError, self).__init__(self.strerror)

class GrammarException(Exception):
    def __init__(self, strerror=''):
        self.strerror = strerror
        super(GrammarException, self).__init__(self.strerror)
