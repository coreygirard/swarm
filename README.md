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




