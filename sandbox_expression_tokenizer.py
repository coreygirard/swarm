import re

keywords = ['and','or','not','nand','nor','xor','xnor']

def buildLiteralsAndVariables(e,scope):
    temp = []
    for i in e:
        if type(i) != type('str'):
            temp.append(i)
            continue
        
        i = i.strip()
        if re.fullmatch(r'([0-9]+[.][0-9]+)',i):
            temp.append(('literal',float(i)))
        elif re.fullmatch(r'([0-9]+)',i): # integer
            temp.append(('literal',int(i)))
            #temp.append(primitives.PrimitiveLiteral(int(i))) # TODO: handle non-ints
        elif re.fullmatch(r'([a-zA-Z0-9]+)',i) and i not in keywords:
            temp.append(('reference',i))
            #temp.append(primitives.PrimitiveReference(i,scope))
        else:
            temp.append(i)
    e = temp
    return e

symbols = ['<=','>=','==','[*]{2}','\(','\)','[-]','[+]','[/]','[!]']
symbols += ['(?<![*])[*](?![*])', # matches '*' not part of '**'
            '[<](?![=])',         # matches '<' not part of '<='
            '[>](?![=])']         # matches '>' not part of '>='

for keyword in keywords:
    symbols += '(?<![a-zA-Z0-9])' + keyword + '(?![a-zA-Z0-9])', # matches 'keyword' unless preceded by or followed by an alphanumeric character


def tokenizeExpression(e,scope):
    e = [e]
    for reg,actual in [("[']{3}","'''"),('["]{3}','"""'),("[']","'"),('["]','"')]:
        pattern = r'(' + reg + '.*?' + reg + ')'
        #print(pattern)
        temp = []
        for w in e:
            if type(w) != type('str'):
                temp.append(w)
            else:
                for i in re.split(pattern,w):
                    if i.startswith(actual) or i.startswith(actual):
                        i = i[len(actual):-len(actual)]
                        temp.append(('literal',i))
                    else:
                        temp.append(i)

                '''
                for q in i:
                    print(i)
                    print(temp)
                    if q.startswith("'") or q.startswith('"'):
                        while q.startswith("'") or q.startswith('"'):
                            q = q[1:-1]
                        temp.append(('literal',q))
                    else:
                        temp += q
                '''
        e = temp
    print(e)
    
    for symbol in symbols:
        temp = []
        for i in e:
            if type(i) != type('str'):
                temp.append(i)
            else:
                for a in re.split(r'(' + symbol + ')',i):
                    if a.strip() != '':
                        temp += [a.strip()]
        e = temp

    e = buildLiteralsAndVariables(e,scope)
    return e

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
"'string literal' and otherStuff"
]

lit = ' and '.join(["'literal'",
                    '"literal"',
                    """'''literal'''""",
                    '''"""literal"""'''])
test = [lit]

print(lit)

for d in test:
    print(d)
    t = tokenizeExpression(d,None)
    print(t)
    print('\n')

