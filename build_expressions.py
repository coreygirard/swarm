import re
import operator
import build_primitives as primitives


class Literal(object):
    def __init__(self,val):
        self.val = val

    def exe(self):
        return self.val
    
    def __repr__(self):
        return 'Literal(' + str(self.val) + ')'

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

def buildLiteralsAndVariables(e,scope):
    temp = []
    for i in e:
        i = i.strip()
        if re.fullmatch(r'([0-9]+)',i):
            temp.append(primitives.PrimitiveLiteral(int(i))) # TODO: handle non-ints
        elif re.fullmatch(r'([a-zA-Z0-9]+)',i):
            temp.append(primitives.PrimitiveReference(i,scope))
        else:
            temp.append(i)
    e = temp
    return e

def tokenizeExpression(e,scope):
    e = [e]
    for symbol in ['<=','>=','==','[*]{2}','\(','\)','(?<![*])[*](?![*])','[-]','[+]','[/]','[<]','[>]']:
        temp = []
        for i in e:
            temp = temp + [a.strip() for a in re.split(r'(' + symbol + ')',i) if a.strip() != '']
        e = temp

    print(e)
    e = buildLiteralsAndVariables(e,scope)
    return e

def collapse(e,op,c):
    if e[0] not in op:
        e.insert(0,op[0])
    indices = [i for i,x in enumerate(e) if x in op]+[len(e)]
    inputs = []
    for a,b in zip(indices,indices[1:]):
        inputs.append([e[a],recurse(e[a+1:b])])
    return c(inputs)

def recurse(exp):    
    print(exp)
    
    assert(exp.count('(') == exp.count(')'))
    
    # reduce parenthetical expressions to single values
    while '(' in exp:
        i = exp.index('(')
        a = exp[:i]
        b = [exp[i]]
        c = exp[i+1:]
        while b.count('(') != b.count(')'):
            b.append(c.pop(0))
        b = recurse(b[1:-1])
        exp = a+[b]+c

    if len(exp) == 1:
        return exp[0]
        
    assert(sum([s in exp for s in ['<','>','==','!=','<=','>=']]) <= 1) # TODO: add support for expressions like 'A < B < C'
    if any([s in exp for s in ['<','>','==','!=','<=','>=']]):
        for char,f in {'<':operator.lt,
                       '>':operator.gt,
                       '==':operator.eq,
                       '!=':operator.ne,
                       '<=':operator.le,
                       '>=':operator.ge}.items():
            if char in exp:
                i = exp.index(char)
                a = recurse(exp[:i])
                b = recurse(exp[i+1:])
                return primitives.PrimitiveComparison(a,f,b)
            
    
    if len(exp) == 1:
        return exp[0]

    # reduce exponential expressions to single values
    while '**' in exp:
        indices = [i for i,x in enumerate(exp) if x == '**']
        i = indices[-1]
        exp[i-1] = ExpressionExponent(exp[i-1],exp[i+1])
        del exp[i:i+2]

    if len(exp) == 1:
        return exp[0]

    # reduce -n notation to single values
    indices = [i for i,x in enumerate(exp) if x == '-']
    for i in reversed(indices):
        if i == 0 or type(exp[i-1]) == type('str'):
            exp[i] = ExpressionAdd([['-',exp[i+1]]])
            del exp[i+1]

    # reduce +n notation to single values
    indices = [i for i,x in enumerate(exp) if x == '+']
    for i in reversed(indices):
        if i == 0 or type(exp[i-1]) == type('str'):
            exp[i] = ExpressionAdd([['+',exp[i+1]]])
            del exp[i+1]

    if len(exp) == 1:
        return exp[0]

    if '+' in exp or '-' in exp:
        return collapse(exp,['+','-'],ExpressionAdd)
    if '*' in exp or '/' in exp:
        return collapse(exp,['*','/'],ExpressionMult)

    raise Exception('invalid expression')

def buildSimpleExpression(e,scope):
    e = tokenizeExpression(e,scope)
    e = recurse(e)
    return e

class ComplexExpression(object):
    def __init__(self,exp,scope):
        self.exp = [buildSimpleExpression(e,scope) for e in exp]
        
    def exe(self):
        if len(self.exp) == 1:
            return self.exp[0].exe()
        else:
            return [e.exe() for e in self.exp]

def buildExpression(e,scope):
    e = [i for i in e.split(',') if i != '']
    return ComplexExpression(e,scope)









class ComplexReference(object):
    def __init__(self,k,scope):
        self.ref = [primitives.PrimitiveReference(i,scope) for i in k]
    
    def set(self,v):
        if len(self.ref) == 1:
            self.ref[0].set(v)
        else:
            assert(len(v) == len(self.ref))
            for a,b in zip(self.ref,v):
                a.set(b)
        
def buildReference(e,scope):
    e = [i for i in e.split(',') if i != '']
    return ComplexReference(e,scope)













