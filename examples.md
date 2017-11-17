# Examples

## Hello World (server version)

```
define HTTP:
    receive(req):
        req.from,'Hello World' -> HTTP.send
```

## Easy Analytics

This simple wrapper sends a copy of every inbound or outbound request to the `analytics` agent.

```
define HTTP:
    receive(req):
        req -> analytics
        # other stuff
        ip -> server
    
    sendWrapper(ip,msg):
        ip,msg -> analytics
        ip,msg -> this.send

define server(ip):
        ip,'Hello' -> HTTP.sendWrapper
```

## Basic text chat server
```
define HTTP:
    receive(req):
        switch req.port:
            8080:
                # some processing happens
                ip,user,hash -> checkPwd
            8000:
                # some processing happens
                ip,sender,receiver,message -> userManager.sendMsg
            default:
                req -> error

define checkPwd:
    init:
        record = {'Alice':   'CyWlfjRd2jmuUCnh',
                  'Wally':   'NYiAQpwgPjRJjniQ',
                  'Asok':    '8yZ8m3tNdfkEj0PV',
                  'Ted':     'CFNoT9eE50uylUpX',
                  'Dogbert': 'wUzdR5OirlxoTteU',
                  'Catbert': 'kA9bXzNx4B9R3FuE',
                  'Boss':    'M1y9NjiBV96wV80L',
                  'Dilbert': '6BPygbOJHp9QT4zu'}

    run(ip,user,hash):
        if record.get(user,'') == hash:
            ip,user -> userManager.login
        else:
            ip,user,'passwordDenied' -> servePage

define userManager:
    init:
        loggedIn = {}
        
    login(ip,user):
        loggedIn[user] = (ip,timestamp())

    sendMsg(ip,sender,receiver,message):
        if sender in loggedIn and receiver in loggedIn:
            i,t = loggedIn[sender]
            if i == ip and timestamp()-t < 60*5:
                receiverIP,_ = loggedIn[receiver]
                sender,receiver,receiverIP,message -> routeMsg
        else if sender not in loggedIn:
            i,'Please log in to chat' -> sendError
        else if receiver not in loggedIn:
            i,'''This person isn't available right now''' -> sendError
                
                    
    

```
















































### Latency reporting

```

define stage1:
    init:
        inTransit = {}

    run(n):
        inTransit.append((n,getTimestamp()))
        n -> c
        
    confirm(n,t):
        if n not in inTransit:
            ('not registered',n) -> error
        else:
            sentAt = get n from inTransit
            delete n from inTransit
            t-sentAt -> analytics

define stage2(n):
        n = process(n)
        
        (n,getTimestamp()) -> stage1.confirm
        n -> stage3

```



### Example basic smart home handler

```
define HTTP(req):
        switch req.from:
            8000:
                req -> something
            8080:
                req -> parseFromFB
                
define parseFromFB(req):
        generateConfirmation(req) -> sendHTTP
        ('FB',req) -> parse
        
define parse(from,req):
        (from,req) -> analytics
        switch req.payload:
            'lights':
                req -> lifx
            'camera':
                req -> nest
            'action':
                req -> alarm
            default:
                'ERROR',req -> error

define lifx(cmd):
        switch cmd:
            'on':
                ('bedroom','on','#LIFX_URL#') -> sendHTTP
            'off':
                ('bedroom','off','#LIFX_URL#') -> sendHTTP
            default:
                'ERROR',req -> error

define test:
    init:
        {'request':{'lights':'on'}} -> parseFromFB
        {'request':{'lights':'off'}} -> parseFromFB
        {'request':{'lights':'on'}} -> parseFromFB
        {'request':{'lights':'on'}} -> parseFromFB

```
