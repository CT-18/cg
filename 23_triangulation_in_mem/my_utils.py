import numpy as np
from sympy import Point, Line, Segment, Ray


def is_vertex_of_segment(p, v):
    return p.equals(v.p1) or p.equals(v.p2)


def is_segment(maybe_s):
    return isinstance(maybe_s, Segment) 


def inf_ray(a, b, k):
    l = Line(a, b)
    c_x, c_y, c_b = l.coefficients
    new_b_x = 0
    new_b_y = 0
    ray = None
    
    if (c_x == 0):
        new_b_y = (-1 * c_x * k - c_b) / c_y
        new_b_x = k
    else:
        new_b_x = (-1 * c_y * k - c_b) / c_x
        new_b_y = k
    
    new_b = Point(new_b_x, new_b_y)
    
    if (Ray(a, b).contains(new_b)):
        b = new_b
    else:
        b = Point(a.x - (new_b_x - a.x), a.y - (new_b_y - a.y))
    
    ray = Ray(a, b)
    return (b, ray)