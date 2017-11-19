import sys
from pprint import pprint
from loadfile import loadfile
from tokenize import tokenize
import treeify

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
            
    #return [e.code[1].value for e in p]

# load file and pre-process
#lines = loadfile(sys.argv[1])
lines = loadfile('hestia.swarm')

# tokenize
lines = tokenize(lines)

program = treeify.nest(lines)

for l in program:
    assert(l.code[0].value == 'define')

pprint(getAgentList(program))
