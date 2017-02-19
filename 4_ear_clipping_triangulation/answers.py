from hidden import turn

def is_outer_answer(v0,v1,v2,v):
    return turn(v0, v1, v)<= -1 or turn(v1, v2, v) <= -1 or turn(v2, v0, v) <= -1 

