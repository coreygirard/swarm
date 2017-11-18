import sys
from loadfile import loadfile
from tokenize import tokenize
import treeify

# load file and pre-process
#lines = loadfile(sys.argv[1])
lines = loadfile('hestia.swarm')

# tokenize
lines = tokenize(lines)

program = treeify.nest(lines)

print(program)

