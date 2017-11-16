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

## Values
```
define values:
    init:
        'concatenate' + ' ' + 'strings' -> print
        '1 + 1 = ' + string(1+1) -> print
        '7/3 = ' + string(7/3) -> print
        true & false -> print
        true | false -> print
        true xor false -> print
        !false -> print
```
```
concatenate strings
1 + 1 = 2
7/3 = 2.3333333333
false
true
true
true
```


## Variables

```
define vars:
    init:
        s = 'this is a string'
        s -> print
        
        a,b = 1,2
        a,b -> print
        
        c,d = 3,4
        c,d -> print

        e = c,d+1
        e -> print
        
        f,g = e
        f -> print
```
```
initial
(1,2)
(3,4)
(3,5)
3
```

## Loops

```
define looping:
    init:
        for n in (2,3,5,7):
            n -> print

        ' ' -> print

        for i in range(4):
            i -> print

        ' ' -> print

        j = 0
        while j < 5:
            j -> print
            j += 1

        ' ' -> print

        j = 1
        while true:
            j -> print
            j *= 2
            if j > 16:
                break
```
```
2
3
5
7

0
1
2
3

0
1
2
3
4

1
2
4
8
16
```

## If/else

```
define conditions:
    init:
        if 7%2 == 1:
            '7 is odd' -> print
        
        n = -2
        if n == 0:
            'n is zero' -> print
        else if n > 0:
            'n is positive' -> print
        
        n = 3
        if n == 0:
            'n is zero' -> print
        else if n > 0:
            'n is positive' -> print
        else:
            'n is negative' -> print
```
```
7 is odd
n is positive
```

## Switch

```
define switching(n):
        switch n:
            0:
                'equal to 0' -> print
            1+1:
                'equal to 2' -> print
            'apple':
                'non sequitur' -> print
            default:
                'stuff happens' -> print

define main:
    init:
        0 -> switching
        2 -> switching
        'pear' -> switching
```
```
equal to 0
equal to 2
stuff happens
```


## Arrays

```
define functionA:
    init:
        b,c = 'string',5
        b,c -> functionB

define functionB(data):
        b,c = data
        b = b + ', appended'
        c += 2
        b,c -> functionC

define functionC(i,j):
        i -> print
        j -> print

```
```
string, appended
7
```

```
define f:
    init:
        (2,3,5,7) -> print
```
```
(2, 3, 5, 7)
```

```
define f:
    init:
        a = (1,2,3,4,5)
        a[3] = 'apple'
        a[2] -> print
        a[3] -> print
        a -> print
```
```
2
apple
(1, 2, 3, 'apple', 5)
```

## Dictionaries

```
define checkPwd:
    init:
        record = {'Alice':'CyWlfjRd2jmuUCnh',
                  'Wally':'NYiAQpwgPjRJjniQ',
                  'Asok':'8yZ8m3tNdfkEj0PV',
                  'Ted':'CFNoT9eE50uylUpX',
                  'Dogbert':'wUzdR5OirlxoTteU',
                  'Catbert':'kA9bXzNx4B9R3FuE',
                  'Boss':'M1y9NjiBV96wV80L',
                  'Dilbert':'6BPygbOJHp9QT4zu'}
                  
    run(user,hash):
        if record[user] == hash:
            user -> showSecretPage
        else:
            user,hash -> reportInvalidPwd
```

























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
