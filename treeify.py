class Literal(object):
    def __init__(self,v):
        self.v = v
    
    def exe(self):
        return self.v

    def __repr__(self):
        return str(self.v)

class Pr(object):
    def recv(self,e):
        print(e)

    def __repr__(self):
        return 'print'

class Send(object):
    def __init__(self,f,t):
        self.f = f
        self.t = t
    
    def exe(self):
        self.t.recv(self.f.exe())

    def __repr__(self):
        return 'Send(' + repr(self.f) + '->' + repr(self.t) + ')'





def nest(code):
    if code == []:
        return []
    
    nested = [code.pop(0)]
    while len(code) > 0:
        while len(code) > 0 and code[0].spaces == nested[-1].spaces:
            nested.append(code.pop(0))

        t = 0
        while t < len(code) and code[t].spaces > nested[-1].spaces:
            t = t + 1
        
        nested[-1].children = nest(code[:t])
        code = code[t:]
    
    return nested

def tags2node(line):
    assert(line.children == [])
    
    c = line.code
    if c[1].value == '->':
        return Send(Literal(c[0].value),Pr())





