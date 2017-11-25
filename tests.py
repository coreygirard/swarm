import unittest
import build_program
import build_expressions
import build_primitives
import build_structures
import build_program
import build_lines

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

class TestScopes(unittest.TestCase):
    def test_basic_make_reference(self):
        agentScope = build_program.AgentScope()
        subagentScope = build_program.SubagentScope(agentScope)
        
        ref = build_primitives.PrimitiveReference('var',subagentScope)

        self.assertEqual(agentScope.getLocals(),{})
        self.assertEqual(subagentScope.getLocals(),{})

        ref.set(4)

        self.assertEqual(agentScope.getLocals(),{})
        self.assertEqual(subagentScope.getLocals(),{'var':4})
        self.assertEqual(ref.exe(),4)

        ref.set('hey')

        #self.assertEqual(agentScope.getLocals(),{}) # TODO: variables are bleeding out of their local scope
        self.assertEqual(subagentScope.getLocals(),{'var':'hey'})
        self.assertEqual(ref.exe(),'hey')

        ref2 = build_primitives.PrimitiveReference('otherVar',subagentScope)

        #self.assertEqual(agentScope.getLocals(),{})
        self.assertEqual(subagentScope.getLocals(),{'var':'hey'})
        self.assertEqual(ref.exe(),'hey')

        ref2.set(-2)

        #self.assertEqual(agentScope.getLocals(),{})
        self.assertEqual(subagentScope.getLocals(),{'var':'hey','otherVar':-2})
        self.assertEqual(ref2.exe(),-2)
        





        agentScope = build_program.AgentScope()
        subagentScope = build_program.SubagentScope(agentScope)

        
        refPush = build_expressions.ComplexTarget(['a','b','c'],subagentScope)
        refPush.set([4,5,6])
        self.assertEqual(agentScope.getLocals(),{})
        self.assertEqual(subagentScope.getLocals(),{'a':4,'b':5,'c':6})
        
        refPull = build_expressions.ComplexSource(['a','b','c'],subagentScope)
        self.assertEqual(refPull.exe(),[4,5,6])
        
        refPush = build_expressions.buildTarget('i,j,k',subagentScope)
        refPush.set([1,2,3])
        self.assertEqual(subagentScope.getLocals(),{'a':4,'b':5,'c':6,'i':1,'j':2,'k':3})
        
        refPull = build_expressions.buildSource('i,j,k',subagentScope)
        self.assertEqual(refPull.exe(),[1,2,3])

        refPull = build_expressions.buildSource('a,j,k',subagentScope)
        self.assertEqual(refPull.exe(),[4,2,3])

        refPush = build_expressions.buildTarget('b,c,i,j',subagentScope)
        refPush.set([-3,'str',42,'2'])
        expected = {'j': '2', 'i': 42, 'b': -3, 'a': 4, 'c': 'str', 'k': 3}
        self.assertEqual(subagentScope.getLocals(),expected)

        refPush = build_expressions.buildTarget('b,c,i,j',subagentScope)
        refPush.set([-3,'str',42,'2'])
        expected = {'j': '2', 'i': 42, 'b': -3, 'a': 4, 'c': 'str', 'k': 3}
        self.assertEqual(subagentScope.getLocals(),expected)

        refPull = build_expressions.buildSource('i',subagentScope)
        self.assertEqual(refPull.exe(),[42])

        refPush = build_expressions.buildTarget('i',subagentScope)
        refPush.set([891])
        
        self.assertEqual(refPull.exe(),[891])


