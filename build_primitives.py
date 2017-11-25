
class PrimitivePrint(object):
    def __init__(self):
        self.separator = '\n'

    def recv(self,e):
        print(e,end=self.separator)

    def setSeparator(self,c):
        self.separator = c

class PrimitiveSend(object):
    def __init__(self,left,right):
        self.left = left
        self.right = right

    def exe(self):
        self.right.recv(self.left.exe())


class PrimitiveLiteral(object):
    def __init__(self,v):
        self.v = v

    def exe(self):
        return self.v


class PrimitiveAssign(object):
    def __init__(self,left,right):
        self.left = left
        self.right = right

    def exe(self):
        self.left.set(self.right.exe())

class PrimitiveReference(object):
    def __init__(self,k,ptr):
        self.k = k
        self.ptr = ptr

    def exe(self):
        return self.ptr.get(self.k)

    def set(self,v):
        self.ptr.set(self.k,v)



class PrimitiveFor(object):
    def __init__(self,variable,iterator,children):
        self.variable = variable
        self.iterator = iterator
        self.children = children

    def exe(self):
        for i in self.iterator.iterate():
            self.variable.set(i)
            for c in self.children:
                c.exe()

class PrimitiveWhile(object):
    def __init__(self,condition,scope,children):
        self.condition = condition
        self.scope = scope
        self.children = children

    def exe(self):
        #while eval(self.condition,self.scope.getLocals()):
        while self.condition.exe():
            for c in self.children:
                c.exe()

class PrimitiveComparison(object):
    def __init__(self,left,op,right):
        self.left = left
        self.op = op
        self.right = right

    def exe(self):
        return self.op(self.left.exe(),self.right.exe())


class PrimitiveRange(object):
    def __init__(self,*args):
        if len(args) == 4:
            self.l = args[0]
            self.a = args[1]
            self.b = 1
            self.c = args[2]
            self.r = args[3]
        elif len(args) == 5:
            self.l = args[0]
            self.a = args[1]
            self.b = args[2]
            self.c = args[3]
            self.r = args[4]

    def iterate(self):
        start = self.a
        if self.l == '(':
            start = start + self.b
        stop = self.c
        if self.r == ')':
            stop = stop - 1
        t = start
        while t <= stop:
            yield t
            t = t + self.b





class ExpressionAdd(object):
    def __init__(self,inputs):
        self.inputs = inputs

    def exe(self):
        total = 0
        for sign,n in self.inputs:
            assert(sign in ['-','+'])
            if sign == '-':
                total = total - n.exe()
            elif sign == '+':
                total = total + n.exe()
        return total

    def __repr__(self):
        return 'ExpressionAdd(' + str(self.inputs) + ')'

class ExpressionMult(object):
    def __init__(self,inputs):
        self.inputs = inputs

    def exe(self):
        total = 1
        for sign,n in self.inputs:
            assert(sign in ['*','/'])
            if sign == '*':
                total = total * n.exe()
            elif sign == '/':
                total = total / n.exe()
        return total

    def __repr__(self):
        return 'ExpressionMult(' + str(self.inputs) + ')'

class ExpressionExponent(object):
    def __init__(self,a,b):
        self.a = a
        self.b = b

    def exe(self):
        return self.a.exe() ** self.b.exe()

    def __repr__(self):
        return 'ExpressionExponent(' + str(self.a) + '**' + str(self.b) + ')'








