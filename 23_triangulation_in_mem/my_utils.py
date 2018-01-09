import numpy as np
from sympy import Point, Ray, Segment, Line
import math 

def is_vertex_of_segment(p, v):
    return p.equals(v.p1) or p.equals(v.p2)


def is_segment(maybe_s):
    return isinstance(maybe_s, Segment) 


def inf_ray(a, b, mult):
    ab = Line(a, b)
    c_x, c_y, c_b = ab.coefficients
    step_x = a.x - b.x if a.x > b.x else b.x - a.x 
    step_y = a.y - b.y if a.y > b.y else b.y - a.y
    new_b = None
    k = 0
    
    if c_y != 0:
        k = -(c_x / c_y)
        
    if k < 0:
        new_b = Point(b.x + step_x, b.y - step_y)
        
        if (Ray(a, b).contains(new_b) and not new_b.equals(a)):
            b = Point(b.x + mult * step_x, b.y - mult * step_y)
        else:
            b = Point(b.x - mult * step_x, b.y + mult * step_y)
    else:
        new_b = Point(b.x + step_x, b.y + step_y)
        
        if (Ray(a, b).contains(new_b) and not new_b.equals(a)):
            b = Point(b.x + mult * step_x, b.y + mult * step_y)
        else:
            b = Point(b.x - mult * step_x, b.y - mult * step_y)
    
    return (b, Ray(a, b)) 