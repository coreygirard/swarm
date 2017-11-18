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
Swarm uses dynamic typing:
```
v = 5
v -> print
v = 'string'
v -> print
```
```
5
string
```

**Arrays** are one-dimensional containers for variables:
```
(1,2,3)
```
Swarm supports multiple assignment:
```
a,b,c = 1,2,3
a -> print

x = a,b,c
x -> print

i,j,k = x
j -> print
```
```
1
(1,2,3)
2
```
The `.length` member function returns the length of an array:
```
a = (2,4,6,8,9)
a.length -> print
```
```
5
```



## Loops

**For loops** iterate through a provided sequence, making the iterator value available within the loop
```
for n in (2,3,5,7):
    n -> print
```
```
2
3
5
7
```

To provide a range of values, Swarm uses mathematical interval notation. `(` or `)` mean *exclusive*, and `[` or `]` mean *inclusive*. For example:
- `[4:7]` = `[4,5,6,7]`
- `[4:7)` = `[4,5,6]`
- `(4:7]` = `[5,6,7]`
- `(4:7)` = `[5,6]`

```
for i in [0:4):
    i -> print
```
```
0
1
2
3
```
```
a = [4,8,15,16,23,42]
for i in [0:len(a)):
    a[i] -> print
```
```
4
8
15
16
23
42
```

**While loops** are identical to Python. If their condition evaluates to `true`, repeatedly execute the contents of the loop until the condition is no longer `true`.
```
j = 0
while j < 5:
    j -> print
    j += 1
```
```
0
1
2
3
4
```
`break` statements work as expected:
```
j = 1
while true:
    j -> print
    j *= 2
    if j > 16:
        break
```
```
1
2
4
8
16
```
`continue` statements as well:
```
for i in [0:5):
    if i == 3:
        continue
    i -> print
```
```
0
1
2
4
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
A nice feature coming from the fact that both the control and cases are evaluated expressions: it is possible to compare multiple values at once.

```
define switching(n,animal):
        switch n,animal:
            4,'lion':
                'number is 4 and animal is lion' -> print
            4,'bear':
                'number is 4 and animal is bear' -> print
            5,'lion':
                'number is 5 and animal is lion' -> print
            5,'bear':
                'number is 5 and animal is bear' -> print
            default:
                'nothing matched' -> print

define main:
    init:
        4,'lion' -> switching
        5,'tiger' -> switching
        4,'bear' -> switching
        4,'' -> switching
```
```
number is 4 and animal is lion
nothing matched
number is 4 and animal is bear
nothing matched
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


## Programmatic Flow

It is possible to choose at runtime where a `->` statement points:

```
define helper(data,dest):
        data*2 -> ref(dest)

define main:
    init:
        4,'main.receive1' -> helper
        5,'main.receive2' -> helper
        1,'main' -> helper
        3,'main.run' -> helper

    run(n):
        str(n) + ' received by main.run' -> print

    receive1(n):
        str(n) + ' received by main.receive1' -> print

    receive2(n):
        str(n) + ' received by main.receive2' -> print
```
```
8 received by main.receive1
10 received by main.receive2
2 received by main.run
6 received by main.run
```

This can frequently be useful to replace the common function call / return pattern in many languages. Instead of:
```
# python
def doStuff(n):
    return 2*n

def doMoreStuff(n):
    return 3*n

def complicatedFunction(n)
    n = doStuff(n)
    n = doMoreStuff(n)
    return n
```

Swarm would break the function stages apart into subagents:
```
define doStuff(n,dest):
        2*n -> ref(dest)

define doMoreStuff(n,dest):
        3*n -> ref(dest)

define complicatedFunction:
    run(n):
        n,'complicatedFunction.stage2' -> doStuff
        
    stage2(n):
        n,'complicatedFunction.stage3' -> doMoreStuff
        
    stage3(n):
        n -> nextAgent
```

This has the conceptual advantage of more clearly separating a complex process into atomic components, and keeping the syntax clean.



## Some patterns

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
