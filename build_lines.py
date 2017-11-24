import sys
from collections import namedtuple
from pprint import pprint
import re
import build_expressions as expressions
import build_primitives as primitives



class Line(object):
    def __init__(self,code):
        self.code = code
        
    def exe(self):
        print("fake-executing '" + self.code + "'")



def buildLine(line,vh):
    assert(line.children == [])
    c = line.code
    if '=' in c:
        a,b = c.split('=')
        a,b = a.strip(),b.strip()
    
        return primitives.PrimitiveAssign(expressions.buildReference(a,vh),
                                          expressions.buildExpression(b,vh))
    elif '->' in c:
        a,b = c.split('->')
        a,b = a.strip(),b.strip()
        
        a = expressions.buildExpression(a,vh)
        b = primitives.PrimitivePrint()
        return primitives.PrimitiveSend(a,b)
    else:
        return Line(c)

#print(buildExpression('3*(abc3+7)**2  -(barr/4)'))
#e = buildExpression('(3+4)-1*6')
#print(e)

#print(e.exe())
