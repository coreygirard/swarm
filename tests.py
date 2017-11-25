import unittest
import build_program
import build_expressions
import build_primitives
import build_structures
import build_program

class TestProgram(unittest.TestCase):
    def test_loading_file(self):
        exampleProgram = '''
        define example:
            init:
                42 -> print
        '''
        exampleProgram = exampleProgram.split('\n')

        f = list(build_program.loadfile(exampleProgram))

        # loadfile should return Nodes with no children
        for e in f:
            self.assertEqual(type(e),type(build_program.Node(0,'')))
            self.assertEqual(e.children,[])

        #t = build_program.tree(f)


class TestExpressions(unittest.TestCase):
    def test_finding_string_ends(self):
        s = 'this is a simple string'
        result = list(build_expressions.findStringEnds(s))
        expected = ['t','h','i','s',' ','i','s',' ','a',' ','s','i','m','p','l','e',' ','s','t','r','i','n','g']
        self.assertEqual(result,expected)

        s = 'this is a simple "string"'
        result = list(build_expressions.findStringEnds(s))
        expected = list('this is a simple ') + [('"',),'s','t','r','i','n','g',('"',)]
        self.assertEqual(result,expected)

        s = 'this is a simple """string"""'
        result = list(build_expressions.findStringEnds(s))
        expected = list('this is a simple ') + [('"""',),'s','t','r','i','n','g',('"""',)]
        self.assertEqual(result,expected)

        s = "this is a simple string"
        result = list(build_expressions.findStringEnds(s))
        expected = list('this is a simple string')
        self.assertEqual(result,expected)

        s = "this is a simple 'string'"
        result = list(build_expressions.findStringEnds(s))
        expected = list('this is a simple ') + [("'",),'s','t','r','i','n','g',("'",)]
        self.assertEqual(result,expected)

        s = "this is a simple '''string'''"
        result = list(build_expressions.findStringEnds(s))
        expected = list('this is a simple ') + [("'''",),'s','t','r','i','n','g',("'''",)]
        self.assertEqual(result,expected)

    def test_finding_multiple_string_ends(self):
        s = 'this "is" a "simple" string'
        result = list(build_expressions.findStringEnds(s))
        expected = list('this ') + [('"',),'i','s',('"',)] + list(' a ') + [('"',),'s','i','m','p','l','e',('"',)] + list(' string')
        self.assertEqual(result,expected)
    
        s = "this 'is' a 'simple' string"
        result = list(build_expressions.findStringEnds(s))
        expected = list('this ') + [("'",),'i','s',("'",)] + list(' a ') + [("'",),'s','i','m','p','l','e',("'",)] + list(' string')
        self.assertEqual(result,expected)
    
    def test_handling_interleaved_strings(self):
        s = '''this "i's" a "sim'ple" string'''
        result = list(build_expressions.findStringEnds(s))
        expected = list('this ') + [('"',),'i',("'",),'s',('"',)] + list(' a ') + [('"',),'s','i','m',("'",),'p','l','e',('"',)] + list(' string')
        self.assertEqual(result,expected)
    
    def test_weird_edge_cases(self):
        s = ''
        result = list(build_expressions.findStringEnds(s))
        expected = []
        self.assertEqual(result,expected)
        
        s = "''"
        result = list(build_expressions.findStringEnds(s))
        expected = [("'",),("'",)]
        self.assertEqual(result,expected)
        
        s = '""'
        result = list(build_expressions.findStringEnds(s))
        expected = [('"',),('"',)]
        self.assertEqual(result,expected)
        
        s = "''''''"
        result = list(build_expressions.findStringEnds(s))
        expected = [("'''",),("'''",)]
        self.assertEqual(result,expected)
        
        s = '""""""'
        result = list(build_expressions.findStringEnds(s))
        expected = [('"""',),('"""',)]
        self.assertEqual(result,expected)
        
        # a non-empty string that takes up the entire expression
        s = "'this is a test string'"
        result = list(build_expressions.findStringEnds(s))
        expected = [("'",)] + list('this is a test string') + [("'",)]
        self.assertEqual(result,expected)
        
        s = '"this is a test string"'
        result = list(build_expressions.findStringEnds(s))
        expected = [('"',)] + list('this is a test string') + [('"',)]
        self.assertEqual(result,expected)
        
        s = "'''this is a test string'''"
        result = list(build_expressions.findStringEnds(s))
        expected = [("'''",)] + list('this is a test string') + [("'''",)]
        self.assertEqual(result,expected)
        
        s = '"""this is a test string"""'
        result = list(build_expressions.findStringEnds(s))
        expected = [('"""',)] + list('this is a test string') + [('"""',)]
        self.assertEqual(result,expected)
        
    def test_basic_string_extracting(self):
        s = ''
        result = build_expressions.extractStringLiterals(s)
        expected = []
        self.assertEqual(result,expected)

        # test all empty string literals
        s = '""'
        result = build_expressions.extractStringLiterals(s)
        expected = [('literal', '')]
        self.assertEqual(result,expected)
    
        s = '""""""'
        result = build_expressions.extractStringLiterals(s)
        expected = [('literal', '')]
        self.assertEqual(result,expected)
    
        s = "''"
        result = build_expressions.extractStringLiterals(s)
        expected = [('literal', '')]
        self.assertEqual(result,expected)
    
        s = "''''''"
        result = build_expressions.extractStringLiterals(s)
        expected = [('literal', '')]
        self.assertEqual(result,expected)

        # test all empty string literals with non-literal afterward
        s = '"" test'
        result = build_expressions.extractStringLiterals(s)
        expected = [('literal', ''),' test']
        self.assertEqual(result,expected)
    
        s = '"""""" test'
        result = build_expressions.extractStringLiterals(s)
        expected = [('literal', ''),' test']
        self.assertEqual(result,expected)
    
        s = "'' test"
        result = build_expressions.extractStringLiterals(s)
        expected = [('literal', ''),' test']
        self.assertEqual(result,expected)
    
        s = "'''''' test"
        result = build_expressions.extractStringLiterals(s)
        expected = [('literal', ''),' test']
        self.assertEqual(result,expected)

        # test all empty string literals with non-literal before
        s = 'test ""'
        result = build_expressions.extractStringLiterals(s)
        expected = ['test ',('literal', '')]
        self.assertEqual(result,expected)
    
        s = 'test """"""'
        result = build_expressions.extractStringLiterals(s)
        expected = ['test ',('literal', '')]
        self.assertEqual(result,expected)
    
        s = "test ''"
        result = build_expressions.extractStringLiterals(s)
        expected = ['test ',('literal', '')]
        self.assertEqual(result,expected)
    
        s = "test ''''''"
        result = build_expressions.extractStringLiterals(s)
        expected = ['test ',('literal', '')]
        self.assertEqual(result,expected)

        # test non-empty literal that takes the entire expression
        s = "'this is a test string'"
        result = build_expressions.extractStringLiterals(s)
        expected = [('literal', 'this is a test string')]
        self.assertEqual(result,expected)
    
        s = '"this is a test string"'
        result = build_expressions.extractStringLiterals(s)
        expected = [('literal', 'this is a test string')]
        self.assertEqual(result,expected)
    
        s = "'''this is a test string'''"
        result = build_expressions.extractStringLiterals(s)
        expected = [('literal', 'this is a test string')]
        self.assertEqual(result,expected)
    
        s = '"""this is a test string"""'
        result = build_expressions.extractStringLiterals(s)
        expected = [('literal', 'this is a test string')]
        self.assertEqual(result,expected)



        #test non-empty literal with non-literal before and after
        s = "test 'this is a test string' test"
        result = build_expressions.extractStringLiterals(s)
        expected = ['test ',('literal', 'this is a test string'),' test']
        self.assertEqual(result,expected)
    
        s = 'test "this is a test string" test'
        result = build_expressions.extractStringLiterals(s)
        expected = ['test ',('literal', 'this is a test string'),' test']
        self.assertEqual(result,expected)
    
        s = "test '''this is a test string''' test"
        result = build_expressions.extractStringLiterals(s)
        expected = ['test ',('literal', 'this is a test string'),' test']
        self.assertEqual(result,expected)
    
        s = 'test """this is a test string""" test'
        result = build_expressions.extractStringLiterals(s)
        expected = ['test ',('literal', 'this is a test string'),' test']
        self.assertEqual(result,expected)
    
    def test_overlapping_string_extracting(self):
        s = '''aaa 'bbb "ccc' 'ddd" eee' fff'''
        result = build_expressions.extractStringLiterals(s)
        expected = ['aaa ',('literal','bbb "ccc'),' ',('literal','ddd" eee'),' fff']
        self.assertEqual(result,expected)

        s = '''aaa "bbb 'ccc" "ddd' eee" fff'''
        result = build_expressions.extractStringLiterals(s)
        expected = ['aaa ',('literal',"bbb 'ccc"),' ',('literal',"ddd' eee"),' fff']
        self.assertEqual(result,expected)

    def test_odd_string_contents(self):
        s = '''"Let's test this!!"'''
        result = build_expressions.extractStringLiterals(s)
        expected = [('literal', "Let's test this!!")]
        self.assertEqual(result,expected)

        s = """'''We can include ' or " and '', etc'''"""
        result = build_expressions.extractStringLiterals(s)
        expected = [('literal', '''We can include ' or " and '', etc''')]
        self.assertEqual(result,expected)

    def test_basic_tokenize_string(self):
        for k in ['and','or','not','nand','nor','xor','xnor']:
            s = '3 ' + k + ' 4'
            result = build_expressions.tokenizeExpression(s,None)
            self.assertEqual(len(result),3)
            self.assertEqual(result[0].exe(),3)
            self.assertEqual(result[1],(k,))
            self.assertEqual(result[2].exe(),4)

        for sym in ['<=','>=','==','**']+list('-+*/<>!()'):
            s = '3 ' + sym + ' 4'
            result = build_expressions.tokenizeExpression(s,None)
            self.assertEqual(len(result),3)
            self.assertEqual(result[0].exe(),3)
            self.assertEqual(result[1],(sym,))
            self.assertEqual(result[2].exe(),4)

        s = '''true and !false'''
        result = build_expressions.tokenizeExpression(s,None)
        self.assertEqual(len(result),4)
        self.assertEqual(result[0].exe(),True)
        self.assertEqual(result[1],('and',))
        self.assertEqual(result[2],('!',))
        self.assertEqual(result[3].exe(),False)
        
        s = '''var + otherVar - thirdVar * something / another'''
        result = build_expressions.tokenizeExpression(s,None)
        self.assertEqual(len(result),9)
        self.assertEqual(result[0],('variable','var'))
        self.assertEqual(result[2],('variable','otherVar'))
        self.assertEqual(result[4],('variable','thirdVar'))
        self.assertEqual(result[6],('variable','something'))
        self.assertEqual(result[8],('variable','another'))
        
    def test_match_superstring_first(self):
        s = '3 <= var'
        result = build_expressions.tokenizeExpression(s,None)
        self.assertEqual(len(result),3)
        self.assertEqual(result[1],('<=',))

        s = '3 >= var'
        result = build_expressions.tokenizeExpression(s,None)
        self.assertEqual(len(result),3)
        self.assertEqual(result[1],('>=',))

        s = '3 ** var'
        result = build_expressions.tokenizeExpression(s,None)
        self.assertEqual(len(result),3)
        self.assertEqual(result[1],('**',))

    '''
    def test_step_through_addition(self):
        s = '1 + 2 + 3 + 4'
        result = build_expressions.tokenizeExpression(s,None)
        self.assertEqual(len(result),7)
        self.assertEqual(result[0].exe(),1)
        self.assertEqual(result[2].exe(),2)
        self.assertEqual(result[4].exe(),3)
        self.assertEqual(result[6].exe(),4)
        
        self.assertEqual(result[1],('+',))
        self.assertEqual(result[3],('+',))
        self.assertEqual(result[5],('+',))
        
        
        result = build_expressions.recurse(result)
        #self.assertEqual(result,3)
    '''

