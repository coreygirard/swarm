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

    def __repr__(self):
        return self.code + str(self.children)

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

class Literal(object):
    def __init__(self,v):
        self.v = v
    
    def exe(self):
        return self.v

    def __repr__(self):
        return str(self.v)

class Pr(object):
    def recv(self,e):
        print(e)

    def __repr__(self):
        return 'print'

class Send(object):
    def __init__(self,f,t):
        self.f = f
        self.t = t
    
    def exe(self):
        self.t.recv(self.f.exe())

    def __repr__(self):
        return 'Send(' + repr(self.f) + '->' + repr(self.t) + ')'

def buildLine(line):
    #token = tokens(line)
    #if [token[1].value,token[2].value] == ['->','print']:
    #    return Send(Literal(token[0].value),Pr())
    return Send(Literal(5),Pr())

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

def convert(t):
    if t.children == []:     # If it's a single raw line
        return buildLine(t.code)
    else:                    # If it's a structure, like 'for', 'define', etc
        return Parent(t.code,[convert(e) for e in t.children])


# --------------------------------------------------------

class Subagent(object):
    def __init__(self,code):
        self.code = code
    
    def __repr__(self):
        return 'Subagent(' + str(self.code) + ')'

    def exe(self):
        self.code.exe()

def makeSubagent(s):
    return Subagent(convert(s))

class Agent(object):
    def __init__(self,subagent):
        self.subagent = subagent
    
    def __repr__(self):
        return 'Agent(' + str(self.subagent) + ')'
    
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









