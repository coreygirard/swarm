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
Define total:
    Init:
        t = 0

    run(a):
        t = t + a
```        

Functions/agents can easily return data to where it was sent from:

```
Define boomerang:
    run(n):
        n -> sender

Define 
```




Latency reporting

```
Define a(input):
    If someProcessesFailed():
        report() -> error
        report() -> analytics

    Flag, data = input
    If flag == 'feedback’:
        LogAsCompleted(data)
    else:
        (data, timestamp,otherdata) -> b
```




