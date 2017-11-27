import shutil, tempfile
from os import path
import unittest
import tokenizer
import tree

Token = tokenizer.Token

# --------------------------------
# -------- TEST TOKENIZER --------
# --------------------------------

class TestStringEnds(unittest.TestCase):
    def test_find_string_ends(self):
        cases= [
                ['',
                 []],
                ['test string',
                 ['t', 'e', 's', 't', ' ', 's', 't', 'r', 'i', 'n', 'g']],
                ['test "string"',
                 ['t', 'e', 's', 't', ' ', ('"',), 's', 't', 'r', 'i', 'n', 'g', ('"',)]],
                ["'test' string",
                 [("'",), 't', 'e', 's', 't', ("'",),  ' ', 's', 't', 'r', 'i', 'n', 'g']],
                ["test '''string'''",
                 ['t', 'e', 's', 't', ' ', ("'''",), 's', 't', 'r', 'i', 'n', 'g', ("'''",)]],
                ['"""test""" string',
                 [('"""',), 't', 'e', 's', 't', ('"""',), ' ', 's', 't', 'r', 'i', 'n', 'g']],
                 ]

        for c,e in cases:
            result = list(tokenizer.findStringEnds(c))
            self.assertEqual(result,e)

class TestStringLiterals(unittest.TestCase):
    def test_extract_string_literals(self):
        cases= [
                ['',
                 []
                 ],
                ['test string',
                 [Token(tag='raw', value='test string')]
                 ],
                ['test "string"',
                 [Token(tag='raw', value='test '), Token(tag='literal', value='string')]
                 ],
                ["'test' string",
                 [Token(tag='literal', value='test'), Token(tag='raw', value=' string')]
                 ],
                ["test '''string'''",
                 [Token(tag='raw', value='test '), Token(tag='literal', value='string')]
                 ],
                ['"""test""" string',
                 [Token(tag='literal', value='test'), Token(tag='raw', value=' string')]
                 ],
                ["""'test"  string'""",
                 [Token(tag='literal', value='test"  string')]
                 ],
                 ]

        for c,e in cases:
            result = list(tokenizer.extractStringLiterals(c))
            self.assertEqual(result,e)


class TestTokenizer(unittest.TestCase):
    def test_tokenize(self):
        cases = [
                 ['define http:',
                  [Token('define','define'),
                   Token('raw','http'),
                   Token(':',':')]
                  ],
                 ['receive(req):',
                  [Token('raw','receive'),
                   Token('()','('),
                   Token('raw','req'),
                   Token('()',')'),
                   Token(':',':')]
                  ],
                 ['switch req.folder:',
                  [Token('switch','switch'),
                   Token('raw','req'),
                   Token('.','.'),
                   Token('raw','folder'),
                   Token(':',':')]
                  ],
                 ["'flic':",
                  [Token('literal','flic'),
                   Token(':',':')]
                  ],
                 ['req -> flic.receive',
                  [Token('raw','req'),
                   Token('->','->'),
                   Token('raw','flic'),
                   Token('.','.'),
                   Token('raw','receive')]
                  ],
                 ['init:',
                  [Token('init','init'),
                   Token(':',':')]
                  ],
                 ['receive(service,status):',
                  [Token('raw','receive'),
                   Token('()','('),
                   Token('raw','service'),
                   Token(',',','),
                   Token('raw','status'),
                   Token('()',')'),
                   Token(':',':')]
                  ],
                 ['send(userID,message):',
                  [Token('raw','send'),
                   Token('()','('),
                   Token('raw','userID'),
                   Token(',',','),
                   Token('raw','message'),
                   Token('()',')'),
                   Token(':',':')]
                  ],
                 ["{'type':'post','url':url+accessToken,'data':data} -> http.send",
                  [Token('{}',      '{'),
                   Token('literal', 'type'),
                   Token(':',       ':'),
                   Token('literal', 'post'),
                   Token(',',       ','),
                   Token('literal', 'url'),
                   Token(':',       ':'),
                   Token('raw',     'url'),
                   Token('+-',       '+'),
                   Token('raw',     'accessToken'),
                   Token(',',       ','),
                   Token('literal', 'data'),
                   Token(':',       ':'),
                   Token('raw',     'data'),
                   Token('{}',      '}'),
                   Token('->',      '->'),
                   Token('raw',     'http'),
                   Token('.',       '.'),
                   Token('raw',     'send')]
                  ],
                 ["self.creds['lifx']     ->     lifx.setToken",
                  [Token('self',    'self'),
                   Token('.',       '.'),
                   Token('raw',     'creds'),
                   Token('[]',      '['),
                   Token('literal', 'lifx'),
                   Token('[]',      ']'),
                   Token('->',      '->'),
                   Token('raw',     'lifx'),
                   Token('.',       '.'),
                   Token('raw',     'setToken')]
                  ],
                   ]

        self.maxDiff = None

        for c,e in cases:
            result = tokenizer.tokenize(c)
            self.assertEqual(result,e)

