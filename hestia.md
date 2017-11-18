```
define HTTP:
    receive(request):
        switch req.folder:
            'flic':
                req -> flic

define flic(req):
    run(req):
        button,action = req.args['button'],req.args['action']
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
                'got invalid input',button,action -> logging

    test:
        200 -> sender

define main:
    run():


facebook:
    init:
        url = 'https://graph.facebook.com/v2.6/me/messages?access_token='
        access_token = 'er0fja034fnoaeinrg0a384f0ag'

    send(user_id,message):
        data = {'recipient': {'id': user_id},
                'message': {'text': message}}

        {'type':'post','url':url+access_token,'data':data} -> HTTP.send -


lights:
    off(light):
        url = 'https://api.lifx.com/v1/lights/' + light + '/state'
        data = {'power':state}    
        {'type':'put','url':url,'data':data} -> HTTP.send

    on(light):
        url = 'https://api.lifx.com/v1/lights/' + light + '/state'
        data = {'power':state}    
        {'type':'put','url':url,'data':data} -> HTTP.send

    toggle(light):
        url = 'https://api.lifx.com/v1/lights/' + light + '/toggle'
        {'type':'post','url':url,'data':{}} -> HTTP.send

        










```
