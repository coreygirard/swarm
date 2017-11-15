# Swarm

## Functions/agents

Basic program structure is defining a set of **functions/agents**:

```
define a:
    init:
        temp = []

    run(b,c):
        temp.append(b)
        (b,c) -> f
```

**Functions/agents** usually have two parts, a part that’s executed repeatedly during program execution and an optional part that’s executed initially

```
define total:
    init:
        t = 0

    run(a):
        t = t + a
```        

```
define fibonacci:
   init:
       (0,0) -> fibonacci
   
   run(a,b):
       a -> print
       (b,a+b) -> fibonacci
```

Any number of inputs can be defined, sent to via the `.` command, for example `agent.input`

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
        1 -> example
        2 -> example.run
        3 -> example.a
        4 -> example.b
```

```
1 received by example.run
2 received by example.run
3 received by example.a
4 received by example.b
```

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
