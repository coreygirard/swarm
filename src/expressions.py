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









