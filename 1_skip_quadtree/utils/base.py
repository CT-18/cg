import enum
import numpy.random

class Quarter(enum.Enum):
    LT = 0
    LB = 1
    RT = 2
    RB = 3

def contains(bounds, point):
    x, y = point
    left, right, bottom, top = bounds
    return x > left and x <= right and y > bottom and y <= top 

def quarter_by(bounds, point):
    if not contains(bounds, point):
        return None
    x, y = point
    left, right, bottom, top = bounds

    x_mid = (left + right) / 2
    y_mid = (bottom + top) / 2
    if x <= x_mid:
        if y <= y_mid:
            return Quarter.LB
        else:
            return Quarter.LT
    else:
        if y <= y_mid:
            return Quarter.RB
        else:
            return Quarter.RT


_quarter_bounds = {}
_quarter_bounds[Quarter.LT] = lambda b: (b[0], (b[0] + b[1]) / 2, (b[2] + b[3]) / 2, b[3])
_quarter_bounds[Quarter.LB] = lambda b: (b[0], (b[0] + b[1]) / 2, b[2], (b[2] + b[3]) / 2)
_quarter_bounds[Quarter.RT] = lambda b: ((b[0] + b[1]) / 2, b[1], (b[2] + b[3]) / 2, b[3])
_quarter_bounds[Quarter.RB] = lambda b: ((b[0] + b[1]) / 2, b[1], b[2], (b[2] + b[3]) / 2)

def quarter_bounds(bounds, quarter):
    return _quarter_bounds[quarter](bounds)        

class Node:
    
    def __init__(self, bounds=None, children=None, data=None):
        self.bounds = bounds
        self.children = children
        self.data = data
    
    def simple(self):
        return self.children is None
    
    def empty(self):
        return (self.children is None) and (self.data is None)

_p = 0.5

def rnd_bool():
    return numpy.random.choice([False, True], p=[1 - _p, _p])