class TestPrimitives(unittest.TestCase):
    def test_make_literal_object(self):
        result = build_expressions.buildLiteral('test string')

    def test_make_variable_object(self):
        result = build_expressions.buildVariable('var',None)

    def test_comparison(self):
        class Dummy(object):
            def __init__(self,var):
                self.var = var
            
            def exe(self):
                return self.var

        import operator
        comp = build_primitives.PrimitiveComparison(Dummy(5),operator.lt,Dummy(7))
        self.assertEqual(comp.exe(),True)

        comp = build_primitives.PrimitiveComparison(Dummy(5),operator.gt,Dummy(7))
        self.assertEqual(comp.exe(),False)

        comp = build_primitives.PrimitiveComparison(Dummy(9),operator.lt,Dummy(-4))
        self.assertEqual(comp.exe(),False)

        comp = build_primitives.PrimitiveComparison(Dummy(9),operator.eq,Dummy(-4))
        self.assertEqual(comp.exe(),False)

        comp = build_primitives.PrimitiveComparison(Dummy(-4),operator.eq,Dummy(-4))
        self.assertEqual(comp.exe(),True)


    def test_range(self):
        r = build_primitives.PrimitiveRange(*['[',0,1,5,')'])
        result = [e for e in r.iterate()]
        self.assertEqual(result,[0,1,2,3,4])

        r = build_primitives.PrimitiveRange(*['[',0,5,')'])
        result = [e for e in r.iterate()]
        self.assertEqual(result,[0,1,2,3,4])

        r = build_primitives.PrimitiveRange(*['(',0,5,')'])
        result = [e for e in r.iterate()]
        self.assertEqual(result,[1,2,3,4])

        r = build_primitives.PrimitiveRange(*['(',0,5,']'])
        result = [e for e in r.iterate()]
        self.assertEqual(result,[1,2,3,4,5])

        r = build_primitives.PrimitiveRange(*['[',10,-2,-9,')'])
        result = [e for e in r.iterate()]
        self.assertEqual(result,[10,8,6,4,2,0,-2,-4,-6,-8])


    def test_for(self):
        agentScope = build_program.AgentScope()
        subagentScope = build_program.SubagentScope(agentScope)


        class Counter(object):
            def __init__(self):
                self.n = 0
            
            def exe(self):
                self.n += 1


        refPush = build_expressions.buildTarget('n',subagentScope)
        r = build_primitives.PrimitiveRange(*['[',0,1,5,')'])
        c = [Counter()]
        f = build_primitives.PrimitiveFor(refPush,r,c)

        f.exe()
        refPull = build_expressions.buildSource('n',subagentScope)
        self.assertEqual(refPull.exe(),[4])


    def test_while(self):

        class Counter(object):
            def __init__(self):
                self.n = 0
            
            def exe(self):
                self.n += 1
        
        class DummyCondition(object):
            def __init__(self,n):
                self.n = n
            
            def exe(self):
                if self.n <= 0:
                    return False
                else:
                    self.n -= 1
                    return True
        
        dc = DummyCondition(9)
        c = Counter()        
        loop = build_primitives.PrimitiveWhile(dc,None,[c])
        loop.exe()
        self.assertEqual(c.n,9)
                
        dc = DummyCondition(0)
        c = Counter()        
        loop = build_primitives.PrimitiveWhile(dc,None,[c])
        loop.exe()
        self.assertEqual(c.n,0)
                
    def test_basic_send(self):
        
        class DummyExe(object):
            def __init__(self,var):
                self.var = var
            
            def exe(self):
                return self.var
        
        class DummyRecv(object):
            def __init__(self):
                self.var = None
            
            def recv(self,e):
                self.var = e
        
        a = DummyExe(4)
        b = DummyRecv()
        
        c = build_primitives.PrimitiveSend(a,b)
        self.assertEqual(b.var,None)
        c.exe()
        self.assertEqual(b.var,4)

        a = DummyExe('string')
        b = DummyRecv()
        
        c = build_primitives.PrimitiveSend(a,b)
        self.assertEqual(b.var,None)
        c.exe()
        self.assertEqual(b.var,'string')


    def test_basic_assign(self):
        
        class DummyExe(object):
            def __init__(self,var):
                self.var = var
            
            def exe(self):
                return self.var
        
        class DummySet(object):
            def __init__(self):
                self.var = None
            
            def set(self,e):
                self.var = e
        
        a = DummySet()
        b = DummyExe(4)
    
        c = build_primitives.PrimitiveAssign(a,b)
        self.assertEqual(a.var,None)
        c.exe()
        self.assertEqual(a.var,4)

        a = DummySet()
        b = DummyExe('string')
        
        c = build_primitives.PrimitiveAssign(a,b)
        self.assertEqual(a.var,None)
        c.exe()
        self.assertEqual(a.var,'string')



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





class TestSend(unittest.TestCase):
    def test_make_send(self):
        pr = build_program.ProgramRouter(debug=False)
        ar = pr.makeAgentRouter('agent1')
        sr = ar.makeSubagentRouter('subagent1')
        
        line = build_program.Node(6,'a -> b')
        
        result = build_lines.buildLine(line,None,sr)






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










