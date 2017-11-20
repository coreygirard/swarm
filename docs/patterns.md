
## Scaling

### Unscaled

```
define stream:
    init:
        while true:
            4 -> slow
            wait(1)

define slow(n):
        wait(5)
        n*2 -> print
```

### Static scaling

```
define stream:
    init:
        while true:
            4 -> slow
            wait(1)


define slow:
    init:
        self.run2.instances.desired = 5
        self.i = 0

    run(n):
        n -> slow[self.i]
        self.i = (self.i+1) % self.run2.instances.current

    run2(n):
        wait(5)
        n*2 -> print
```

### Dynamic scaling

```
define stream:
    init:
        while true:
            4 -> loadBalancer            
            wait(1)

define slow:
    init:
        self.i = 0
        
        self.run2.instances.min = 1
        self.run2.instances.max = 5

        self.run2.instances.desired = 1

    run(n):
        self.i = self.i % self.run2.instances.current
        4 -> b[self.i]
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
        n*2 -> b
```


---
