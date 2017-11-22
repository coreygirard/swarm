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























'''
def getAgentList(p):
    temp = []
    for agent in p:
        if [i.tag for i in agent.code] == ['define','variable',':']:
            for subagent in agent.children:
                temp.append(agent.code[1].value+'.'+subagent.code[0].value)
        else:
            temp.append(agent.code[1].value+'.run')
    for e in temp:
        if e.endswith('.run'):
            temp.append(e[:-4])
    return sorted(temp)
'''






'''
















class ProtoLine(object):
    def __init__(self,spaces,code):
        self.spaces = spaces
        self.code = code
        self.children = []

    def addChild(self,c):
        self.children.append(c)

def loadfile(filename):
    code = []
    with open(filename,'r') as f:
        for line in f:
            match = re.match('^([ ]*)([^#\s\n][^#]*[^#\s\n])',line)
            if match:
                a,b = match.groups()
                code.append(ProtoLine(len(a),b))
                yield ProtoLine(len(a),b)
    #return code





















Tag = namedtuple('Tag','tag value')

def tokens(line):
    line = line.strip(' ')
    if line == '':
        return []

    # grab string literals
    match = re.match("^(.*)('[^'].*?')(.*)$",line)
    if match:
        a,b,c = match.groups()
        return tokens(a) + [Tag('literal',b)] + tokens(c)

    for symbol in ['->','==','-=','+=','<=','>=']:
        match = re.match('^(.*)' + symbol + '(.*)$',line)
        if match:
            return tokens(match.groups()[0]) + [Tag(symbol,symbol)] + tokens(match.groups()[1])

    for symbol in list(':,(){}[]=-.+<>'):
        match = re.match('^(.*)[' + symbol + '](.*)$',line)
        if match:
            return tokens(match.groups()[0]) + [Tag(symbol,symbol)] + tokens(match.groups()[1])

    match = re.match('^(.*) in (.*)$',line)
    if match:
        return tokens(match.groups()[0]) + [Tag('in','in')] + tokens(match.groups()[1])

    for prefix in ['if','else','else if','switch','for','while','type','define']:
        match = re.match('^'+prefix+' (.*)$',line)
        if match:
            return [Tag(prefix,prefix)] + tokens(match.groups()[0])

    for symbol in ['->','==','-=','+=','<=','>=']:
        match = re.match('^(.*)' + symbol + '(.*)$',line)
        if match:
            return tokens(match.groups()[0]) + [Tag(symbol,symbol)] + tokens(match.groups()[1])


    match = re.match("^[a-zA-Z][a-zA-Z0-9]*$",line)
    if match:
        return [Tag('variable',line)]


    match = re.match("^[0-9]+$",line)
    if match:
        return [Tag('literal',line)]
    

    if line == 'print':
        return [Tag('builtin','print')]

    return [line]

def tokenize(lines):
    for i in range(len(lines)):
        #print(lines[i].code)
        lines[i].code = tokens(lines[i].code)
        #print(' '.join([e.tag for e in lines[i].code]))
        #print('\n')
    return lines


















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





    
def nest(code):
    if code == []:
        return []
    
    nested = [code.pop(0)]
    while len(code) > 0:
        while len(code) > 0 and code[0].spaces == nested[-1].spaces:
            nested.append(code.pop(0))

        t = 0
        while t < len(code) and code[t].spaces > nested[-1].spaces:
            t = t + 1
        
        nested[-1].children = nest(code[:t])
        code = code[t:]
    
    return nested

def makeTree(filename):
    # TODO: make this stream properly without building a list
    code = list(loadfile(filename))
    
    return nest(code)

def tags2node(line):
    assert(line.children == [])
    
    c = line.code
    if c[1].value == '->':
        return Send(Literal(c[0].value),Pr())















































Tag = namedtuple('Tag','tag value')

def tokens(line):
    line = line.strip(' ')
    if line == '':
        return []

    # grab string literals
    match = re.match("^(.*)('[^'].*?')(.*)$",line)
    if match:
        a,b,c = match.groups()
        return tokens(a) + [Tag('literal',b)] + tokens(c)

    for symbol in ['->','==','-=','+=','<=','>=']:
        match = re.match('^(.*)' + symbol + '(.*)$',line)
        if match:
            return tokens(match.groups()[0]) + [Tag(symbol,symbol)] + tokens(match.groups()[1])

    for symbol in list(':,(){}[]=-.+<>'):
        match = re.match('^(.*)[' + symbol + '](.*)$',line)
        if match:
            return tokens(match.groups()[0]) + [Tag(symbol,symbol)] + tokens(match.groups()[1])

    match = re.match('^(.*) in (.*)$',line)
    if match:
        return tokens(match.groups()[0]) + [Tag('in','in')] + tokens(match.groups()[1])

    for prefix in ['if','else','else if','switch','for','while','type','define']:
        match = re.match('^'+prefix+' (.*)$',line)
        if match:
            return [Tag(prefix,prefix)] + tokens(match.groups()[0])

    for symbol in ['->','==','-=','+=','<=','>=']:
        match = re.match('^(.*)' + symbol + '(.*)$',line)
        if match:
            return tokens(match.groups()[0]) + [Tag(symbol,symbol)] + tokens(match.groups()[1])


    match = re.match("^[a-zA-Z][a-zA-Z0-9]*$",line)
    if match:
        return [Tag('variable',line)]


    match = re.match("^[0-9]+$",line)
    if match:
        return [Tag('literal',line)]
    

    if line == 'print':
        return [Tag('builtin','print')]

    return [line]



def buildLine(line):
    token = tokens(line)
    if [token[1].value,token[2].value] == ['->','print']:
        return Send(Literal(token[0].value),Pr())


def tokenize(lines):
    for i in range(len(lines)):
        lines[i].code = tokens(lines[i].code)
    return lines

def line2obj(t):
    if type(t) == type([1,2,3]): # If it's just a sequence of raw lines
        for e in t:
            line2obj(e)
    elif t.children == []:       # If it's a single raw line
        print('\t'+t.code)
        print(buildLine(t.code))
    else:
        for c in t.children:     # If it's a structure, like 'for', 'define', etc
            line2obj(c)














def printTree(t,depth=0):
    if type(t) == type([1,2,3]):
        for e in t:
            printTree(e,depth+1)
    elif t.children == []:
        print('  '*depth + t.code)
    else:
        print('  '*depth + t.code)
        for c in t.children:
            printTree(c,depth+1)
    











#lines = loadfile(sys.argv[1])
#lines = loadfile('test.swarm')

#for line in loadfile('test.swarm'):
#    print(line)



tree = makeTree('test.swarm')

#printTree(tree)

obj = line2obj(tree)





'''







'''


# tokenize
lines = tokenize(lines)

# don't need to treeify this program

program = nest(lines)


pprint(program)
'''
'''
treed = [treeify.tags2node(e) for e in lines]
for t in treed:
    t.exe()
'''

'''
program = treeify.nest(lines)

for l in program:
    assert(l.code[0].value == 'define')

#pprint(getAgentList(program))

print(program[0].children[0].children[0].code)
'''
