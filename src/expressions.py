from collections import namedtuple
import re

Token = namedtuple('Token','tag value')


class Literal(object):
    def __init__(self,val):
        self.val = val

    def exe(self):
        return self.val

def linkLiterals(exp):
    '''
    >>> e = linkLiterals([Token('raw','3')])
    >>> e[0].tag == 'object' and e[0].value.exe() == 3
    True

    >>> e = linkLiterals([Token('literal','hello world')])
    >>> e[0].tag == 'object' and e[0].value.exe() == 'hello world'
    True
    '''

    temp = []
    for e in exp:
        if e.tag == 'literal':
            temp.append(Token('object',Literal(e.value)))
        elif e.tag == 'raw':
            if re.fullmatch(r'[0-9]+[.][0-9]+',e.value):
                temp.append(Token('object',Literal(float(e.value))))
            elif re.fullmatch(r'[0-9]+',e.value):
                temp.append(Token('object',Literal(int(e.value))))
            else:
                temp.append(e)
        else: # if token is already processed
            temp.append(e)
    return temp

class Variable(object):
    def __init__(self,ptr,name):
        self.ptr = ptr
        self.name = name

    def exe(self):
        return self.ptr.getVar(self.name)

    def recv(self,val):
        self.ptr.setVar(self.name,val)

def linkVariables(exp):
    # TODO
    return exp
















def getDividingCommas(exp):
    '''
    >>> getDividingCommas('a,b,c')
    [1, 3]
    >>> getDividingCommas('1,2,3,4,5,6,7,8')
    [1, 3, 5, 7, 9, 11, 13]
    >>> getDividingCommas('1,[2,3,4,5,6],7,8')
    [1, 13, 15]
    '''

    i = [i for i,e in enumerate(exp) if e == ',']

    # remove all commas between [] from consideration
    for m in re.finditer(r'\[.*?\]',exp):
        i = [e for e in i if e < m.start() or e >= m.end()]

    # remove all commas between () from consideration
    for m in re.finditer(r'\(.*?\)',exp):
        i = [e for e in i if e < m.start() or e >= m.end()]


    return i

def splitExpression(exp):
    '''
    >>> splitExpression('a,b,c')
    ['a', 'b', 'c']
    >>> splitExpression('a,[b,c]')
    ['a', '[b,c]']
    >>> splitExpression('a,[1,2,3]')
    ['a', '[1,2,3]']
    '''

    # -1 and i+1 are necessary because we're excluding commas
    i = [-1] + getDividingCommas(exp) + [None]
    return [exp[i+1:j] for i,j in zip(i,i[1:])]




#def buildSendTarget(




def splitByToken(exp,tok):
    '''
    >>> splitByToken([Token('raw','a'),
    ...               Token('=','='),
    ...               Token('raw','b')],
    ...              {'value':'='})
    ([Token(tag='raw', value='a')], [Token(tag='raw', value='b')])

    >>> splitByToken([Token('raw','a'),
    ...               Token('->','->'),
    ...               Token('raw','b')],
    ...              {'value':'->'})
    ([Token(tag='raw', value='a')], [Token(tag='raw', value='b')])

    >>> splitByToken([Token('define','define'),
    ...               Token('raw','testing'),
    ...               Token(':',':')],
    ...              {'tag':'raw'})
    ([Token(tag='define', value='define')], [Token(tag=':', value=':')])
    '''

    i = -1

    # checks whether all required properties of the candidate match provided pattern
    test = lambda candidate,pattern : all([getattr(candidate,k)==v for k,v in pattern.items()])

    while not test(exp[i],tok):
        i += 1
    assert(i >= 0)
    assert(i < len(exp))
    assert(test(exp[i],tok))

    left = exp[:i]
    right = exp[i+1:]
    return left,right


def parseSend(exp):
    i = -1
    while exp[i].value != '->':
        i += 1
    assert(i > 0)
    assert(i+1 < len(exp))
    assert(exp[i].value == '->')

    left = exp[:i]
    right = exp[i+1:]
    print(left,'->',right)


def parseAssign(exp,subagent):

    i = -1
    while exp[i].value != '=':
        i += 1
    assert(i > 0)
    assert(i+1 < len(exp))
    assert(exp[i].value == '=')

    left = exp[:i]
    right = exp[i+1:]
    return
    print(left,'=',right)


# TODO: name better
def parseBranchEnds3(exp):
    temp = ' '.join([e.value for e in exp])
    if '->' in temp:
        pass
        #parseSend(exp)
    elif '=' in temp:
        parseAssign(exp)

# TODO: name better
def iterBranchEnds2(p,subagent):
    try:
        if len(p.children) > 0:
            for e in p.children:
                parseBranchEnds2(e,subagent)
    except:
        parseBranchEnds3(p,subagent)
    return p

def iterBranchEnds(p):
    for agent_name,agent in p.agent.items():
        for subagent_name,subagent in agent.subagent.items():
            for line in subagent.code:
                line.code = parseBranchEnds2(line.code,subagent)

    return p


def parseBranchEnds(p):








