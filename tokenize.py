from collections import namedtuple
from pprint import pprint
import re

Tag = namedtuple('Tag','tag value')

def tokens(line):
    line = line.strip(' ')
    if line == '':
        return []

    # grab string literals
    match = re.match("^(.*)('[^'].*?')(.*)$",line)
    if match:
        a,b,c = match.groups()
        return tokens(a) + [Tag('literal',b)] + tokens(c)

    for symbol in list(':,(){}[]=-.+<>'):
        match = re.match('^(.*)[' + symbol + '](.*)$',line)
        if match:
            return tokens(match.groups()[0]) + [Tag(symbol,symbol)] + tokens(match.groups()[1])

    for symbol in ['->','==','-=','+=','<=','>=']:
        match = re.match('^(.*)' + symbol + '(.*)$',line)
        if match:
            return tokens(match.groups()[0]) + [Tag(symbol,symbol)] + tokens(match.groups()[1])

    match = re.match('^(.*) in (.*)$',line)
    if match:
        return tokens(match.groups()[0]) + [Tag('in','in')] + tokens(match.groups()[1])

    for prefix in ['if','else','else if','switch','for','while','type','define']:
        match = re.match('^'+prefix+' (.*)$',line)
        if match:
            return [Tag(prefix,prefix)] + tokens(match.groups()[0])

    for symbol in ['->','==','-=','+=','<=','>=']:
        match = re.match('^(.*)' + symbol + '(.*)$',line)
        if match:
            return tokens(match.groups()[0]) + [Tag(symbol,symbol)] + tokens(match.groups()[1])


    match = re.match("^[a-zA-Z][a-zA-Z0-9]*$",line)
    if match:
        return [Tag('variable',line)]


    match = re.match("^[0-9]+$",line)
    if match:
        return [Tag('literal',line)]
    

    if line == 'print':
        return [Tag('builtin','print')]

    return [line]

def tokenize(lines):
    for i in range(len(lines)):
        #print(lines[i].code)
        lines[i].code = tokens(lines[i].code)
        #print(' '.join([e.tag for e in lines[i].code]))
        #print('\n')
    return lines





