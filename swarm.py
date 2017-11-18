import sys
from loadfile import loadfile
from tokenize import tokenize

'''
# file
define test:
    init:
        for i in [0:5):
            i -> test.p
    p(n):
        n -> print
'''


#lines = loadfile(sys.argv[1])
lines = loadfile('hestia.swarm')

'''
lines = [Protoline(0, 'define test:'), 
         Protoline(4, 'init:'), 
         Protoline(8, 'for i in [0:5):'), 
         Protoline(12, 'i -> test.p'), 
         Protoline(4, 'p(n):'), 
         Protoline(8, 'n -> print')]
'''

for i in range(len(lines)):
    lines[i].code = tokenize(lines[i].code)
    if len([e for e in lines[i].code if type(e) == type('str')]) > 0:
        #print(lines[i].code)
        for e in lines[i].code:
            if type(e) == type('str'):
                print(repr(e))


'''
# all as Tag(tag='exampletag', value='examplevalue')

[('define','define'), ('variable','test'), (':',':')]
[('variable','init'), (':',':')]
[('for','for'), 'i in', ('[','['), ('literal','0'), (':',':'), ('literal','5'), (')',')'), (':',':')]
[('variable','i'), ('->','->'), ('variable','test'), ('.','.'), ('variable','p')]
[('variable','p'), ('(','('), ('variable','n'), (')',')'), (':',':')]
[('variable','n'), ('->','->'), ('variable','print')]
'''


