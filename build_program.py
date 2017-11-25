import sys
from collections import namedtuple
from pprint import pprint
import re
import build_structures as structures


class PrimitivePrint(object):
    def __init__(self,addr):
        self.separator = '\n'
        self.addr = addr

    def recv(self,e):
        print(str(e) + ' arrived at ' + str(self.addr))
        print(e,end=self.separator)

    def setSeparator(self,c):
        self.separator = c

class PrimitiveError(object):
    def __init__(self,addr):
        self.separator = '\n'
        self.addr = addr

    def recv(self,e):
        print(str(e) + ' arrived at ' + str(self.addr))

# --------------------------------------------------------

class Endpoint(object):
    def __init__(self,parent,target):
        self.parent = parent
        self.target = target

    def recv(self,v):
        self.parent.recv(v,self.target)

# --------------------------------------------------------

class Subagent(object):
    def __init__(self,code,scope,router):
        self.code = code
        self.scope = scope
        self.router = router

    def exe(self):
        for c in self.code:
            c.exe()

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

    def getLocals(self):
        temp = self.parent.d
        for k,v in self.d.items():
            temp[k] = v
        return temp

class SubagentRouter(object):
    def __init__(self,parent,addr):
        self.parent = parent
        self.addr = addr

    def recv(self,v,addr):
        if addr == self.addr:
            print(str(v) + ' arrived at ' + str(self.addr))
            print('adding to queue')
        else:
            print(str(v) + ' received by ' + str(self.addr))
            self.parent.recv(v,addr)

    def makeEndpoint(self,target):
        return Endpoint(self,target.split('.'))

def makeSubagent(s,agentScope,router):
    scope = SubagentScope(agentScope)

    temp = []
    for e in s.children:
        temp.append(structures.buildStructure(e,scope,router))

    return Subagent(temp,scope,router)

# --------------------------------------------------------

class Agent(object):
    def __init__(self,subagent,scope,router):
        self.subagent = subagent
        self.scope = scope
        self.router = router

    def init(self):
        if 'init' in self.subagent.keys():
            self.subagent['init'].exe()

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

    def getLocals(self):
        return self.d

class AgentRouter(object):
    def __init__(self,parent,addr):
        self.parent = parent
        self.addr = addr
        self.subagentRouter = {}

    def makeSubagentRouter(self,name):
        temp = SubagentRouter(self,self.addr+[name])
        self.subagentRouter[name] = temp
        return temp

    def recv(self,v,addr):
        print(str(v) + ' received by ' + str(self.addr))
        if addr[:1] == self.addr:
            self.subagentRouter[addr[1]].recv(v,addr)
        else:
            self.parent.recv(v,addr)

def makeAgent(a,router):
    scope = AgentScope()

    subagent = {}
    for line in a.children:
        c = line.code
        assert(re.match(r'^[a-zA-Z0-9]+:$',c) != None)

        match = re.match(r'^([a-zA-Z0-9]+):$',c)
        if match:
            name = match.groups()[0]
            subagent[name] = makeSubagent(line,scope,router.makeSubagentRouter(name))

    return Agent(subagent,scope,router)

# --------------------------------------------------------

class Program(object):
    def __init__(self,agent,router):
        self.agent = agent
        self.router = router

    def init(self):
        for a in self.agent.values():
            a.init()

class ProgramRouter(object):
    def __init__(self):
        self.agentRouter = {}
        self.builtins = {'print':PrimitivePrint(['print']),
                         'error':PrimitiveError(['error'])}

    def makeAgentRouter(self,name):
        temp = AgentRouter(self,[name])
        self.agentRouter[name] = temp
        return temp

    def recv(self,v,addr):
        print(str(v) + ' received by program')
        if addr[0] in self.builtins.keys():
            self.builtins[addr[0]].recv(v)
        else:
            self.agentRouter[addr[0]].recv(v,addr)

def makeProgram(t):
    # TODO: handle type definitions as well
    programRouter = ProgramRouter()
    agent = {}
    for line in t.children:
        c = line.code
        assert(c.startswith('define '))

        match = re.match(r'^define (.*):$',c)
        if match:
            name = match.groups()[0]
            agent[name] = makeAgent(line,programRouter.makeAgentRouter(name))

    return Program(agent,programRouter)

