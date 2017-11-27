import unittest

from context import build_program
from context import build_expressions
from context import build_primitives
from context import build_structures
from context import build_lines


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


unittest.main()

