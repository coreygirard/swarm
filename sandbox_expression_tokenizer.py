import re

keywords = ['and','or','not','nand','nor','xor','xnor']

def buildLiteralsAndVariables(e,scope):
    temp = []
    for i in e:
        i = i.strip()
        if re.fullmatch(r'([0-9]+)',i):
            temp.append(('literal',i))
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
    for symbol in symbols:
        temp = []
        for i in e:
            temp = temp + [a.strip() for a in re.split(r'(' + symbol + ')',i) if a.strip() != '']
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
' and '
]

for d in test:
    print(d)
    t = tokenizeExpression(d,None)
    print(t)
    print('\n')

