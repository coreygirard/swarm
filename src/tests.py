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
                   Token('+',       '+'),
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

class TestFileLoading(unittest.TestCase):
    def test_file_load(self):
        code = '\n'.join(['define stuff:',
                          '    init:',
                          '        3 -> print #print',
                          '',
                          '   # taking awkward space',
                          '    run(n): #run',
                          '        n*2 -> test'])

        result = tree.loadfile(code.split('\n'))
        expected = [(0, 'define stuff:'),
                    (4, 'init:'),
                    (8, '3 -> print'),
                    (4, 'run(n):'),
                    (8, 'n*2 -> test')]
        self.assertEqual(result,expected)











if __name__ == '__main__':
    unittest.main()