class TestComplexReference(unittest.TestCase):
    def test_basic_make_reference(self):
        agentScope = build_program.AgentScope()
        subagentScope = build_program.SubagentScope(agentScope)
        
        ref = build_primitives.PrimitiveReference('var',subagentScope)
        self.assertEqual(subagentScope.d,{})
        ref.set(4)
        self.assertEqual(subagentScope.d,{'var':4})
        self.assertEqual(ref.exe(),4)
        ref.set('hey')
        self.assertEqual(subagentScope.d,{'var':'hey'})
        self.assertEqual(ref.exe(),'hey')

        ref2 = build_primitives.PrimitiveReference('otherVar',subagentScope)
        self.assertEqual(subagentScope.d,{'var':'hey'})
        self.assertEqual(ref.exe(),'hey')
        ref2.set(-2)
        self.assertEqual(subagentScope.d,{'var':'hey','otherVar':-2})
        self.assertEqual(ref2.exe(),-2)




class TestPrimitives(unittest.TestCase):
    def test_make_literal_object(self):
        result = build_expressions.buildLiteral('test string')

    def test_make_variable_object(self):
        result = build_expressions.buildVariable('var',None)

class TestRouter(unittest.TestCase):
    def test_basic_routing(self):
        class Dummy(object):
            def __init__(self):
                self.var = None
            
            def recv(self,k):
                self.var = k

        dummy = Dummy()
        
        pr = build_program.ProgramRouter(debug=False)
        ar = {'agent1':pr.makeAgentRouter('agent1'),
              'agent2':pr.makeAgentRouter('agent2')}
        sr = {'agent1.subagent1':ar['agent1'].makeSubagentRouter('subagent1'),
              'agent1.subagent2':ar['agent1'].makeSubagentRouter('subagent2'),
              'agent2.subagent1':ar['agent2'].makeSubagentRouter('subagent1'),
              'agent2.subagent2':ar['agent2'].makeSubagentRouter('subagent2')}
        


        pr.builtins['print'] = dummy

        pr.recv(3,['print'])
        self.assertEqual(dummy.var,3)
        ar['agent1'].recv(4,['print'])
        self.assertEqual(dummy.var,4)
        sr['agent1.subagent1'].recv(5,['print'])
        self.assertEqual(dummy.var,5)


        ep_1_1_1 = sr['agent1.subagent1'].makeEndpoint('print')
        ep_1_1_1.recv('hello')
        self.assertEqual(dummy.var,['hello'])


'''
class TestStructures(unittest.TestCase):
    def test_basic_structure_build(self):
        a = build_program.Node(0,'for n = [0:5):')
        b = build_program.Node(0,'')
        c = build_program.Node(0,'')
        a.add(b)
        a.add(c)
                
        result = build_structures.buildStructure(a,None,None)
        expected = []
        self.assertEqual(result,expected)
'''

if __name__ == '__main__':
    unittest.main()










