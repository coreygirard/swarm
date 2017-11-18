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
                {'who':{'lights':'all'},'what':{'state':'on'},'lifx' -> main.lifx

    test:
        200 -> sender

define main:
    run():
```
