from collections import namedtuple
from pprint import pprint
import re

Tag = namedtuple('Tag','tag value')

def tokenize(line):
    line = line.strip(' ')
    if line == '':
        return []

    match = re.match("^(.*)('[^'].*?')(.*)$",line)
    if match:
        a,b,c = match.groups()
        return tokenize(a) + [Tag('literal',b)] + tokenize(c)
    
    for symbol in list(':,(){}[]=-.+<>'):
        match = re.match('^(.*)[' + symbol + '](.*)$',line)
        if match:
            return tokenize(match.groups()[0]) + [Tag(symbol,symbol)] + tokenize(match.groups()[1])

    for symbol in ['->','==','-=','+=','<=','>=']:
        match = re.match('^(.*)' + symbol + '(.*)$',line)
        if match:
            return tokenize(match.groups()[0]) + [Tag(symbol,symbol)] + tokenize(match.groups()[1])

    for prefix in ['switch','for','while','type','define']:
        match = re.match('^'+prefix+' (.*)$',line)
        if match:
            return [Tag(prefix,prefix)] + tokenize(match.groups()[0])

    match = re.match("^[a-zA-Z0-9]+$",line)
    if match:
        return [Tag('variable',line)]


    match = re.match("^[0-9]+$",line)
    if match:
        return [Tag('literal',line)]
    

    if line == 'print':
        return [Tag('builtin','print')]

    return [line]








