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










```
