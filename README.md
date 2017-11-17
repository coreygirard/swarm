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

## Conceptual structure

The design of **Swarm** is meant to emulate the design paradigm of microservice architecture on a smaller scale (think one server instance rather than many). To that end, the overall structure is analogous to a set of distinct processes that communicate via HTTP-style requests. These pseudo-processes are called 'agents', and the requests are handled via the 'send' command (`->`).

## The `send` command

Understanding the 'send' command is critical for effective programming in Swarm. **Agents** don't communicate through traditional function calls, such as the following (Python):

```
def doubleIt(n):
    return n*2

def tripleIt(n):
    return n*3

def f(n):
    return tripleIt(doubleIt(n))

print(f(1))
```
Here, `f` is called, and execution of everything else stops. Then `f` calls `doubleIt`, and `f` stops to wait for the results returned by `doubleIt`. Once `f` resumes, it then calls `tripleIt` again, and again waits for results. Finally, it returns the result back to the `print` function. **Swarm** handles this rather differently:

```
define main:
    init:
        1 -> doubleIt
        
define doubleIt(n):
        n*2 -> tripleIt
        
define tripleIt(n):
        n*3 -> print
```
The send command (`->`) sends the data on its left to the **agent** on its right. Mechanically, this can be modelled as the following: **agents** have a data queue, and they repeatedly pop items from the front of the queue and execute themselves on that data, for as long as there is data in the queue. The send command appends a piece of data to the back of that queue. This way, it is possible for these components to communicate in a non-blocking fashion.



## Agents

Basic program structure is defining a set of **agents**:

```
define average:
    init:
        total,n = 0,0

    run(e):
        total,n = total+e,n+1
        total/n -> print
```

**Agents** have two specially named parts:

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

Any number of other inputs can be defined, sent to via the `.` command, for example `agent.input`. Sending data to the function name itself, ie `-> agent` is equivalent to sending to the `.run` subagent, ie `-> agent.run`

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

In the above example, the command `42 -> example` would be invalid (because `example.run` hasn't been defined), but `42 -> example.alternateInput` would work.


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

You can imagine each **agent** as a process, and each **subagent** as a thread within that process. the `init` command, when used within an **agent**'s definition, will initialize variables that are shared among all **subagents**

## Structures

**Structures** are defined inside the `init` section of an agent:

```

define shift:
    init:
        type point(x,y)
        delta = point(0,0)

    run(p):
        p = point(p)
        point(p.x+delta.x,p.y+delta.y) -> nextThing
    
    changeShift(p):
        delta.x,delta.y = p.x,p.y

```

## Built-in Agents

Certain agent names, such as `print`, `error`, `logging`, and `analytics`, are already assigned to internal functionality, and are therefore invalid for user-defined agents. They can, and should, be *sent* to, however:

### error
```
define example:
    init:
        'This is an example error' -> error
```
```
ERROR in 'example': This is an example error
```

### print
```
'Strings work' -> print
5 -> print
'Integers work',5 -> print

' ' -> print.separator
for i in [0:5):
    i -> print

'\n' -> print

', ' -> print.separator
for i in [0:5):
    i -> print
0, 1, 2, 3, 4,

        
```
```
Strings work
5
'Integers work',5
0 1 2 3 4
0, 1, 2, 3, 4,
```

### logging (to file)
```
define example:
    init:
        'Something happened' -> logging
        'Something else happened' -> logging
        wait(3)
        'And another thing -> logging
```
```
# excerpt of logging text file
1510933165: [2017-11-17 3:39:25 PM GMT] [example] Something happened
1510933165: [2017-11-17 3:39:25 PM GMT] [example] Something else happened
1510933168: [2017-11-17 3:39:28 PM GMT] [example] And another thing
```

### logging (to screen)
```
define example:
    init:
        true -> logging.toScreen
        false -> logging.toFile
        'Something happened' -> logging
        'Something else happened' -> logging
        wait(3)
        'And another thing' -> logging
```
```
1510933165: [2017-11-17 3:39:25 PM GMT] [example] Something happened
1510933165: [2017-11-17 3:39:25 PM GMT] [example] Something else happened
1510933168: [2017-11-17 3:39:28 PM GMT] [example] And another thing
```

### analytics

```
define example:
    init:
        'apple' -> analytics
        'pear' -> analytics
        wait(4)
        'apple' -> analytics
        wait(3*60)
        'apple' -> analytics
```
```
# analytics text file
tag: 'apple'
[2017-11-17 3:39:25 - 3:39:30 PM GMT] : 2
[2017-11-17 3:42:25 - 3:42:30 PM GMT] : 1

tag: 'pear'
[2017-11-17 3:39:25 - 3:39:30 PM GMT] : 1
```
(Specification for `analytics` is subject to change)


## User-modified agents

Certain pre-existing agents are meant to be user-defined in order to add certain functionality, such as the `HTTP` agent:

```
define HTTP:
    receive(req):
        req -> server

define server:
    init:
        ip,'Hello' -> HTTP.send
        
    run(req):
        'Received something' -> print
```
`HTTP.send` can be sent to, but cannot be user-defined. `HTTP.receive` should be defined in order to route incoming HTTP traffic to various other agents in the program.




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
