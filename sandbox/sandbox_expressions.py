import itertools

def encode(e):
    if e == ('(',):
        return 1
    elif e == (')',):
        return -1
    else:
        return 0

def collapseParentheses(exp):
    temp = []
    buff = []
    for a,b in zip(itertools.accumulate(map(encode,exp)),exp):
        if a == 0:
            if len(buff) > 0:
                temp += [buff]
                buff = []
            else:
                temp.append(b)
        else:
            buff.append(b)

    print(temp)



def parse(exp):
    assert(exp.count(('(',)) == exp.count((')',)))

    collapseParentheses(exp)





test = [('(',),('(',),('(',),(')',),(')',),(')',)]
parse(test)