# -------------------------------------
# -------- TEST TREE GENERATOR --------
# -------------------------------------

class TestFetchFile(unittest.TestCase):
    def setUp(self):
        # temporary directory
        self.test_dir = tempfile.mkdtemp()

        # temporary file
        with open(path.join(self.test_dir, 'test.swarm'), 'w') as f:
            f.write('\n'.join(['aaa',
                               '    bbb',
                               '    ccc']))

    def tearDown(self):
        # remove directory
        shutil.rmtree(self.test_dir)

    def test_something(self):
        results = []
        for line in tree.fetchfile(path.join(self.test_dir, 'test.swarm')):
            results.append(line)

        expected = ['aaa\n',
                    '    bbb\n',
                    '    ccc']

        self.assertEqual(results,expected)

class TestFileLoading(unittest.TestCase):
    def test_file_load(self):
        self.maxDiff = None

        code = '\n'.join(['define stuff:',
                          '    init:',
                          '        3 -> print #print',
                          '',
                          '   # taking awkward space',
                          '    run(n): #run',
                          '        n*2 -> test'])

        result = tree.loadfile(code.split('\n'))

        expected = [(0,
                     [Token('define', 'define'),
                      Token('raw',    'stuff'),
                      Token(':',      ':')]
                     ),
                    (4,
                     [Token('init',   'init'),
                      Token(':',      ':')]
                     ),
                    (8,
                     [Token('raw',    '3'),
                      Token('->',     '->'),
                      Token('raw',    'print')]
                     ),
                    (4,
                     [Token('run',    'run'),
                      Token('()',     '('),
                      Token('raw',    'n'),
                      Token('()',     ')'),
                      Token(':',      ':')]
                     ),
                    (8,
                     [Token('raw',    'n'),
                      Token('*/',     '*'),
                      Token('raw',    '2'),
                      Token('->',     '->'),
                      Token('raw',    'test')]
                     )
                    ]

        self.assertEqual(result,expected)


Node = tree.Node

class TestNodeClass(unittest.TestCase):
    def test_node_class(self):
        a = Node(0,'a')
        b = Node(4,'b')
        c = Node(4,'c')
        a.add(b)
        a.add(c)

    def test_tree_folding(self):
        example = [(0,'aaa'),
                       (4,'bbb'),
                           (8,'ccc'),
                           (8,'ddd'),
                       (4,'eee'),
                           (8,'fff'),
                   (0,'ggg'),
                       (4,'hhh'),
                       (4,'iii'),
                   (0,'jjj')]

        p = tree.tree(example)
        self.assertEqual(len(p.children),3)

        a = p.children[0]
        b = a.children[0]
        c = b.children[0]
        d = b.children[1]
        e = a.children[1]
        f = e.children[0]
        g = p.children[1]
        h = g.children[0]
        i = g.children[1]
        j = p.children[2]

        self.assertEqual(a.code,'aaa')
        self.assertEqual(b.code,'bbb')
        self.assertEqual(c.code,'ccc')
        self.assertEqual(d.code,'ddd')
        self.assertEqual(e.code,'eee')
        self.assertEqual(f.code,'fff')
        self.assertEqual(g.code,'ggg')
        self.assertEqual(h.code,'hhh')
        self.assertEqual(i.code,'iii')
        self.assertEqual(j.code,'jjj')

        self.assertEqual(len(p.children),3)
        self.assertEqual(p.children[0].code,'aaa')
        self.assertEqual(p.children[1].code,'ggg')
        self.assertEqual(p.children[2].code,'jjj')

        self.assertEqual(len(a.children),2)
        self.assertEqual(a.children[0].code,'bbb')
        self.assertEqual(a.children[1].code,'eee')

        self.assertEqual(len(b.children),2)
        self.assertEqual(b.children[0].code,'ccc')
        self.assertEqual(b.children[1].code,'ddd')

        self.assertEqual(len(c.children),0)

        self.assertEqual(len(d.children),0)

        self.assertEqual(len(e.children),1)
        self.assertEqual(e.children[0].code,'fff')

        self.assertEqual(len(f.children),0)

        self.assertEqual(len(g.children),2)
        self.assertEqual(g.children[0].code,'hhh')
        self.assertEqual(g.children[1].code,'iii')

        self.assertEqual(len(h.children),0)

        self.assertEqual(len(i.children),0)

        self.assertEqual(len(j.children),0)
















if __name__ == '__main__':
    unittest.main()



