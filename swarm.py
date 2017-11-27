from pprint import pprint
#import build_program as program
import random
from src import tree




'''
p = program.makeProgram('test.swarm')
p.init()


while True:
    q = [e[0] for e in p.getQueueLengths() if e[1] > 0]
    if q == []:
        break

    sa = random.choice(q)
    assert(not sa.endswith('.init'))
    sa = sa.split('.')
    #print("Executing: '" + str(sa) + "'")
    p.execute(sa)
'''


p = tree.buildProgram('test.swarm')

for k,v in p.agent.items():
    print(k)
    pprint(v.subagent)









