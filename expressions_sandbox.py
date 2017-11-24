import re


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

class Variable(object):
    def __init__(self,code):
        self.code = code
    
    def __repr__(self):
        return 'Variable(' + str(self.code) + ')'

def buildLiteralsAndVariables(e):
    #e = re.split(r'([a-zA-Z0-9]+)',e)
    temp = []
    for i in e:
        if re.fullmatch(r'([0-9]+)',i):
            temp.append(Literal(int(i))) # TODO: handle non-ints
        elif re.fullmatch(r'([a-zA-Z0-9]+)',i):
            temp.append(Variable(i))
        else:
            temp.append(i.strip())
    e = temp
    return e

def tokenizeExpression(e):
    e = [e]
    for symbol in ['[*]{2}','\(','\)','(?<![*])[*](?![*])','[-]','[+]','[/]']:
        temp = []
        for i in e:
            temp = temp + [a.strip() for a in re.split(r'(' + symbol + ')',i) if a.strip() != '']
        e = temp

    e = buildLiteralsAndVariables(e)
    return e

def collapse(e,op,c):
    if e[0] not in op:
        e.insert(0,op[0])
    indices = [i for i,x in enumerate(e) if x in op]+[len(e)]
    inputs = []
    for a,b in zip(indices,indices[1:]):
        inputs.append([e[a],recurse(e[a+1:b])])
    return c(inputs)

def collapseParentheses(e):
    assert(e.count('(') == e.count(')'))
    i = e.index('(')
    a = e[:i]
    b = [e[i]]
    c = e[i+1:]
    while b.count('(') != b.count(')'):
        b.append(c.pop(0))
    b = recurse(b[1:-1])
    e = a+[b]+c
    return recurse(e)

exp = [
'(3)+(5+3)',
'2**3**4',
'2+3**4',
'2**3+4',
'-3**4',
'-3**4+-5**3',
'-3**4-4+-5**3',
'2*3+4-5+6*7'
]

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


def buildExpression(e):
    e = tokenizeExpression(e)
    e = recurse(e)
    return e




def driver(expr):
    for e in expr:
        t = buildExpression(e)
        #print(t)
        if t.exe() != eval(e):
            print(e)
            print('Result: ' + str(t.exe()))
            print('Should be: ' + str(eval(e)))
            print('\n')

#print(buildExpression('((3+4)*2)*     2 -7**4 - 54'))
e = [
'3+4',
'3-4',
'-3+4',
'-3-4',
'-3+53-3-3+10',
'3+(2-1)',
'((3+4)*2)*     2 -7**4**2 - 54',
'((3+4)*2)*     2 -7**4 - 54',
'((3+4)*2)*     2 -74 - 54',
'(2**3)**4',
'-3**4',
'-3**3',
'(-3)**4',
'(1)',
'2+1',
'2+1-3',
'2+1+10',
'(2+1)',
'3+(2+1)',
'(2+1)-1',
'3+(2+1)-1',
'3*5',
'3*5+6',
'3*-5+6',
'3*56/-2*4',
'-3*5+3',
'3+4',
'(2+1)',
'(1+2)+3',
'(1+2)-(5-3)',
'3*4'
]


#driver(e)

from pprint import pprint
import random
c = '()-+*/0123456789 '

test = []
while len(test) < 1000:
    e = ''.join([random.choice(c) for i in range(random.randint(0,20))])
    try:
        eval(e)
        if '//' not in e:
            test.append(e)
    except:
        print('FAILED! Found ' + str(len(test)) + ' valid so far')
pprint(test)


for d in test:

    try:
        parsed = buildExpression(d)
        result = parsed.exe()
        shouldBe = eval(d)
    except:
        print("Choked on '" + d + "'")

    if result != shouldBe:
        print('Expression: ' + d)
        print('Parsed:     ' + str(parsed))
        print('Result:     ' + str(result))
        print('Should be:  ' + str(shouldBe))
        print('\n')



