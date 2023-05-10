# work in progress, but the basic idea is there

class Row(object):
    def __init__(self, dot, left, right, pos, completes=[]):
        self.dot = dot
        self.left = left
        self.right = right
        self.pos = pos
        self.start = pos[0]
        self.end = pos[1]
        self.completes = completes

    def show(self):
        dotted = ''.join(self.right)
        formated = (self.left + ' -> ' + ' ' + dotted[:self.dot] +
                    '\033[94m.\033[0m' + dotted[self.dot:])
        if len(formated) < 10:
            formated += '\t'
        formated += '\t\033[93m/'+str(self.start)+'\033[0m'
        print(formated)

    def get_next(self):
        return self.right[self.dot] if self.dot < len(self.right) else None

    def is_complete(self):
        return self.dot == len(self.right)

    def __eq__(self, other):
        return (self.left == other.left and self.right == other.right and
                self.dot == other.dot and self.pos == other.pos)

class Table(object):
    def __init__(self, k):
        self.rows = []
        self.k = k

    def add_row(self, row, completes=None):
        if row not in self.rows:
            self.rows.append(row)

        if completes is not None and completes not in row.completes:
            row.completes.append(completes)

    def get_rows(self):
        return self.rows

    def __len__(self):
        return len(self.rows)

class Parser(object):
    def __init__(self, grammar):
        grammar.productions['GAMMA'] = [[grammar.start]]
        self.grammar = grammar
        self.tables = []
        self.words = []

    def add_table(self, k):
        self.tables.append(Table(k))

    def run(self, words):
        self.words = [[word] for word in words]
        self.init()

        for i in range(0, len(self.words) + 1):
            for row in self.tables[i].get_rows():
                if not row.is_complete():
                    if self.grammar.is_nonterminal(row.get_next()):
                        self.predict(row)
                    else:
                        self.scan(row)
                else:
                    self.complete(row)

    def init(self):
        # creates a GAMMA starting production and n+1 tables
        self.tables = []
        for i in range(0, len(self.words)+1):
            self.add_table(i)
        self.tables[0].add_row(Row(0, '', ['GAMMA'], (0, 0)))

    def scan(self, row):
        # creates a new row and copies the production that triggered this op
        # from the table[k-1] to the current table, advancing the pointer
        next_symbol = row.get_next()
        if row.end < len(self.words):
            atual = self.words[row.end][0]
            if next_symbol == atual:
                nrow = Row(1, next_symbol, [atual], (row.end, (row.end+1)))
                self.tables[row.end+1].add_row(nrow)

    def predict(self, row):
        # copies the productions from the nonterminal that triggered this op
        # with the new pointer in the begining of the right side
        next_row = row.get_next()
        if next_row in self.grammar.productions:
            for rule in self.grammar.productions[next_row]:
                self.tables[row.end].add_row(Row(0, next_row, rule, (row.end, row.end)))

    def complete(self, row):
        # advances all rows that were waiting for the current word
        for old_row in self.tables[row.start].get_rows():
            if (not old_row.is_complete() and
                old_row.right[old_row.dot] == row.left):
                nrow = Row((old_row.dot+1), old_row.left, old_row.right,
                           (old_row.start, row.end), old_row.completes[:])
                self.tables[row.end].add_row(nrow, row)

    def show_tables(self):
        for table in self.tables:
            for row in table.rows:
                row.show()

    def make_node(self, row, relatives=[]):
        nodo = {'a': row.left}
        nodo['children'] = [self.make_node(_, []) for _ in row.completes]
        if not row.completes:
            relatives += [row]
        if row.left == 'GAMMA':
            nodo['children'] += [{'a': self.words[_.start]} for _ in relatives
                                  if _.start < len(self.words)]
        return nodo

    def get_completes(self):
        # returns all rows that are in the GAMMA nonterminal
        completes = []
        for row in self.tables[-1].get_rows():
            if row.left == 'GAMMA':
                completes.append(row)
        del self.grammar.productions['GAMMA']

        return completes

    #
    # Runs parser on some list of words (tape) and pretty prints its derivation
    # tree.
    #
    # `derivation_no` denotes which completed derivation will be shown
    #
    def print_derivation_tree(self, words, derivation_no=0):
        self.run(words)
        derivations = self.get_completes()

        if len(derivations) < derivation_no:
            print("Error: derivation not found!")
            print("Are you sure the words given belong to the grammar?")
            return False

        root_node = self.make_node(derivations[derivation_no])
        self.walk_node(root_node)

    def walk_node(self, node, level=0):
        print((level * '..') + node['a'])
        for child in node['children']:
            self.walk_node(child, level + 1)
