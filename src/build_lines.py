import sys
from collections import namedtuple
from pprint import pprint
import re
import build_expressions as expressions
import build_primitives as primitives

def makeAssign(c,scope):
        a,b = c.split('=')
        a,b = a.strip(),b.strip()

        return primitives.PrimitiveAssign(expressions.buildTarget(a,scope),
                                          expressions.buildSource(b,scope))

def makeSend(c,scope,router):
    a,b = c.split('->')
    a,b = a.strip(),b.strip()

    a = expressions.buildSource(a,scope)
    e = router.makeEndpoint(b)
    return primitives.PrimitiveSend(a,e)

# handles conversion of any line that has no children. Assignment, send, etc
def buildLine(line,scope,router):
    assert(line.children == [])
    c = line.code
    if '=' in c:
        return makeAssign(c,scope)
    elif '->' in c:
        return makeSend(c,scope,router)
