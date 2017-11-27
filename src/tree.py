import re
import tokenizer


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
    '''
    >>> loadfile(['aaa','    bbb # comment  ','    ccc'])
    [(0, 'aaa'), (4, 'bbb'), (4, 'ccc')]
    '''

    code = []
    for line in it:
        match = re.match('^([ ]*)([^#\s\n][^#]*[^#\s\n])',line)
        if match:
            a,b = match.groups()
            code.append((len(a),tokenizer.tokenize(b)))
    return code

def tree(lines):
    '''
    folds stream of (indent,code) tuples into a tree

    returns a program-level node, parent to all 'agent' nodes
    >>> p = tree([(0, 'aaa'), (4, 'bbb'), (4, 'ccc')])
    >>> p.parent == None
    True

    >>> a = p.children[0]
    >>> a.depth == 0 and a.code == 'aaa'
    True
    >>> a.parent == p and len(a.children) == 2
    True

    >>> b = a.children[0]
    >>> b.depth == 4 and b.code == 'bbb'
    True
    >>> b.parent == a and b.children == []
    True

    >>> c = a.children[1]
    >>> c.depth == 4 and c.code == 'ccc'
    True
    >>> c.parent == a and c.children == []
    True
    '''

    root = Node(-4,'')
    ptr = root
    for depth,code in lines:
        line = Node(depth,code)

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

# ------------------------------------------------
# -------- PROGRAM/AGENT/SUBAGENT OBJECTS --------
# ------------------------------------------------

class Subagent(object):
    def __init__(self,parent,subagent):
        self.parent = parent
        self.scope = {}

    def getVar(self,name):
        if name.startswith('self.'):
            return self.parent.getVar(name)
        else:
            assert(name in self.scope.keys())
            return self.scope[name]

    def setVar(self,name,val):
        if name.startswith('self.'):
            return self.parent.setVar(name,val)
        else:
            self.scope[name] = val


class Agent(object):
    def __init__(self,agent):
        self.subagent = {}
        for subagent in agent.children:
            code = subagent.code

            assert(code[0].tag in ['raw','init','run'])

            name = code[0].value
            self.buildSubagent(name,subagent)

        self.scope = {}

    def buildSubagent(self,name,subagent):
        self.subagent[name] = Subagent(self,subagent)

    def getVar(self,name):
        assert(name.startswith('self.'))
        assert(name in self.scope.keys())
        return self.scope[name]

    def setVar(self,name,val):
        assert(name.startswith('self.'))
        self.scope[name] = val


class Program(object):
    def __init__(self,program):
        self.agent = {}
        for agent in program.children:
            code = agent.code

            if code[0].value == 'define':
                name = code[1].value
                self.buildAgent(name,agent)
            elif code[0].value == 'type':
                pass # TODO: implement types

    def buildAgent(self,name,agent):
        self.agent[name] = Agent(agent)

# --------------------------------------------
# -------- LOOP/IF/SWITCH/ETC OBJECTS --------
# --------------------------------------------










