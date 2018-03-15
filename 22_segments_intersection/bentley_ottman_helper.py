import geometry_utils
from geometry_utils import orientation_exact, make_line


def do_intersect(f, s):
    [a, b] = f
    [c, d] = s
    abc = orientation_exact((a, b), c)
    abd = orientation_exact((a, b), d)
    cda = orientation_exact((c, d), a)
    cdb = orientation_exact((c, d), b)

    if abc != abd and cda != cdb:
        return True
    elif abc == abd == cda == cdb == 0:
        # Less or equal
        def leq(a, b):
            return a[0] < b[0] or a[0] == b[0] and a[1] <= b[1]

        # l <= x <= r
        def between(x, l, r):
            return leq(l, x) and leq(x, r)

        if leq(b, a):
            a, b = b, a
        if leq(d, c):
            c, d = d, c

        return (between(c, a, b) or between(d, a, b) or
                between(a, c, d) or between(b, c, d))
    else:
        return False


def intersection_point(f, s):
    fa, fb, fc = make_line(f[0], f[1])
    sa, sb, sc = make_line(s[0], s[1])
    zn = geometry_utils.determinant([fa, fb], [sa, sb])
    if zn != 0:
        return [-geometry_utils.determinant([fc, fb], [sc, sb]) / zn,
                -geometry_utils.determinant([fa, fc], [sa, sc]) / zn]
    return None


def segments_intersection_n2(segments):
    n = len(segments)
    intersection_points = []
    for i in range(n):
        for j in range(i + 1, n):
            if do_intersect(segments[i], segments[j]):
                x = intersection_point(segments[i], segments[j])
                intersection_points.append(x)
    return intersection_points


def max_np_array(a, b):
    for i in range(min(len(a), len(b))):
        if a[i] < b[i]:
            return b
        elif a[i] > b[i]:
            return a
    return a


def min_np_array(a, b):
    return -max_np_array(-a, -b)


def segments_intersection_set(f, s):
    if not do_intersect(f, s):
        return None
    result = intersection_point(f, s)
    if result is None:
        return [max_np_array(min_np_array(f[0], f[1]), min_np_array(s[0], s[1])),
                min_np_array(max_np_array(f[0], f[1]), max_np_array(s[0], s[1]))]
    return result
