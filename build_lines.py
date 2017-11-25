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


# handles conversion of any line that has no children. Assignment, send, etc
def buildLine(line,vh,router):
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
        return primitives.PrimitiveSend(a,router.makeEndpoint(b))
    else:
        return Line(c)
