import sys
from collections import namedtuple
from pprint import pprint
import re



class Node(object):
    def __init__(self,depth,code):
        self.depth = depth
        self.code = code
        self.parent = None
        self.children = []
        
    def add(self,child):
        child.parent = self
        self.children.append(child)

    #def __repr__(self):
    #    return self.code + str(self.children)

def loadfile(filename):
    code = []
    with open(filename,'r') as f:
        for line in f:
            match = re.match('^([ ]*)([^#\s\n][^#]*[^#\s\n])',line)
            if match:
                a,b = match.groups()
                yield Node(len(a),b)

def tree(filename):
    root = Node(-4,'')
    ptr = root
    for line in loadfile(filename):
        if line.depth > ptr.depth:
            ptr.add(line)
            ptr = ptr.children[-1]
        elif line.depth == ptr.depth:
            ptr = ptr.parent
            ptr.add(line)
            ptr = ptr.children[-1]
        else:
            while line.depth < ptr.depth:
                ptr = ptr.parent
            ptr = ptr.parent
            ptr.add(line)
            ptr = ptr.children[-1]
            
    return root


# -----------------------------------------------------------

class Line(object):
    def __init__(self,code):
        self.code = code
        
    def exe(self):
        print("fake-executing '" + self.code + "'")

class Parent(object):
    def __init__(self,code,children):
        self.code = code
        self.children = children
    
    def exe(self):
        print("fake-executing '" + self.code + "'")
        for c in self.children:
            c.exe()

class PrimitiveReference(object):
    def __init__(self,k,ptr):
        self.k = k
        self.ptr = ptr

    def exe(self):
        return self.ptr.get(self.k)
    
    def set(self,v):
        self.ptr.set(self.k,v)

class PrimitiveLiteral(object):
    def __init__(self,v):
        self.v = v
    
    def exe(self):
        return self.v

class PrimitivePrint(object):
    def recv(self,e):
        print(e)

class PrimitiveAssign(object):
    def __init__(self,left,right):
        self.left = left
        self.right = right

    def exe(self):
        self.left.set(self.right.exe())

class PrimitiveSend(object):
    def __init__(self,left,right):
        self.left = left
        self.right = right

    def exe(self):
        self.right.recv(self.left.exe())

class PrimitiveFor(object):
    def __init__(self,variable,iterator,children):
        self.variable = variable
        self.iterator = iterator
        self.children = children
    
    def exe(self):
        for i in self.iterator.iterate():
            self.variable.set(i)
            for c in self.children:
                c.exe()
        
class PrimitiveRange(object):
    def __init__(self,*args):
        if len(args) == 4:
            self.l = args[0]
            self.a = args[1]
            self.b = 1
            self.c = args[2]
            self.r = args[3]
        elif len(args) == 5:
            self.l = args[0]
            self.a = args[1]
            self.b = args[2]
            self.c = args[3]
            self.r = args[4]

    def iterate(self):
        start = self.a
        if self.l == '(':
            start = start + self.b
        stop = self.c
        if self.r == ')':
            stop = stop - 1
        t = start
        while t <= stop:
            yield t
            t = t + self.b

# -----------------------------------------------------------


def buildLine(line,vh):
    assert(line.children == [])
    c = line.code
    if '=' in c:
        a,b = c.split('=')
        a,b = a.strip(),b.strip()
    
        return PrimitiveAssign(PrimitiveReference(a,vh),PrimitiveLiteral(int(b)))
    elif '->' in c:
        a,b = c.split('->')
        a,b = a.strip(),b.strip()
        
        a = PrimitiveReference(a,vh)
        b = PrimitivePrint()
        return PrimitiveSend(a,b)
    else:
        return Line(c)

def buildParent(line):
    return Parent(line.code,line.children)

def convert(t,scope):
    if t.children == []:
        return buildLine(t,scope)

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

        return PrimitiveFor(PrimitiveReference(variables,scope),
                            PrimitiveRange(*rangeParams),
                            [convert(e,scope) for e in t.children])
    else:
        return buildParent(t)


# --------------------------------------------------------

class Subagent(object):
    def __init__(self,code,scope):
        self.code = code
        self.scope = scope

    def exe(self):
        for c in self.code:
            c.exe()

class Agent(object):
    def __init__(self,subagent,scope):
        self.subagent = subagent
        self.scope = scope
    
    def init(self):
        if 'init' in self.subagent.keys():
            self.subagent['init'].exe()

class Program(object):
    def __init__(self,agent):
        self.agent = agent

    def init(self):
        for a in self.agent.values():
            a.init()

class SubagentScope(object):
    def __init__(self,parent):
        self.d = {}
        self.parent = parent
    
    def exists(self,k):
        return k in self.d
    
    def get(self,k):
        if k.startswith('self.'):
            return self.parent.get(k)
        return self.d[k]
    
    def set(self,k,v):
        if k.startswith('self.'):
            return self.parent.set(k,v)
        self.d[k] = v

class AgentScope(object):
    def __init__(self):
        self.d = {}
    
    def exists(self,k):
        return k in self.d
    
    def get(self,k):
        assert(k.startswith('self.'))   
        return self.d[k[5:]]
    
    def set(self,k,v):
        assert(k.startswith('self.'))
        self.d[k[5:]] = v

# --------------------------------------------------------

def makeSubagent(s,agentScope):
    scope = SubagentScope(agentScope)
    
    temp = []
    for e in s.children:
        temp.append(convert(e,scope))

    return Subagent(temp,scope)

def makeAgent(a):
    scope = AgentScope()
    
    subagent = {}
    for line in a.children:
        c = line.code
        assert(re.match(r'^[a-zA-Z0-9]+:$',c) != None)
        
        match = re.match(r'^([a-zA-Z0-9]+):$',c)
        if match:
            subagent[match.groups()[0]] = makeSubagent(line,scope)
    
    return Agent(subagent,scope)

def makeProgram(t):
    # TODO: handle type definitions as well
    agent = {}
    for line in t.children:
        c = line.code
        assert(c.startswith('define '))
        
        match = re.match(r'^define (.*):$',c)
        if match:
            agent[match.groups()[0]] = makeAgent(line)

    return Program(agent)



    

t = tree('test.swarm')


p = makeProgram(t)

p.init()
print(p.agent['test'].scope.d)
print(p.agent['test'].subagent['init'].scope.d)


