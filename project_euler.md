
### Problem 1

If we list all the natural numbers below 10 that are multiples of 3 or 5, we get 3, 5, 6 and 9. The sum of these multiples is 23.

Find the sum of all the multiples of 3 or 5 below 1000.

```
define driver:
    init:
        for n in range(1000):
            n -> filter5
        -1 -> filter5

define filter5(n):
        if n%5 == 0 or n == -1:
            n -> filter3

define filter3(n):
        if n%3 == 0 or n == -1:
            n -> sum

define sum:
    init:
        total = 0
        
    run(n):
        if n == -1:
            total -> print
        else:
            total += n
```



