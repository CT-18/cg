#from cg import turn
from hidden import turn

def is_outer_answer(v0,v1,v2,v):
    # Допущение для триангуляции многоугольников с дырками, позволяющее сохранять полигон
    # корректным после слияния внешней и внутренней частей двумя налегающими друг на друга ребрами.
    prop = v == v0 or v == v1 or v == v2
    return prop or turn(v0, v1, v)<= -1 or turn(v1, v2, v) <= -1 or turn(v2, v0, v) <= -1 

