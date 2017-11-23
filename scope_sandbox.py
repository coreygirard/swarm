
class Scope(object):
    def __init__(self):
        self.d = {}
        self.parent = None
    
    def getChild(self):
        temp = Scope()
        temp.parent = self
        return temp
    
    def get(self,k):
        if k in self.d:
            return self.d[k]
        else:
            return self.parent.get(k)

    def hackySet(self,k,v):
        self.d[k] = v

a = Scope()
b = a.getChild()
c = b.getChild()

a.hackySet('abc',5)
a.hackySet('xyz',3)
b.hackySet('abc',2)

print(a.d)
print(b.d)
print(c.d)
print('--------')
print(c.get('abc'))

