import sys
from collections import namedtuple
from pprint import pprint
import re
import build_structures as structures

# --------------------------------------------------------
# -------- PREPROCESSING ---------------------------------
# --------------------------------------------------------

class Node(object):
    def __init__(self,depth,code):
        self.depth = depth
        self.code = code
        self.parent = None
        self.children = []

    def add(self,child):
        child.parent = self
        self.children.append(child)

def fetchfile(filename):
    with open(filename,'r') as f:
        for line in f:
            yield line

# returns iterator of Node objects containing indent depth and line of code
def loadfile(it):
    code = []
    for line in it:
        match = re.match('^([ ]*)([^#\s\n][^#]*[^#\s\n])',line)
        if match:
            a,b = match.groups()
            yield Node(len(a),b)

# folds stream of Node objects into a tree based upon indent depth
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

# --------------------------------------------------------
# -------- BUILT-IN FUNCTIONS ----------------------------
# --------------------------------------------------------

class PrimitivePrint(object):
    def __init__(self,addr,debug):
        self.separator = '\n'
        self.addr = addr
        self.debug = debug

    def recv(self,e):
        if self.debug:
            print(str(e) + ' arrived at ' + str(self.addr))
        print(e,end=self.separator)

    def setSeparator(self,c):
        self.separator = c

class PrimitiveError(object):
    def __init__(self,addr,debug):
        self.separator = '\n'
        self.addr = addr
        self.debug = debug

    def recv(self,e):
        if self.debug:
            print(str(e) + ' arrived at ' + str(self.addr))

# --------------------------------------------------------
# -------- SCOPE OBJECTS ---------------------------------
# --------------------------------------------------------

class SubagentScope(object):
    def __init__(self,parent):
        self.d = {}
        self.parent = parent

    def exists(self,k):
        return k in self.d

    def get(self,k):
        if k.startswith('self.'):
            return self.parent.get(k)
        else:
            return self.d[k]

    def set(self,k,v):
        if k.startswith('self.'):
            self.parent.set(k,v)
        else:
            self.d[k] = v

    def clear(self):
        self.d.clear()

    def getLocals(self):
        temp = self.parent.getLocals()
        for k,v in self.d.items():
            temp[k] = v
        return temp

class AgentScope(object):
    def __init__(self):
        self.d = {}

    def exists(self,k):
        return k in self.d

    def get(self,k):
        assert(k.startswith('self.'))
        return self.d[k]

    def set(self,k,v):
        assert(k.startswith('self.'))
        self.d[k] = v

    def getLocals(self):
        return self.d

# --------------------------------------------------------
# -------- MESSAGING -------------------------------------
# --------------------------------------------------------

class Endpoint(object):
    def __init__(self,parent,target):
        self.parent = parent
        self.target = target

    def recv(self,v):
        if type(v) != type([]):
            v = [v]
        self.parent.recv(v,self.target)

class SubagentRouter(object):
    def __init__(self,parent,addr,debug=False):
        self.subagent = None
        self.parent = parent
        self.addr = addr
        self.debug = debug

    def recv(self,v,addr):
        if addr == self.addr:
            if self.debug:
                print(str(v) + ' arrived at ' + str(self.addr))
                print('adding to queue')
            self.subagent.queue.append(v)

        else:
            if self.debug:
                print(str(v) + ' received by ' + str(self.addr))
            self.parent.recv(v,addr)

    def makeEndpoint(self,target):
        return Endpoint(self,target.split('.'))

class AgentRouter(object):
    def __init__(self,parent,addr,debug):
        self.parent = parent
        self.addr = addr
        self.subagentRouter = {}
        self.debug = debug

    def makeSubagentRouter(self,name):
        temp = SubagentRouter(self,self.addr+[name],debug=self.debug)
        self.subagentRouter[name] = temp
        return temp

    def recv(self,v,addr):
        if self.debug:
            print(str(v) + ' received by ' + str(self.addr))
        if addr[:1] == self.addr:
            self.subagentRouter[addr[1]].recv(v,addr)
        else:
            self.parent.recv(v,addr)

