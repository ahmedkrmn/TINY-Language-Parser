class Node:
    def __init__(self, t, c, s):
        self.token_value = t
        self.code_value = c
        self.shape = s
        self.children = []
        self.sibling = None
        self.index = None

    def set_children(self, y):
        try:
            assert isinstance(y, list)
            for i in y:
                self.children.append(i)
        except:
            self.children.append(y)

    def set_sibling(self, y):
        self.sibling = y


class Parser:
    nodes_table = {}
    tmp_index = 0
    edges_table = []

    def __init__(self):
        self.token = str
        self.tokens_list = ['identifier', ':=',
                            'identifier', '+', 'number']
        self.code_list = ['x', ':=', 'x', '+', '5']
        self.tmp_index = 0
        self.token = self.tokens_list[self.tmp_index]
        self.parse_tree = None
        self.nodes_table = None
        self.edges_table = None
        self.same_rank_nodes = []

    def set_tokens_list_and_code_list(self, x, y):
        self.code_list = y
        self.tokens_list = x
        self.tmp_index = 0
        self.token = self.tokens_list[self.tmp_index]

    def next_token(self):
        if(self.tmp_index == len(self.tokens_list)-1):
            return False  # we have reachd the end of the list
        self.tmp_index = self.tmp_index + 1
        self.token = self.tokens_list[self.tmp_index]
        return True

    def match(self, x):
        if self.token == x:
            self.next_token()
            return True
        else:
            raise ValueError('Token Mismatch', self.token)

    def statement(self):
        if self.token == 'if':
            t = self.if_stmt()
            return t
        elif self.token == 'repeat':
            t = self.repeat_stmt()
            return t
        elif self.token == 'identifier':
            t = self.assign_stmt()
            return t
        elif self.token == 'read':
            t = self.read_stmt()
            return t
        elif self.token == 'write':
            t = self.write_stmt()
            return t
        else:
            raise ValueError('SyntaxError', self.token)

    def stmt_sequence(self):
        t = self.statement()
        p = t
        while self.token == ';':
            q = Node(None, None, None)
            self.match(';')
            q = self.statement()
            if q == None:
                break
            else:
                if t == None:
                    t = p = q
                else:
                    p.set_sibling(q)
                    p = q
        return t

    def factor(self):
        if self.token == '(':
            self.match('(')
            t = self.exp()
            self.match(')')
        elif self.token == 'number':
            t = Node(
                'CONSTANT', '(' + self.code_list[self.tmp_index] + ')', 'o')
            self.match('number')
        elif self.token == 'identifier':
            t = Node('IDENTIFIER',
                     '(' + self.code_list[self.tmp_index] + ')', 'o')
            self.match('identifier')
        else:
            raise ValueError('SyntaxError', self.token)
            return False
        return t

    def term(self):
        t = self.factor()
        while self.token == '*' or self.token == '/':
            p = Node(
                'OPERATOR', '(' + self.code_list[self.tmp_index] + ')', 'o')
            p.set_children(t)
            t = p
            self.mulop()
            p.set_children(self.factor())
        return t

    def simple_exp(self):
        t = self.term()
        while self.token == '+' or self.token == '-':
            p = Node(
                'OPERATOR', '(' + self.code_list[self.tmp_index] + ')', 'o')
            p.set_children(t)
            t = p
            self.addop()
            t.set_children(self.term())
        return t

    def exp(self):
        t = self.simple_exp()
        if self.token == '<' or self.token == '=' or self.token == '>':
            p = Node(
                'OPERATOR', '(' + self.code_list[self.tmp_index] + ')', 'o')
            p.set_children(t)
            t = p
            self.comparison_op()
            t.set_children(self.simple_exp())
        return t

    def if_stmt(self):
        t = Node('IF', '', 's')
        if self.token == 'if':
            self.match('if')
            t.set_children(self.exp())
            self.match('then')
            t.set_children(self.stmt_sequence())
            if self.token == 'else':
                self.match('else')
                t.set_children(self.stmt_sequence())
            self.match('end')
        return t

    def comparison_op(self):
        if self.token == '<':
            self.match('<')
        elif self.token == '=':
            self.match('=')
        elif self.token == '>':
            self.match('>')

    def addop(self):
        if self.token == '+':
            self.match('+')
        elif self.token == '-':
            self.match('-')

    def mulop(self):
        if self.token == '*':
            self.match('*')
        elif self.token == '/':
            self.match('/')

    def repeat_stmt(self):
        t = Node('REPEAT', '', 's')
        if self.token == 'repeat':
            self.match('repeat')
            t.set_children(self.stmt_sequence())
            self.match('until')
            t.set_children(self.exp())
        return t

    def assign_stmt(self):
        t = Node('ASSIGN', '(' + self.code_list[self.tmp_index] + ')', 's')
        self.match('identifier')
        self.match(':=')
        t.set_children(self.exp())
        return t

    def read_stmt(self):
        t = Node('READ', '(' + self.code_list[self.tmp_index+1] + ')', 's')
        self.match('read')
        self.match('identifier')
        return t

    def write_stmt(self):
        t = Node('WRITE', '', 's')
        self.match('write')
        t.set_children(self.exp())
        return t

    def create_nodes_table(self, args=None):
        if args == None:
            self.parse_tree.index = Parser.tmp_index
            Parser.nodes_table.update(
                {Parser.tmp_index: [self.parse_tree.token_value, self.parse_tree.code_value, self.parse_tree.shape]})
            Parser.tmp_index = Parser.tmp_index+1
            if len(self.parse_tree.children) != 0:
                for i in self.parse_tree.children:
                    self.create_nodes_table(i)
            if self.parse_tree.sibling != None:
                self.create_nodes_table(self.parse_tree.sibling)
        else:
            args.index = Parser.tmp_index
            Parser.nodes_table.update(
                {Parser.tmp_index: [args.token_value, args.code_value, args.shape]})
            Parser.tmp_index = Parser.tmp_index+1
            if len(args.children) != 0:
                for i in args.children:
                    self.create_nodes_table(i)
            if args.sibling != None:
                self.create_nodes_table(args.sibling)

    def create_edges_table(self, args=None):
        if args == None:
            if len(self.parse_tree.children) != 0:
                for i in self.parse_tree.children:
                    Parser.edges_table.append((self.parse_tree.index, i.index))
                for j in self.parse_tree.children:
                    self.create_edges_table(j)
            if self.parse_tree.sibling != None:
                Parser.edges_table.append(
                    (self.parse_tree.index, self.parse_tree.sibling.index))
                self.same_rank_nodes.append(
                    [self.parse_tree.index, self.parse_tree.sibling.index])
                self.create_edges_table(self.parse_tree.sibling)
        else:
            if len(args.children) != 0:
                for i in args.children:
                    Parser.edges_table.append((args.index, i.index))
                for j in args.children:
                    self.create_edges_table(j)
            if args.sibling != None:
                Parser.edges_table.append((args.index, args.sibling.index))
                self.same_rank_nodes.append([args.index, args.sibling.index])
                self.create_edges_table(args.sibling)

    def run(self):
        self.parse_tree = self.stmt_sequence()  # create parse tree
        self.create_nodes_table()  # create nodes_table
        self.create_edges_table()  # create edges_table
        self.edges_table = Parser.edges_table  # save edges_table
        self.nodes_table = Parser.nodes_table  # save nodes_table
        if self.tmp_index == len(self.tokens_list)-1:
            print('success')
        elif self.tmp_index < len(self.tokens_list):
            raise ValueError('SyntaxError', self.token)

    def clear_tables(self):
        self.nodes_table.clear()
        self.edges_table.clear()
