
## Scaling / Elasticity

Swarm also provides easy ways to elastically scale 'microservices'. For example, take a simple flow:

### Unscaled

```
define fast:
    init:
        while true:
            4 -> slow
            wait(1)

define slow(n):
        wait(5)
        n*2 -> print
```

It appears we have quite a bottleneck in the agent `slow`. If only we could have more of them. Rather than forcing the user to fiddle with copy-pasting and renaming, Swarm offers easy static duplication of agents:

### Static scaling

```
define fast:
    init:
        while true:
            4 -> slow
            wait(1)


define slow:
    init:
        self.run2.instances.desired = 5

    run(n):
        # Here we randomly choose an instance
        i = random.choice([0:self.run2.instances.current))
        n -> slow[i]

    run2(n):
        wait(5)
        n*2 -> print
```

We can also scale elastically at runtime, based on perceived demand:

### Dynamic scaling

```
define fast:
    init:
        while true:
            4 -> slow          
            wait(1)

define slow:
    init:
        self.i = 0
        
        self.run2.instances.min = 1
        self.run2.instances.max = 5

        self.run2.instances.desired = 1

    run(n):
        # Here we distribute to the instances sequentially
        self.i = self.i % self.run2.instances.current
        n -> b[self.i]
        self.i += 1
        
        totalQueue = 0
        for e in slow.instances:
            totalQ += e.queue.length
        avgQueue = totalQueue / self.run2.instances.current
        
        if avgQueue > someThreshold and self.run2.instances.desired < self.run2.instances.max:
            self.run2.instances.desired += 1
        
        if avgQueue < someOtherThreshold and self.run2.instances.desired > self.run2.instances.min:
            self.run2.instances.desired -= 1            

    run2(n):
        wait(5)
        n*2 -> print
```

## String tricks

using .replace to automatically append {{{ and }}} to things in a dictionary 


---
