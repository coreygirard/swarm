import sys
from collections import namedtuple
from pprint import pprint
import build_program as program
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





t = tree('test.swarm')


p = program.makeProgram(t)

p.init()
#print(p.agent['test'].scope.d)
#print(p.agent['test'].subagent['init'].scope.d)






















