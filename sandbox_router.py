



class Endpoint(object):
    def __init__(self,parent,target):
        self.parent = parent
        self.target = target

    def recv(self,v):
        self.parent.recv(v,self.target)

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

class ProgramRouter(object):
    def __init__(self):
        self.agentRouter = {}

    def makeAgentRouter(self,name):
        temp = AgentRouter(self,[name])
        self.agentRouter[name] = temp
        return temp

    def recv(self,v,addr):
        print(str(v) + ' received by program')
        self.agentRouter[addr[0]].recv(v,addr)


pr = ProgramRouter()
ar1 = pr.makeAgentRouter('example')
ar2 = pr.makeAgentRouter('test')
sr11 = ar1.makeSubagentRouter('init')
sr12 = ar1.makeSubagentRouter('run')
sr21 = ar2.makeSubagentRouter('init')
sr22 = ar2.makeSubagentRouter('run')

e = sr11.makeEndpoint('test.run')
e.recv('hello')




