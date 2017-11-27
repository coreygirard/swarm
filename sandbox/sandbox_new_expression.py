
import re
from collections import namedtuple


Token = namedtuple('Token','tag value')





# ---------------------------
# -------- TOKENIZER --------
# ---------------------------

def findStringEnds(s):
    '''
    >>> list(findStringEnds('This is a "test" string'))
    ['T', 'h', 'i', 's', ' ', 'i', 's', ' ', 'a', ' ', ('"',), 't', 'e', 's', 't', ('"',), ' ', 's', 't', 'r', 'i', 'n', 'g']
    '''

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



def extractStringLiterals(s):
    '''
    >>> extractStringLiterals('This is a "test" string')
    [Token(tag='unprocessed', value='This is a '), Token(tag='literal', value='test'), Token(tag='unprocessed', value=' string')]
    '''

    st = []
    buff = []
    delim = None

    # iterate through each character/delimiter
    for c in findStringEnds(s):
        if type(c) == type((0,)): # if we received a delimiter
            if delim == None:   # if we're starting a string literal
                if len(buff) > 0:
                    st.append(Token('unprocessed',''.join(buff)))
                buff = []
                delim = c[0]

            elif delim == c[0]: # if we're ending a string literal
                st.append(Token('literal',''.join(buff)))
                buff = []
                delim = None

            else: # if we got for example the " inside 'abc"def'
                buff.append(c[0])
        else: # if we received a char, not a delimiter
            buff.append(c)

    assert(delim == None)
    if len(buff) > 0:
        st.append(Token('unprocessed',''.join(buff)))
    return st


def classify(exp):
    '''
    >>> classify([Token('unprocessed','+'), Token('unprocessed','*')])
    [Token(tag='+-', value='+'), Token(tag='*/', value='*')]
    '''

    temp = []
    for e in exp:
        if e.value in ['+','-']:
            temp.append(Token('+-',e.value))
        elif e.value in ['*','/']:
            temp.append(Token('*/',e.value))
        elif e.value in ['(',')']:
            temp.append(Token('()',e.value))
        elif e.value in ['not']:
            temp.append(Token('boolean->',e.value))
        elif e.value in ['and','or','nand','nor','xor','xnor']:
            temp.append(Token('<-boolean->',e.value))
        elif e.value in ['->']:
            temp.append(Token('->',e.value))
        else:
            temp.append(e)
    return temp


keywords = ['and','or','not','nand','nor','xor','xnor']

# potential substring matches are placed after longer matches, to scan for after
symbols = ['<=','>=','==','[*]{2}','\(','\)','[-]','[+]','[/]','[!]','[+]','[<]','[>]','[*]']
for keyword in keywords:
    symbols += ['(?<![a-zA-Z0-9])' + keyword + '(?![a-zA-Z0-9])'] # matches 'keyword' unless preceded by or followed by an alphanumeric character


def tokenize(s,scope):
    '''
    >>> t = tokenize('"string literal" and 4 or 5+3',None)
    >>> t[0].tag == 'literal'       and t[0].value == 'string literal'
    True
    >>> t[1].tag == '<-boolean->'   and t[1].value == 'and'
    True
    >>> t[2].tag == 'unprocessed'   and t[2].value == '4'
    True
    >>> t[3].tag == '<-boolean->'   and t[3].value == 'or'
    True
    >>> t[4].tag == 'unprocessed'   and t[4].value == '5'
    True
    >>> t[5].tag == '+-'            and t[5].value == '+'
    True
    >>> t[6].tag == 'unprocessed'   and t[6].value == '3'
    True
    '''

    # set string literals off-limits for further parsing
    s = extractStringLiterals(s)

    # package all meaningful symbols into tuples
    for symbol in symbols:
        temp = []
        for e in s:
            if e.tag == 'unprocessed':
                for snippet in re.split('('+symbol+')',e.value.strip()):
                    snippet = snippet.strip()
                    if re.fullmatch(symbol,snippet):
                        temp.append(Token('processed',snippet))
                    elif snippet != '':
                        temp.append(Token('unprocessed',snippet))
            else:
                temp.append(e)
        s = temp

    s = classify(s)

    # create literals and link variables
    #s = buildLiteralsAndVariables(s,scope)

    # everything should be matched by now
    assert(not any([e.tag == 'unprocessed' for e in s]))

    return s
























class PrimitiveLiteral(object):
    def __init__(self,v):
        self.v = v

    def exe(self):
        return self.v

    def __repr__(self):
        return 'PrimitiveLiteral('+str(self.exe())+')'

