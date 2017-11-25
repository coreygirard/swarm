import sys
from collections import namedtuple
from pprint import pprint
import re
import build_lines as lines
import build_primitives as primitives
import build_expressions as expressions





class Parent(object):
    def __init__(self,code,children):
        self.code = code
        self.children = children

    def exe(self):
        print("fake-executing '" + self.code + "'")
        for c in self.children:
            c.exe()



# -----------------------------------------------------------




def buildParent(line):
    return Parent(line.code,line.children)

# handles conversion of any line of code that has children. Loops, conditionals, etc
def convert(t,scope):
    if t.children == []:
        return lines.buildLine(t,scope)

    c = t.code
    if c.startswith('for '):
        assert(t.children != [])

        match = re.match(r'^for (.+?) in (.+?):$',c)
        if match:
            variables = match.groups()[0]
            iterator = match.groups()[1]

            match = re.match(r'(\[|\()([0-9]+)(?:[:]([0-9]+)){1,2}(\]|\))',iterator)
            rangeParams = list(match.groups())
            for i in range(len(rangeParams)):
                if rangeParams[i] not in '()[]':
                    rangeParams[i] = int(rangeParams[i])

            return primitives.PrimitiveFor(primitives.PrimitiveReference(variables,scope),
                                           primitives.PrimitiveRange(*rangeParams),
                                           [convert(e,scope) for e in t.children])
    elif c.startswith('while '):
        assert(t.children != [])

        match = re.match(r'^while (.+?):$',c)
        if match:
            condition = match.groups()[0]
            condition = condition.strip()
            condition = expressions.buildExpression(condition,scope)

            loop = primitives.PrimitiveWhile(condition,
                                             scope,
                                             [convert(e,scope) for e in t.children])
            return loop


    else:
        return buildParent(t)








