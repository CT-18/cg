import numpy as np
from sympy import Point, Line, Segment, Ray, intersection

def intersect_ray_and_segment(x_a_ray, y_a_ray, x_b_ray, y_b_ray,
                                      x_a_s, y_a_s, x_b_s, y_b_s):
    r = Ray(Point(x_a_ray, y_a_ray), Point(x_b_ray, y_b_ray)) 
    s = Segment(Point(x_a_s, y_a_s), Point(x_b_s, y_b_s)) 
    return r.intersect(s)

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

def turn(q, h_point1, h_point2):
    ar = np.array([[h_point1.x, h_point1.y, 1],[h_point2.x, h_point2.y, 1],[q.x, q.y, 1]], dtype='float')
    return np.sign(np.linalg.det(ar))