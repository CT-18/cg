from hidden import turn

def compute_vtype_answer(v1, v2, v3):
    if v1 > v2 and v3 > v2: # greater means below
        if turn(v1,v2,v3) > 0:
            return 'start'
        else:
            return 'split'
    elif v1 < v2 and v3 < v2:
        if turn(v1,v2,v3) > 0:
            return 'end'
        else:
            return 'merge'
    return 'regular'