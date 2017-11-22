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

def buildLine(line):
    return Line(line)

class Parent(object):
    def __init__(self,code,children):
        self.code = code
        self.children = children
    
    def exe(self):
        print("fake-executing '" + self.code + "'")
        for c in self.children:
            c.exe()

class PrimitiveFor(object):
    def __init__(self,iterator,children):
        self.iterator = iterator
        self.children = children
    
    def exe(self):
        for i in self.iterator.iterate():
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

def convert(t):
    c = t.code
    if c.startswith('for '):
        assert(t.children != [])
        
        match = re.match(r'^for (.+?) in (.+?):$',c)
        if match:
            variables = match.groups()[0]
            iterator = match.groups()[1]
            
            print(iterator)
            match = re.match(r'(\[|\()([0-9]+)(?:[:]([0-9]+)){1,2}(\]|\))',iterator)
            rangeParams = list(match.groups())
            for i in range(len(rangeParams)):
                if rangeParams[i] not in '()[]':
                    rangeParams[i] = int(rangeParams[i])
            
            

        return PrimitiveFor(PrimitiveRange(*rangeParams),[buildLine(e.code) for e in t.children])
        
        print(t.code)
        print(t.children[0].code)
        return buildLine(t.code)


# --------------------------------------------------------

class Subagent(object):
    def __init__(self,code):
        self.code = code
    
    #def __repr__(self):
    #    return 'Subagent(' + str(self.code) + ')'

    def exe(self):
        for c in self.code:
            c.exe()

def makeSubagent(s):
    return Subagent([convert(e) for e in s.children])

class Agent(object):
    def __init__(self,subagent):
        self.subagent = subagent
    
    #def __repr__(self):
    #    return 'Agent(' + str(self.subagent) + ')'
    
    def init(self):
        if 'init' in self.subagent:
            self.subagent['init'].exe()

def makeAgent(a):
    subagent = {}
    for line in a.children:
        c = line.code
        assert(re.match(r'^[a-zA-Z0-9]+:$',c) != None)
        
        match = re.match(r'^([a-zA-Z0-9]+):$',c)
        if match:
            subagent[match.groups()[0]] = makeSubagent(line)
    
    return Agent(subagent)

class Program(object):
    def __init__(self,agent):
        self.agent = agent

    def init(self):
        for a in self.agent.values():
            a.init()

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









