import sys
from collections import namedtuple
from pprint import pprint
import re
import build_structures as structures



# --------------------------------------------------------

class Subagent(object):
    def __init__(self,code,scope):
        self.code = code
        self.scope = scope

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

def makeSubagent(s,agentScope):
    scope = SubagentScope(agentScope)

    temp = []
    for e in s.children:
        temp.append(structures.convert(e,scope))

    return Subagent(temp,scope)

# --------------------------------------------------------

class Agent(object):
    def __init__(self,subagent,scope):
        self.subagent = subagent
        self.scope = scope

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

def makeAgent(a,router):
    scope = AgentScope()

    subagent = {}
    for line in a.children:
        c = line.code
        assert(re.match(r'^[a-zA-Z0-9]+:$',c) != None)

        match = re.match(r'^([a-zA-Z0-9]+):$',c)
        if match:
            subagent[match.groups()[0]] = makeSubagent(line,scope,router)

    return Agent(subagent,scope,)

# --------------------------------------------------------

class Program(object):
    def __init__(self,agent,router):
        self.agent = agent
        self.router = router

    def init(self):
        for a in self.agent.values():
            a.init()

def makeProgram(t):
    # TODO: handle type definitions as well
    router = Router()
    agent = {}
    for line in t.children:
        c = line.code
        assert(c.startswith('define '))

        match = re.match(r'^define (.*):$',c)
        if match:
            agent[match.groups()[0]] = makeAgent(line,router)

    return Program(agent)

