import re

class ProtoLine(object):
    def __init__(self,spaces,code):
        self.spaces = spaces
        self.code = code
        self.children = []

    def addChild(self,c):
        self.children.append(c)

def loadfile(filename):
    code = []
    with open(filename,'r') as f:
        for line in f:
            match = re.match('^([ ]*)([^#\s\n][^#]*[^#\s\n])',line)
            if match:
                a,b = match.groups()
                code.append(ProtoLine(len(a),b))
    return code

