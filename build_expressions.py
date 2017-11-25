import re
import operator
import build_primitives as primitives




def buildLiteral(e):
    return primitives.PrimitiveLiteral(e)

def buildVariable(e,scope):
    if scope == None:
        return ('variable',e)
    else:
        return primitives.PrimitiveReference(e,scope)

# creates executable objects
def buildLiteralsAndVariables(e,scope):
    temp = []
    for i in e:
        if type(i) != type('str'):
            temp.append(i)
            continue

        i = i.strip()
        if i == 'true':
            temp.append(buildLiteral(True))

        elif i == 'false':
            temp.append(buildLiteral(False))

        elif re.fullmatch(r'([0-9]+[.][0-9]+)',i):
            temp.append(buildLiteral(float(i)))

        elif re.fullmatch(r'([0-9]+)',i): # integer
            temp.append(buildLiteral(int(i)))

        elif re.fullmatch(r'([a-zA-Z0-9]+)',i) and i not in keywords:
            temp.append(buildVariable(i,scope))

        else:
            temp.append(i)

    e = temp
    return e

# generator that yields all characters in a string, lumping and designating all possible string literal boundaries
def findStringEnds(s):
    t = 0
    while t < len(s):
        if s[t:t+3] == "'''":
            yield ("'''",)
            t += 3
        elif s[t:t+3] == '"""':
            yield ('"""',)
            t += 3
        elif s[t] == "'":
            yield ("'",)
            t += 1
        elif s[t] == '"':
            yield ('"',)
            t += 1
        else:
            yield s[t]
            t += 1

# runs through a string, lumping together all string literals
def extractStringLiterals(s):
    st = []
    buff = []
    delim = None

    # iterate through each character/delimiter
    for c in findStringEnds(s):
        if type(c) == type((0,)):
            if delim == None:   # if we're starting a string literal
                if len(buff) > 0:
                    st.append(''.join(buff))
                buff = []
                delim = c[0]

            elif delim == c[0]: # if we're ending a string literal
                st.append(('literal',''.join(buff)))
                buff = []
                delim = None

            else:
                buff.append(c[0])
        else:
            buff.append(c)

    assert(delim == None)
    if len(buff) > 0:
        st.append(''.join(buff))
    return st

keywords = ['and','or','not','nand','nor','xor','xnor']

# potential substring matches are placed after longer matches, to scan for after
symbols = ['<=','>=','==','[*]{2}','\(','\)','[-]','[+]','[/]','[!]','[+]','[<]','[>]','[*]']
for keyword in keywords:
    symbols += ['(?<![a-zA-Z0-9])' + keyword + '(?![a-zA-Z0-9])'] # matches 'keyword' unless preceded by or followed by an alphanumeric character


def tokenizeExpression(s,scope):
    # set string literals off-limits for further parsing
    s = extractStringLiterals(s)

    # package all meaningful symbols into tuples
    for symbol in symbols:
        temp = []
        for e in s:
            if type(e) == type((0,)):
                temp.append(e)
            else:
                for snippet in re.split('('+symbol+')',e.strip()):
                    snippet = snippet.strip()
                    if re.fullmatch(symbol,snippet):
                        temp.append((snippet,))
                    elif snippet != '':
                        temp.append(snippet)
        s = temp

    # create literals and link variables
    s = buildLiteralsAndVariables(s,scope)

    # everything should be matched by now
    assert(not any([type(e) == type('str') for e in s]))

    return s












'''
# same operation for +,- and *,/ pairs
def collapse(e,op,c):
    if e[0] not in op:
        e.insert(0,op[0])
    indices = [i for i,x in enumerate(e) if x in op]+[len(e)]
    inputs = []
    for a,b in zip(indices,indices[1:]):
        inputs.append([e[a][0],recurse(e[a+1:b])])
    return c(inputs)
'''

# simplify all addition/subtraction in the expression to a single object with subobjects
def collapseAddSub(exp):
    if exp[0] not in [('+',),('-',)]:
        exp.insert(0,('+',))
    indices = [i for i,x in enumerate(exp) if x[0] in ['+','-']]+[len(exp)]
    inputs = []
    for a,b in zip(indices,indices[1:]):
        inputs.append([exp[a][0],exp[a+1:b]])
    return primitives.ExpressionAdd(inputs)

# simplify all multiplication/division in the expression to a single object with subobjects
def collapseMultDiv(exp):
    if exp[0] not in [('*',),('/',)]:
        exp.insert(0,('*',))
    indices = [i for i,x in enumerate(exp) if x[0] in ['*','/']]+[len(exp)]
    inputs = []
    for a,b in zip(indices,indices[1:]):
        inputs.append([exp[a][0],exp[a+1:b]])
    return primitives.ExpressionMult(inputs)


def recurse(exp):
    assert(exp.count(('(',)) == exp.count((')',)))

    # reduce parenthetical expressions to single values
    while ('(',) in exp:
        i = exp.index(('(',))
        a = exp[:i]
        b = [exp[i]]
        c = exp[i+1:]
        while b.count(('(',)) != b.count((')',)):
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

    if ('+',) in exp or ('-',) in exp:
        return collapseAddSub(exp)
    if ('*',) in exp or ('/',) in exp:
        return collapseMultDiv(exp)

    raise Exception('invalid expression')

def buildSimpleExpression(e,scope):
    e = tokenizeExpression(e,scope)
    e = recurse(e)
    return e

# --------------------------------------------------------
# -------- HANDLE PULLING FROM MEMORY --------------------
# --------------------------------------------------------

class ComplexExpression(object):
    def __init__(self,exp,scope):
        self.exp = [buildSimpleExpression(e,scope) for e in exp]

    def exe(self):
        return [e.exe() for e in self.exp]

def buildExpression(e,scope):
    e = [i for i in e.split(',') if i != '']
    return ComplexExpression(e,scope)

# --------------------------------------------------------
# -------- HANDLE PUSHING TO MEMORY ----------------------
# --------------------------------------------------------


class ComplexReference(object):
    def __init__(self,k,scope):
        self.ref = [primitives.PrimitiveReference(i,scope) for i in k]

    def set(self,v):
        if len(self.ref) == 1:
            if len(v) == 1:
                v = v[0]
            self.ref[0].set(v)
        else:
            assert(len(v) == len(self.ref))
            for a,b in zip(self.ref,v):
                a.set(b)

def buildReference(e,scope):
    e = [i for i in e.split(',') if i != '']
    return ComplexReference(e,scope)













