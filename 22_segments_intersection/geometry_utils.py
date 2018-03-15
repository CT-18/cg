from fractions import Fraction
import numpy as np


def calculate_arg(a, b):
    return abs(a[0] * b[1]) + abs(b[0] * a[1])


def calculate_det(a, b):
    return a[0] * b[1] - b[0] * a[1]


def determinant(a, b):
    return a[0] * b[1] - b[0] * a[1]


def orientation_exact(x, c):
    a, b = x
    ca = a - c
    cb = b - c
    e = 8 * np.finfo(float).eps * calculate_arg(ca, cb)
    det = determinant(ca, cb)
    if det > e:
        return 1
    if det < -e:
        return -1

    lc = (Fraction(c[0]), Fraction(c[1]))
    la = (Fraction(a[0]) - lc[0], Fraction(a[1]) - lc[1])
    lb = (Fraction(b[0]) - lc[0], Fraction(b[1]) - lc[1])
    ldet = la[0] * lb[1] - la[1] * lb[0]
    if ldet > 0:
        return 1
    if ldet < 0:
        return -1
    return 0


def make_line(a, b):
    return a[1] - b[1], b[0] - a[0], a[0] * b[1] - a[1] * b[0]
