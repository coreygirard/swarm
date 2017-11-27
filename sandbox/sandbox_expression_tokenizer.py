import re




test = [
'a+b',
'4+7',
'abc+532',
'(abc-4) > (3*testing)',
't <= 6',
'3 <= 77',
'3 >= 77',
'a < b < c',
'a <= b >= c',
'a and b',
'a and !b',
'!b',
'a and ! b',
'researchanddevelopment and rd',
'and 4',
'5 and',
'4 and 4',
'and',
' and ',
'0.444',
'0.444 and 9',
"'string literal' and otherStuff",
"'Goodbye, world'"
]

lit = ' and '.join(["'literal'",
                    '"literal"',
                    """'''literal'''""",
                    '''"""literal"""'''])


test += [lit]






























def buildLiteral(e):
    return ('literal',e)
    #return primitives.PrimitiveLiteral(e)

def buildVariable(e,scope):
    return ('variable',e)
    #return primitives.PrimitiveReference(e,scope)

# creates executable objects
def buildLiteralsAndVariables(e,scope):
    temp = []
    for i in e:
        if type(i) != type('str'):
            temp.append(i)
            continue

        i = i.strip()
        if re.fullmatch(r'([0-9]+[.][0-9]+)',i):
            temp.append(buildLiteral(float(i)))

        elif re.fullmatch(r'([0-9]+)',i): # integer
            temp.append(buildLiteral(int(i)))

        elif re.fullmatch(r'([a-zA-Z0-9]+)',i) and i not in keywords:
            temp.append(buildVariable(i,scope))

        else:
            temp.append(i)

    e = temp
    return e

# generator that yields all characters in a string, lumping and designating all possible string literal boundaries
def findStringEnds(s):
    t = 0
    while t < len(s):
        if s[t:t+3] == "'''":
            yield ("'''",)
            t += 3
        elif s[t:t+3] == '"""':
            yield ('"""',)
            t += 3
        elif s[t] == "'":
            yield ("'",)
            t += 1
        elif s[t] == '"':
            yield ('"',)
            t += 1
        else:
            yield s[t]
            t += 1

# runs through a string, lumping together all string literals
def extractStringLiterals(s):
    st = []
    buff = []
    delim = None

    # iterate through each character/delimiter
    for c in findStringEnds(s):
        if type(c) == type((0,)):
            if delim == None:   # if we're starting a string literal
                st.append(''.join(buff))
                buff = []
                delim = c[0]

            elif delim == c[0]: # if we're ending a string literal
                st.append(('literal',''.join(buff)))
                buff = []
                delim = None

            else:
                buff.append(c[0])
        else:
            buff.append(c)
    assert(delim == None)
    st.append(''.join(buff))
    return st

keywords = ['and','or','not','nand','nor','xor','xnor']

# potential substring matches are placed after longer matches, to scan for after
symbols = ['<=','>=','==','[*]{2}','\(','\)','[-]','[+]','[/]','[!]','[+]','[<]','[>]','[*]']
for keyword in keywords:
    symbols += ['(?<![a-zA-Z0-9])' + keyword + '(?![a-zA-Z0-9])'] # matches 'keyword' unless preceded by or followed by an alphanumeric character


def tokenizeExpression(s,scope):
    # set string literals off-limits for further parsing
    s = extractStringLiterals(s)

    # package all meaningful symbols into tuples
    for symbol in symbols:
        temp = []
        for e in s:
            if type(e) == type((0,)):
                temp.append(e)
            else:
                for snippet in re.split('('+symbol+')',e.strip()):
                    snippet = snippet.strip()
                    if re.fullmatch(symbol,snippet):
                        temp.append((snippet,))
                    elif snippet != '':
                        temp.append(snippet)
        s = temp

    # create literals and link variables
    s = buildLiteralsAndVariables(s,scope)

    # everything should be matched by now
    assert(not any([type(e) == type('str') for e in s]))

    return s






























s = "this '''is''' a " + '"""test""" hello <= world "string" testing '
test += [s]






for d in test:
    print(d)
    t = tokenizeExpression(d,None)
    print(t)
    print('\n')


















































