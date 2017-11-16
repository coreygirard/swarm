# Swarm

## Hello World

```
define hello:
    init:
        "Hello World!" -> print
```
```
Hello World!
```

## Functions/agents

Basic program structure is defining a set of **functions/agents**:

```
define average:
    init:
        total,n = 0,0

    run(e):
        total,n = total+e,n+1
        total/n -> print
```

**Functions/agents** have two specially named parts:

- `init` is executed once initially
- `run` is executed repeatedly, every time data is sent to the function/agent

```
define total:
    init:
        t = 0

    run(e):
        t = t + e
        t -> print
```        

```
define fibonacci:
   init:
       (0,0) -> fibonacci
   
   run(a,b):
       a -> print
       (b,a+b) -> fibonacci
```

Any number of other inputs can be defined, sent to via the `.` command, for example `agent.input`

```

define example:
    init:
        # do stuff
        
    run(n):
        n + ' received by example.run' -> print
        
    a(n):
        n + ' received by example.a' -> print

    b(n):
        n + ' received by example.b' -> print

define test:
    init:
        5 -> example
        4 -> example.run
        3 -> example.a
        2 -> example.b
```

```
5 received by example.run
4 received by example.run
3 received by example.a
2 received by example.b
```

Both `init` and `run` are optional. The following is completely valid:

```
define example:
    alternateInput(n):
        # do things
```

In the above example, the command `42 -> example` would be invalid (because `run` hasn't been defined), but `42 -> example.alternateInput` would work.


When `run` is the only section defined, it can be abridged. The following two definitions are equivalent:
```
define example:
    run(n):
        n -> other
```
```
define example(n):
        n -> other
```






```


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
        if record[user] == hash:
            ip,user,'secretPage' -> servePage
        else:
            ip,user,'passwordDenied' -> servePage


```


## Basic text chat server
```
define handleRequests(req):
    switch req.port:
        8080:
            req -> checkPwd
        8000:
            req -> userManager.sendMsg
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





























## Structures

**Structures** are defined outside of functions/agents:

```
type point(x,y)

define shift:
    init:
        delta = point(0,0)

    run(p):
        point(p.x+delta.x,p.y+delta.y) -> nextThing
    
    changeShift(p):
        delta.x,delta.y = p.x,p.y

```



















Latency reporting

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



Example basic text handler

```
define HTTP:
    run(req):
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
