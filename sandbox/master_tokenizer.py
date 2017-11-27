import re
from collections import namedtuple


code = '''
define HTTP:
    receive(req):
        switch req.folder: # something that means what subfolder of the url it was addressed to
            'flic':
                req -> flic.receive
            'facebook':
                req -> facebook.receive

define credentials:
    init:
        self.creds = {'lifx':     'aaaaaaaa',
                      'facebook': 'bbbbbbbb',


        self.creds['lifx']     ->     lifx.setToken
        self.creds['facebook'] -> facebook.setToken

define watchdog:
    init:
        type resp(status,timestamp)
        self.timeout = 30

        self.status = {'lifx':     resp('no response',timestamp()),
                       'facebook': resp('no response',timestamp())}

        while true:
            true ->     lifx.test
            true -> facebook.test
            wait(5)

    receive(service,status):
        self.status[service] = (status,timestamp())
        temp = {}
        for service,stat in self.status:
            if timestamp() < stat.timestamp + self.timeout:
                temp[service] = stat
            else:
                temp[service] = resp('no response',timestamp())
        self.status = temp

    buildReport(ip):
        # blah blah blah
        # html stuff
        # blah blah blah
        # build from self.status
        ip,finishedHTMLreport -> HTTP.send

define flic:
    run(req):
        req.args['button'],req.args['action'] -> main.flic

    test:
        'flic',200 -> watchdog.receive

define main:
    flic(button,action):
        switch button,action:
            'button1','single':
                cmd = {'who':{'lights':'bedroom'},'what':{'state':'on'}}
                cmd,'flic' -> main
            'button1','hold':
                cmd = {'who':{'lights':'bedroom'},'what':{'state':'off'}}
                cmd,'flic' -> main
            'button2','single':
                cmd = {'who':{'lights':'closet'},'what':{'state':'on'}}
                cmd,'flic' -> main
            'button2','hold':
                cmd = {'who':{'lights':'closet'},'what':{'state':'off'}}
                cmd,'flic' -> main
            default:
                'got invalid Flic input',button,action -> logging

    facebook(sender,message):
        # something

    test:
        'main',200 -> watchdog.receive


define facebook:
    init:
        self.url = 'https://graph.facebook.com/v2.6/me/messages?access_token='
        self.accessToken = 'er0fja034fnoaeinrg0a384f0ag'

    receive(req):
        # data = something like req.get_json()
        sender = data['entry'][0]['messaging'][0]['sender']['id']
        message = data['entry'][0]['messaging'][0]['message']['text']

        sender,message -> main.facebook

        # gotta do something to return a 200 to FB

    send(userID,message):
        data = {'recipient': {'id': userID},
                'message': {'text': message}}

        {'type':'post','url':url+accessToken,'data':data} -> HTTP.send

    setToken(token):
        self.accessToken = token

    test:
        'facebook',200 -> watchdog.receive

define lifx:
    init:
        headers = {'Authorization': 'Bearer ' + token}

    off(light):
        url = 'https://api.lifx.com/v1/lights/' + light + '/state'
        data = {'power':state}
        {'type':'put','headers':headers,'url':url,'data':data} -> HTTP.send

    on(light):
        url = 'https://api.lifx.com/v1/lights/' + light + '/state'
        data = {'power':state}
        {'type':'put','headers':headers,'url':url,'data':data} -> HTTP.send

    toggle(light):
        url = 'https://api.lifx.com/v1/lights/' + light + '/toggle'
        {'type':'post','headers':headers,'url':url,'data':{}} -> HTTP.send

    setToken(token):
        headers = {'Authorization': 'Bearer ' + token}

    test:
        'lifx',200 -> watchdog.receive

define weather:
    init:
        self.lat,self.lon = 0.0,0.0

    setLocation(lat,lon):
        self.lat,self.lon = lat,lon
'''




Token = namedtuple('Token','tag value')

tokens = [('()',r'([\(])'),
          ('()',r'([\)])'),
          ('[]',r'([\[])'),
          ('[]',r'([\]])'),
          ('{}',r'([\{])'),
          ('{}',r'([\}])'),
          ('->',r'(->)'),
          (',', r'([,])'),
          ('.', r'([.])'),
          ('=', r'([=])'),
          ('+', r'([+])'),
          (':', r'([:])')]

keywords = ['and','or','not','nand','nor','xor','xnor','define','switch','if','else','self','init','run','type']
for keyword in keywords:
    tokens.append((keyword,'(?<![a-zA-Z0-9])(' + keyword + ')(?![a-zA-Z0-9])')) # matches 'keyword' unless preceded by or followed by an alphanumeric character

def findStringEnds(s):
    '''
    >>> list(findStringEnds('This is a "test" string'))
    ['T', 'h', 'i', 's', ' ', 'i', 's', ' ', 'a', ' ', ('"',), 't', 'e', 's', 't', ('"',), ' ', 's', 't', 'r', 'i', 'n', 'g']
    '''

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



def extractStringLiterals(s):
    '''
    >>> extractStringLiterals('This is a "test" string')
    [Token(tag='unprocessed', value='This is a '), Token(tag='literal', value='test'), Token(tag='unprocessed', value=' string')]
    '''

    st = []
    buff = []
    delim = None

    # iterate through each character/delimiter
    for c in findStringEnds(s):
        if type(c) == type((0,)): # if we received a delimiter
            if delim == None:   # if we're starting a string literal
                if len(buff) > 0:
                    st.append(Token('raw',''.join(buff)))
                buff = []
                delim = c[0]

            elif delim == c[0]: # if we're ending a string literal
                st.append(Token('literal',''.join(buff)))
                buff = []
                delim = None

            else: # if we got for example the " inside 'abc"def'
                buff.append(c[0])
        else: # if we received a char, not a delimiter
            buff.append(c)

    assert(delim == None)
    if len(buff) > 0:
        st.append(Token('raw',''.join(buff)))
    return st


def tokenize(exp):
    #exp = [Token('raw',exp)]
    exp = extractStringLiterals(exp)

    for tag,regex in tokens:
        temp = []
        for e in exp:
            if e.tag == 'raw':
                for snippet in re.split(regex,e.value.strip()):
                    snippet = snippet.strip()
                    if re.fullmatch(regex,snippet):
                        temp.append(Token(tag,snippet))
                    elif snippet != '':
                        temp.append(Token('raw',snippet))
            else:
                temp.append(e)
        exp = temp
    return exp

for line in code.split('\n'):
    for w in tokenize(line):
        if w.tag == 'raw':
            print(w.value)

