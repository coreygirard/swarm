import unittest
import build_program
import build_expressions
import build_primitives
import build_structures
import build_program
import build_lines


class TestPrimitives(unittest.TestCase):
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




class TestExpressions2(unittest.TestCase):
    def test_basic_addition_and_subtraction(self):
        a = build_primitives.PrimitiveLiteral(4)
        b = build_primitives.PrimitiveLiteral(5)
        e = build_primitives.ExpressionAdd([['+',a],
                                            ['+',b]])
        self.assertEqual(e.exe(),9)

        a = build_primitives.PrimitiveLiteral(4)
        b = build_primitives.PrimitiveLiteral(5)
        e = build_primitives.ExpressionAdd([['-',a],
                                            ['+',b]])
        self.assertEqual(e.exe(),1)

        a = build_primitives.PrimitiveLiteral(4)
        b = build_primitives.PrimitiveLiteral(5)
        e = build_primitives.ExpressionAdd([['+',a],
                                            ['-',b]])
        self.assertEqual(e.exe(),-1)

        a = build_primitives.PrimitiveLiteral(4)
        b = build_primitives.PrimitiveLiteral(5)
        e = build_primitives.ExpressionAdd([['-',a],
                                            ['-',b]])
        self.assertEqual(e.exe(),-9)

        # making sure double negatives play nice
        a = build_primitives.PrimitiveLiteral(-4)
        b = build_primitives.PrimitiveLiteral(-5)
        e = build_primitives.ExpressionAdd([['+',a],
                                            ['-',b]])
        self.assertEqual(e.exe(),1)

        # complicated
        a = ['+','-','-','+','+','+','-']
        b = [build_primitives.PrimitiveLiteral(i) for i in [-5,3,8,-55,2,8,5]]
        e = build_primitives.ExpressionAdd(list(zip(a,b)))
        self.assertEqual(e.exe(),-66)

    def test_basic_multiplication_and_division(self):
        a = build_primitives.PrimitiveLiteral(4)
        b = build_primitives.PrimitiveLiteral(5)
        e = build_primitives.ExpressionMult([['*',a],
                                             ['*',b]])
        self.assertEqual(e.exe(),4*5)

        a = build_primitives.PrimitiveLiteral(4)
        b = build_primitives.PrimitiveLiteral(5)
        e = build_primitives.ExpressionMult([['*',a],
                                             ['/',b]])
        self.assertEqual(e.exe(),4/5)

        a = build_primitives.PrimitiveLiteral(4)
        b = build_primitives.PrimitiveLiteral(5)
        e = build_primitives.ExpressionMult([['/',a],
                                             ['*',b]])
        self.assertEqual(e.exe(),5/4)


        # complicated
        a = ['*','/','/','*','*','*','/']
        b = [build_primitives.PrimitiveLiteral(i) for i in [-5,3,8,-55,2,8,5]]
        e = build_primitives.ExpressionMult(list(zip(a,b)))
        self.assertEqual(e.exe(),-5/3/8*-55*2*8/5)

    def test_basic_exponentiation(self):
        for i in range(-5,6):
            for j in range(-5,6):
                if not (i == 0 and j < 0):
                    a = build_primitives.PrimitiveLiteral(i)
                    b = build_primitives.PrimitiveLiteral(j)

                    e = build_primitives.ExpressionExponent(a,b)
                    self.assertEqual(e.exe(),i**j)