class ProgramRouter(object):
    def __init__(self,debug):
        self.debug = debug
        self.agentRouter = {}
        self.builtins = {'print':PrimitivePrint(['print'],self.debug),
                         'error':PrimitiveError(['error'],self.debug)}

    def makeAgentRouter(self,name):
        temp = AgentRouter(self,[name],self.debug)
        self.agentRouter[name] = temp
        return temp

    def recv(self,v,addr):
        if self.debug:
            print(str(v) + ' received by program')
        if addr[0] in self.builtins.keys():
            self.builtins[addr[0]].recv(v)
        else:
            self.agentRouter[addr[0]].recv(v,addr)

# --------------------------------------------------------
# -------- CONTAINERS ------------------------------------
# --------------------------------------------------------

class Subagent(object):
    def __init__(self,code,inputs,scope,router):
        self.code = code
        self.scope = scope
        self.router = router
        self.router.subagent = self
        self.queue = []

        if inputs == None:
            self.inputs = []
        elif ',' in inputs:
            self.inputs = inputs.split(',')
        else:
            self.inputs = [inputs]

    def exe(self):
        for c in self.code:
            c.exe()

    def inspectQueues(self,n):
        print('[{0}]: {1}'.format(n,str(self.queue)))

    def execute(self):
        #print('executing @ ' + str(self.router.addr))
        if len(self.queue) > 0:
            for v,i in zip(self.inputs,self.queue.pop(0)):
                self.scope.set(v,i)
            self.exe()
            self.scope.clear()

class Agent(object):
    def __init__(self,subagent,scope,router):
        self.subagent = subagent
        self.scope = scope
        self.router = router

    def init(self):
        if 'init' in self.subagent.keys():
            self.subagent['init'].exe()

    def inspectQueues(self,n):
        for k,v in self.subagent.items():
            v.inspectQueues(n+'.'+k)

    def getQueueLengths(self,n):
        temp = []
        for k,v in self.subagent.items():
            temp.append((n+'.'+k,len(v.queue)))
        return temp

    def execute(self,route):
        head = route.pop(0)
        self.subagent[head].execute()

class Program(object):
    def __init__(self,agent,router):
        self.agent = agent
        self.router = router

    def init(self):
        for a in self.agent.values():
            a.init()

    def inspectQueues(self):
        for k,v in self.agent.items():
            v.inspectQueues(k)

    def getQueueLengths(self):
        temp = []
        for k,v in self.agent.items():
            temp += v.getQueueLengths(k)
        return temp

    def execute(self,route):
        head = route.pop(0)
        tail = route
        self.agent[head].execute(tail)

# --------------------------------------------------------
# -------- FACTORIES -------------------------------------
# --------------------------------------------------------

def makeSubagent(s,inputs,agentScope,router):
    scope = SubagentScope(agentScope)

    temp = []
    for e in s.children:
        temp.append(structures.buildStructure(e,scope,router))

    return Subagent(temp,inputs,scope,router)

def makeAgent(a,router):
    scope = AgentScope()

    subagent = {}
    for line in a.children:
        c = line.code
        assert(re.match(r'^[a-zA-Z0-9]+([\(].*[\)])?:$',c) != None)

        match = re.match(r'^([a-zA-Z0-9]+)(?:[\(](.*)[\)])?:$',c)
        if match:
            name = match.groups()[0]
            inputs = match.groups()[1]
            subagentRouter = router.makeSubagentRouter(name)
            subagent[name] = makeSubagent(line,inputs,scope,subagentRouter)

    return Agent(subagent,scope,router)

def makeProgram(filename,debug=False):
    t = tree(loadfile(fetchfile(filename)))

    # TODO: handle type definitions as well
    programRouter = ProgramRouter(debug=debug)
    program = Program(agent,programRouter)
    
    agent = {}
    for line in t.children:
        c = line.code
        assert(c.startswith('define '))

        match = re.match(r'^define (.*):$',c)
        if match:
            name = match.groups()[0]
            agentRouter = program.router.makeAgentRouter(name)
            agent[name] = makeAgent(line,agentRouter)

    return program








