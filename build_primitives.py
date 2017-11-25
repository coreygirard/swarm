

# --------------------------------------------------------
# -------- VARIABLE-LEVEL --------------------------------
# --------------------------------------------------------

class PrimitiveLiteral(object):
    def __init__(self,v):
        self.v = v

    def exe(self):
        return self.v

class PrimitiveReference(object):
    def __init__(self,k,ptr):
        self.k = k
        self.ptr = ptr

    def exe(self):
        return self.ptr.get(self.k)

    def set(self,v):
        self.ptr.set(self.k,v)

# --------------------------------------------------------
# -------- BASIC OPERATIONS ------------------------------
# --------------------------------------------------------

class PrimitiveSend(object):
    def __init__(self,left,right):
        self.left = left
        self.right = right

    def exe(self):
        self.right.recv(self.left.exe())

class PrimitiveAssign(object):
    def __init__(self,left,right):
        self.left = left
        self.right = right

    def exe(self):
        self.left.set(self.right.exe())

# --------------------------------------------------------
# -------- LOOPS -----------------------------------------
# --------------------------------------------------------


class PrimitiveFor(object):
    def __init__(self,variable,iterator,children):
        self.variable = variable
        self.iterator = iterator
        self.children = children

    def exe(self):
        for i in self.iterator.iterate():
            self.variable.set([i])
            for c in self.children:
                c.exe()

class PrimitiveWhile(object):
    def __init__(self,condition,scope,children):
        self.condition = condition
        self.scope = scope
        self.children = children

    def exe(self):
        while self.condition.exe():
            for c in self.children:
                c.exe()

# --------------------------------------------------------
# -------- COMPARISONS -----------------------------------
# --------------------------------------------------------

class PrimitiveComparison(object):
    def __init__(self,left,op,right):
        self.left = left
        self.op = op
        self.right = right

    def exe(self):
        return self.op(self.left.exe(),self.right.exe())

# --------------------------------------------------------
# -------- RANGES ----------------------------------------
# --------------------------------------------------------

class PrimitiveRange(object):
    def __init__(self,*args):
        if len(args) == 4:
            a,b,d,e = args
            c = 1
        elif len(args) == 5:
            a,b,c,d,e = args

        self.step = c

        if a == '(':
            self.start = b + c
        else:
            self.start = b

        if e == ')':
            if c > 0:
                self.stop = d - 1 # note deliberate asymmetry here
            elif c < 0:
                self.stop = d + 1
        else:
            self.stop = d

    def iterate(self):
        i = self.start
        # TODO: YUCK
        while (self.step > 0 and i <= self.stop) or (self.step < 0 and i >= self.stop):
            yield i
            i += self.step

# --------------------------------------------------------
# -------- EXPRESSION ATOMS ------------------------------
# --------------------------------------------------------

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








