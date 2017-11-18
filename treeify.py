def nest(code):
    if code == []:
        return []
    
    nested = [code.pop(0)]
    while len(code) > 0:
        while len(code) > 0 and code[0].spaces == nested[-1].spaces:
            nested.append(code.pop(0))

        t = 0
        while t < len(code) and code[t].spaces > nested[-1].spaces:
            t = t + 1
        
        nested[-1].children = nest(code[:t])
        code = code[t:]
    
    return nested
