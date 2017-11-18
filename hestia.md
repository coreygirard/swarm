```
define HTTP:
    receive(req):
        switch req.folder: # something that means what subfolder of the url it was addressed to
            'flic':
                req -> flic.receive
            'facebook':
                req -> facebook.receive

define credentials:
    init:
        creds = {'lifx':     'aaaaaaaa',
                 'facebook': 'bbbbbbbb',
                 
        creds['lifx']     ->     lifx.setToken
        creds['facebook'] -> facebook.setToken

define watchdog:
    init:
        while true:
            true ->     lifx.test
            true -> facebook.test

    receive(service,status):

define flic(req):
    run(req):
        req.args['button'],req.args['action'] -> main.flic

    test:
        'flic',200 -> watchdog.receive

define main:
    flic(button,action):
        switch button,action:
            'button1','single':
                cmd = {'who':{'lights':'bedroom'},'what':{'state':'on'}
                cmd,'flic' -> main
            'button1','hold':
                cmd = {'who':{'lights':'bedroom'},'what':{'state':'off'}
                cmd,'flic' -> main
            'button2','single':
                cmd = {'who':{'lights':'closet'},'what':{'state':'on'}
                cmd,'flic' -> main
            'button2','hold':
                cmd = {'who':{'lights':'closet'},'what':{'state':'off'}
                cmd,'flic' -> main
            default:
                'got invalid Flic input',button,action -> logging

    facebook(sender,message):
        # something

    test:
        'main',200 -> watchdog.receive


facebook:
    init:
        url = 'https://graph.facebook.com/v2.6/me/messages?access_token='
        access_token = 'er0fja034fnoaeinrg0a384f0ag'

    receive(req):
        # data = something like req.get_json()
        sender = data['entry'][0]['messaging'][0]['sender']['id']
        message = data['entry'][0]['messaging'][0]['message']['text']

        sender,message -> main.facebook
        
        # gotta do something to return a 200 to FB

    send(user_id,message):
        data = {'recipient': {'id': user_id},
                'message': {'text': message}}

        {'type':'post','url':url+access_token,'data':data} -> HTTP.send -

    setToken(token):
        access_token = token

    test:
        'facebook',200 -> watchdog.receive

lifx:
    init:
        headers = {"Authorization": "Bearer %s" % token}

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
        headers = {"Authorization": "Bearer %s" % token}

    test:
        'lifx',200 -> watchdog.receive

define weather:
    init:
        this.lat,this.lon = 0.0,0.0
        self.lat,self.lon = 0.0,0.0
        lat,lon = 0.0,0.0
        
    setLocation(lat,lon):
        lat,lon = lat,lon






```
