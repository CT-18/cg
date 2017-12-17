import numpy as np
from sympy import Point, Ray, Segment
import math 

def is_vertex_of_segment(p, v):
    return p.equals(v.p1) or p.equals(v.p2)


def is_segment(maybe_s):
    return isinstance(maybe_s, Segment) 


def inf_ray(a, b, k):
    ray = None
    step_x = abs(a.x - b.x)
    step_y = abs(a.y - b.y)
    new_b = Point(b.x + step_x, b.y + step_y) 
    
    if (Ray(a, b).contains(new_b)):
        b = Point(b.x + k * step_x, b.y + k * step_y)
    else:
        b = Point(b.x - k * step_x, b.y - k * step_y)
        
    return (b, Ray(a, b))