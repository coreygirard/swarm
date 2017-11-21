from multiprocessing import Process, Queue, Pipe
import time
import random

def loop(f,i,o):
    while True:
        temp = i.get()
        time.sleep(1)
        if temp == None:
            break
        else:
            o.put(f(temp))

class Subagent(object):
    def __init__(self,p,i,o):
        self.p = p
        self.i = i
        self.o = o

    def put(self,e):
        self.i.put(e)
    
    def get(self):
        return self.o.get()

def buildSubagent(f):
    toSpoke,toHub = Queue(),Queue()
    
    p = Process(target=loop, args=(doStuff1,toSpoke,toHub))
    p.start()

    return Subagent(p,toSpoke,toHub)


def doStuff1(n):
    return '1: ' + str(n)

s = buildSubagent(doStuff1)

s.put(4)
s.put(5)
s.put(7)
print(s.get())
print(s.get())
print(s.get())
