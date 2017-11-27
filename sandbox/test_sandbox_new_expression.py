import unittest
import sandbox_new_expression

class TestStage1(unittest.TestCase):
    def test_basic_exp_split(self):
        basics = [('4',['4']),
                  ('4 + 1',['4','+','1']),
                  ('42 + 13',['42','+','13'])]

        for i,expected in basics:
            result = sandbox_new_expression.stage1(i)
            self.assertEqual(result,expected)




class TestStage4(unittest.TestCase):
    '''
    def test_basic_parsing(self):
        exp = '4'
        result = sandbox_new_expression.parseExpression(exp)
        expected = sandbox_new_expression.makeLiteral(sandbox_new_expression.Token('literal',4))
        self.assertEqual(type(result),type(expected))
        self.assertEqual(result.exe(),expected.exe())

        exp = '4+5'
        result = sandbox_new_expression.parseExpression(exp)
        a = sandbox_new_expression.makeLiteral(sandbox_new_expression.Token('literal',4))
        a = sandbox_new_expression.makeLiteral(sandbox_new_expression.Token('literal',5))
        expected = sandbox_new_expression.makeAddSub('4')
        self.assertEqual(type(result),type(expected))
        self.assertEqual(result.exe(),expected.exe())
        '''

    def test_combining_terms_without_parentheses(self):
        # 4 + 1 => 5
        Token = sandbox_new_expression.Token
        PrimitiveLiteral = sandbox_new_expression.PrimitiveLiteral
        i = [Token('object', PrimitiveLiteral(4)),
             Token(tag='+-', value='+'),
             Token('object', PrimitiveLiteral(1))]
        r = sandbox_new_expression.stage4(i)
        self.assertEqual(r.exe(),5)

        # 4 - 1 => 3
        Token = sandbox_new_expression.Token
        PrimitiveLiteral = sandbox_new_expression.PrimitiveLiteral
        i = [Token('object', PrimitiveLiteral(4)),
             Token(tag='+-', value='-'),
             Token('object', PrimitiveLiteral(1))]
        r = sandbox_new_expression.stage4(i)
        self.assertEqual(r.exe(),3)

        # 2 ** 3 => 8
        Token = sandbox_new_expression.Token
        PrimitiveLiteral = sandbox_new_expression.PrimitiveLiteral
        i = [Token('object', PrimitiveLiteral(2)),
             Token(tag='**', value='**'),
             Token('object', PrimitiveLiteral(3))]
        r = sandbox_new_expression.stage4(i)
        self.assertEqual(r.exe(),8)

        # 2 + 2 ** 3 => 10
        Token = sandbox_new_expression.Token
        PrimitiveLiteral = sandbox_new_expression.PrimitiveLiteral
        i = [Token('object', PrimitiveLiteral(2)),
             Token(tag='+-', value='+'),
             Token('object', PrimitiveLiteral(2)),
             Token(tag='**', value='**'),
             Token('object', PrimitiveLiteral(3))]
        r = sandbox_new_expression.stage4(i)
        self.assertEqual(r.exe(),10)

    '''
    def test_combining_terms_with_parentheses(self):
        # ( 4 ) => 4
        Token = sandbox_new_expression.Token
        PrimitiveLiteral = sandbox_new_expression.PrimitiveLiteral
        i = [Token('()', '('),
             Token('object', PrimitiveLiteral(4)),
             Token('()', ')')]
        r = sandbox_new_expression.stage4(i)
        self.assertEqual(r.exe(),4)
    '''




if __name__ == '__main__':
    unittest.main()