def makeLiteral(v):
    assert(v.tag == 'literal')
    return Token('object',PrimitiveLiteral(v.value))

class ExpressionAddSub(object):
    def __init__(self,inputs):
        self.inputs = inputs

    def exe(self):
        temp = 0
        for sign,e in self.inputs:
            if sign == '+':
                temp += e.exe()
            elif sign == '-':
                temp -= e.exe()
        return temp

class ExpressionExponent(object):
    def __init__(self,a,b):
        self.a = a
        self.b = b

    def exe(self):
        return self.a.exe() ** self.b.exe()

def buildExp(cmd):
    a,_,b = cmd
    return ExpressionExponent(a.value,b.value)


def buildAddSub(cmd):
    '''
    >>> t = buildAddSub([Token('object',PrimitiveLiteral(4)),Token('+-','+'),Token('object',PrimitiveLiteral(1))])
    >>> t.exe()
    5
    '''

    a,op,b = cmd
    a = [['+',a.value]]

    if op.value == '+':
        b = [['+',b.value]]
    elif op.value == '-':
        b = [['-',b.value]]

    inputs = a+b

    return ExpressionAddSub(inputs)




def stage1(exp):
    '''
    >>> stage1('4 + 1')
    ['4', '+', '1']
    '''

    return exp.split(' ')

def stage2(exp):
    '''
    >>> stage2(['4', '+', '1'])
    [Token(tag='literal', value=4), Token(tag='+-', value='+'), Token(tag='literal', value=1)]
    '''

    temp = []
    for e in exp:
        if e in '41':
            temp.append(Token('literal',int(e)))
        elif e in ['+','-']:
            temp.append(Token('+-',e))
        elif e == '**':
            temp.append(Token('**',e))
        else:
            temp.append(Token('string',e))
    return temp

def stage3(exp):
    '''
    >>> temp = stage3([Token(tag='literal', value=4), Token(tag='+-', value='+'), Token(tag='literal', value=1)])
    >>> temp[0].tag
    'object'
    >>> temp[0].value.exe()
    4
    >>> temp[2].tag
    'object'
    >>> temp[2].value.exe()
    1
    '''
    temp = []
    for e in exp:
        if e.tag == 'literal':
            temp.append(makeLiteral(e))
        else:
            temp.append(e)
    return temp


def stage4(exp):
    '''
    >>> t = stage4([Token('object', PrimitiveLiteral(4)),
    ...             Token('+-',     '+'),
    ...             Token('object', PrimitiveLiteral(1))])
    >>> t.exe()
    5

    >>> t = stage4([Token('object', PrimitiveLiteral(2)),
    ...             Token('+-',     '+'),
    ...             Token('object', PrimitiveLiteral(2)),
    ...             Token('**',     '**'),
    ...             Token('object', PrimitiveLiteral(3))])
    >>> t.exe()
    10
    '''

    indicesExp = reversed([i for i,e in enumerate(exp) if e.tag == '**'])
    for i in indicesExp:
        if i > 0:
            exp[i-1] = Token('object', buildExp(exp[i-1:i+2]))
            del exp[i:i+2]

    indicesAddSub = reversed([i for i,e in enumerate(exp) if e.tag == '+-'])
    for i in indicesAddSub:
        if i > 0:
            exp[i-1] = Token('object', buildAddSub(exp[i-1:i+2]))
            del exp[i:i+2]


    assert(len(exp) == 1)
    assert(exp[0].tag == 'object')
    return exp[0].value



def parse(exp):
    '''
    >>> i = parse('4 + 1')
    >>> i.exe()
    5

    '''

    s1 = stage1(exp)
    s2 = stage2(s1)
    s3 = stage3(s2)
    s4 = stage4(s3)
    return s4



def tokenizeExpression(exp):
    exp = [Token('literal',exp)]
    temp = []
    for e in exp:
        if e.tag == 'literal':
            temp.append(makeLiteral(e))
        else:
            temp.append(e)
    return temp



# ----------------------------------------------
# -------- HANDLES LISTS OF EXPRESSIONS --------
# ----------------------------------------------

class MultiExpression(object):
    def __init__(self,inputs):
        self.inputs = inputs

    def exe(self):
        return [e.exe() for e in self.inputs]

def buildMultiExpression(exp):
    temp = exp.split(',') # TODO: make it not split '[0,1,2,3]', for example
    multi = [parseExpression(e) for e in temp]
    return MultiExpression(multi)

def parseMultiExpression(exp):
    exp = buildMultiExpression(exp)
    return exp





'''
exp = '1,2,3+3'
p = parseMultiExpression(exp)

print(p)
print(p.exe())
'''
