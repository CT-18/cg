from fractions import Fraction

import numpy as np
import random as rnd

import bentley_ottman_helper
import geometry_utils


def gen_double(l, r):
    return rnd.random() * (r - l) + l


def gen_int(l, r):
    return rnd.randint(l, r)


def gen_point(l, r):
    return np.array([gen_double(l, r), gen_double(l, r)])


def gen_int_point(l, r):
    return np.array([rnd.randint(l, r), rnd.randint(l, r)])


def ordered(seg):
    return [bentley_ottman_helper.min_np_array(seg[0], seg[1]), bentley_ottman_helper.max_np_array(seg[0], seg[1])]


def generate_segments(max_val, n):
    return np.array([ordered([gen_point(-max_val, max_val), gen_point(-max_val, max_val)]) for i in range(n)])


def get_point_on_line(line, x):
    a, b, c = line
    return np.array([x, Fraction((-a * x - c), b)])


def generate_segment_on_line(line, max_val):
    return np.array([get_point_on_line(line, gen_int(-max_val, max_val)) for i in range(2)])


def generate_segments_on_line(max_val, n):
    line = 0, 0, 0
    while line[1] == 0:
        p1 = gen_int_point(-max_val, max_val)
        p2 = gen_int_point(-max_val, max_val)
        line = geometry_utils.make_line(p1, p2)
    return [generate_segment_on_line(line, max_val) for i in range(n)]
