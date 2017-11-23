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

class ExpressionAdd(object):
    def __init__(self,inputs):
        self.inputs = inputs
    
    def exe(self):
        total = 0
        for sign,i in self.inputs:
            total = total + i.exe() * {'-':-1,'+':1}[sign]
        return total
        
class ExpressionMult(object):
    def __init__(self,inputs):
        self.inputs = inputs
    
    def exe(self):
        total = 1
        for sign,i in self.inputs:
            e = i.exe()
            total = total * {'/':1.0/e,'*':e}[sign]
        return total

def buildExpression(e):
    assert(e.count('(') == e.count(')'))
    
    e = e.strip()
    
    if '(' in e or ')' in e:
        temp = []
        for i in re.split(r'([\(].*?[\)])',e):
            if i != '':
                if i.startswith('('):
                    temp.append(buildExpression(i[1:-1]))
        return temp
    elif '-' in e or '+' in e:
        return e


def buildExpression2(e):
    e = e.strip()
    if re.fullmatch(r'[0-9]+',e):
        return primitives.PrimitiveLiteral(int(e))
    
    if '+' in e or '-' in e:
        e = re.split(r'([+-])',e)
        print(e)
        
        if e[0] not in ['-','+']:
            e[0] = ('+',e[0])
        i = 0
        while i < len(e):
            if e[i] in ['-','+']:
                e[i] = (e[i],e[i+1])
                del e[i+1]
            else:
                i = i + 1

        return ExpressionAdd([(a,buildExpression(b)) for a,b in e])

    if '/' in e or '*' in e:
        e = re.split(r'([/*])',e)
        print(e)
        
        if e[0] not in ['/','*']:
            e[0] = ('*',e[0])
        i = 0
        while i < len(e):
            if e[i] in ['/','*']:
                e[i] = (e[i],e[i+1])
                del e[i+1]
            else:
                i = i + 1
        
        return ExpressionMult([(a,buildExpression(b)) for a,b in e])
    
    return e

def buildLine(line,vh):
    assert(line.children == [])
    c = line.code
    if '=' in c:
        a,b = c.split('=')
        a,b = a.strip(),b.strip()
    
        return primitives.PrimitiveAssign(primitives.PrimitiveReference(a,vh),
                                          primitives.PrimitiveLiteral(int(b)))
    elif '->' in c:
        a,b = c.split('->')
        a,b = a.strip(),b.strip()
        
        a = primitives.PrimitiveReference(a,vh)
        b = primitives.PrimitivePrint()
        return primitives.PrimitiveSend(a,b)
    else:
        return Line(c)

#print(buildExpression('3*(abc3+7)**2  -(barr/4)'))
e = buildExpression('(3+4)-1*6')
print(e)

#print(e.exe())
