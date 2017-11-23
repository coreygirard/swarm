import sys
from collections import namedtuple
from pprint import pprint
import re
import build_primitives as primitives




class Line(object):
    def __init__(self,code):
        self.code = code
        
    def exe(self):
        print("fake-executing '" + self.code + "'")



def buildExpression():
    pass


def buildLine(line,vh):
    assert(line.children == [])
    c = line.code
    if '=' in c:
        a,b = c.split('=')
        a,b = a.strip(),b.strip()
    
        return primitives.PrimitiveAssign(primitives.PrimitiveReference(a,vh),primitives.PrimitiveLiteral(int(b)))
    elif '->' in c:
        a,b = c.split('->')
        a,b = a.strip(),b.strip()
        
        a = primitives.PrimitiveReference(a,vh)
        b = primitives.PrimitivePrint()
        return primitives.PrimitiveSend(a,b)
    else:
        return Line(c)
