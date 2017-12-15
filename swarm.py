from pprint import pprint
import random
from src import tree
from src import expressions


def buildProgram(filename):
    p = tree.fetchfile('test.swarm')
    p = tree.loadfile(p)
    p = tree.tree(p)
    p = tree.Program(p)

    p = expressions.parseBranchEnds(p)

    return p





p = buildProgram('test.swarm')





for k,v in p.agent.items():
    print(k)
    pprint(v.subagent)









