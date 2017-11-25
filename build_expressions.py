import re
import operator
import build_primitives as primitives





keywords = ['and','or','not','nand','nor','xor','xnor']

def buildLiteralsAndVariables(e,scope):
    temp = []
    for i in e:
        if type(i) != type('str'):
            temp.append(i)
            continue

        i = i.strip()
        if re.fullmatch(r'([0-9]+[.][0-9]+)',i):
            temp.append(primitives.PrimitiveLiteral(float(i)))
        elif re.fullmatch(r'([0-9]+)',i): # integer
            temp.append(primitives.PrimitiveLiteral(int(i)))
            #temp.append(primitives.PrimitiveLiteral(int(i))) # TODO: handle non-ints
        elif re.fullmatch(r'([a-zA-Z0-9]+)',i) and i not in keywords:
            temp.append(primitives.PrimitiveReference(i,scope))
            #temp.append(primitives.PrimitiveReference(i,scope))
        else:
            temp.append(i)
    e = temp
    return e

symbols = ['<=','>=','==','[*]{2}','\(','\)','[-]','[+]','[/]','[!]']
symbols += ['(?<![*])[*](?![*])', # matches '*' not part of '**'
            '[<](?![=])',         # matches '<' not part of '<='
            '[>](?![=])']         # matches '>' not part of '>='

for keyword in keywords:
    symbols += '(?<![a-zA-Z0-9])' + keyword + '(?![a-zA-Z0-9])', # matches 'keyword' unless preceded by or followed by an alphanumeric character


def tokenizeExpression(e,scope):
    e = [e]
    for reg,actual in [("[']{3}","'''"),('["]{3}','"""'),("[']","'"),('["]','"')]:
        pattern = r'(' + reg + '.*?' + reg + ')'
        temp = []
        for w in e:
            if type(w) != type('str'):
                temp.append(w)
            else:
                for i in re.split(pattern,w):
                    if i.startswith(actual) or i.startswith(actual):
                        i = i[len(actual):-len(actual)]
                        temp.append(('literal',i))
                    else:
                        temp.append(i)
        e = temp

    for symbol in symbols:
        temp = []
        for i in e:
            if type(i) != type('str'):
                temp.append(i)
            else:
                for a in re.split(r'(' + symbol + ')',i):
                    if a.strip() != '':
                        temp += [a.strip()]
        e = temp

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
        exp[i-1] = primitives.ExpressionExponent(exp[i-1],exp[i+1])
        del exp[i:i+2]

    if len(exp) == 1:
        return exp[0]

    # reduce -n notation to single values
    indices = [i for i,x in enumerate(exp) if x == '-']
    for i in reversed(indices):
        if i == 0 or type(exp[i-1]) == type('str'):
            exp[i] = primitives.ExpressionAdd([['-',exp[i+1]]])
            del exp[i+1]

    # reduce +n notation to single values
    indices = [i for i,x in enumerate(exp) if x == '+']
    for i in reversed(indices):
        if i == 0 or type(exp[i-1]) == type('str'):
            exp[i] = primitives.ExpressionAdd([['+',exp[i+1]]])
            del exp[i+1]

    if len(exp) == 1:
        return exp[0]

    if '+' in exp or '-' in exp:
        return collapse(exp,['+','-'],primitives.ExpressionAdd)
    if '*' in exp or '/' in exp:
        return collapse(exp,['*','/'],primitives.ExpressionMult)

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













