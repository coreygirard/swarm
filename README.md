# swarm











Basic program structure is defining a set of functions/agents:

```
define a:
    init:
        temp = []

    run(b,c):
        temp.append(b)
        (b,c) -> f
```

Functions/agents have two parts, a part that’s executed repeatedly during program execution and an optional part that’s executed initially

```
define total:
    init:
        t = 0

    run(a):
        t = t + a
```        

Functions/agents can easily return data to where it was sent from:

```
define boomerang:
    run(n):
        n -> sender

define test:
    run(n):
        n = 
```


Functions/agents can easily wait for data from another functions/agents (questionable?)

```
define error:
    run(n):
        while True:
            temp <- errorprone
```


```
define fibonacci:
   init:
       (0,0) -> fibonacci
   
   run(a,b):
       a -> print
       (b,a+b) -> fibonacci
```



Latency reporting

```
define a(input):
    if someProcessesFailed():
        report() -> error
        report() -> analytics

    flag, data = input
    if flag == 'feedback’:
        LogAsCompleted(data)
    else:
        (data, timestamp,otherdata) -> b
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












