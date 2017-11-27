import re
from collections import namedtuple





Token = namedtuple('Token','tag value')

tokens = [('()',r'([\(])'),
          ('()',r'([\)])'),
          ('[]',r'([\[])'),
          ('[]',r'([\]])'),
          ('{}',r'([\{])'),
          ('{}',r'([\}])'),
          ('->',r'(->)'),
          (',', r'([,])'),
          ('.', r'([.])'),
          ('=', r'([=])'),
          ('+', r'([+])'),
          (':', r'([:])')]

keywords = ['and','or','not','nand','nor','xor','xnor','define','switch','if','else','self','init','run','type']
for keyword in keywords:
    tokens.append((keyword,'(?<![a-zA-Z0-9])(' + keyword + ')(?![a-zA-Z0-9])')) # matches 'keyword' unless preceded by or followed by an alphanumeric character

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
    >>> t = extractStringLiterals('This is a "test" string')
    >>> t == [Token(tag='raw', value='This is a '),
    ...       Token(tag='literal', value='test'),
    ...       Token(tag='raw', value=' string')]
    True
    '''

    st = []
    buff = []
    delim = None

    # iterate through each character/delimiter
    for c in findStringEnds(s):
        if type(c) == type((0,)): # if we received a delimiter
            if delim == None:   # if we're starting a string literal
                if len(buff) > 0:
                    st.append(Token('raw',''.join(buff)))
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
        st.append(Token('raw',''.join(buff)))
    return st


def tokenize(exp):
    '''
    >>> t = tokenize('receive(service,status):')
    >>> t == [Token(tag='raw', value='receive'),
    ...       Token(tag='()', value='('),
    ...       Token(tag='raw', value='service'),
    ...       Token(tag=',', value=','),
    ...       Token(tag='raw', value='status'),
    ...       Token(tag='()', value=')'),
    ...       Token(tag=':', value=':')]
    True
    '''
    #exp = [Token('raw',exp)]
    exp = extractStringLiterals(exp)

    for tag,regex in tokens:
        temp = []
        for e in exp:
            if e.tag == 'raw':
                for snippet in re.split(regex,e.value.strip()):
                    snippet = snippet.strip()
                    if re.fullmatch(regex,snippet):
                        temp.append(Token(tag,snippet))
                    elif snippet != '':
                        temp.append(Token('raw',snippet))
            else:
                temp.append(e)
        exp = temp
    return exp





