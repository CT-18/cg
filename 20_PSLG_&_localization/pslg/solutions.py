class Point:
    __slots__ = ("x", "y", "enger")

    def __init__(self, x, y, enger=None):
        self.x = x
        self.y = y
        self.enger = enger

    def __lt__(self, p):
        return self.x < p.x or (self.x == p.x and self.y < p.y)

    def __eq__(self, p):
        return self.x == p.x and self.y == p.y

    def __gt__(self, p):
        return not (self < p or self == p)

    def __repr__(self):
        return "(%r,%r)" % (self.x, self.y)

    def __hash(self):
        return hash(str(self))


class HalfEdge:
    __slots__ = ("origin", "twin", "next", "prev", "face")

    def __init__(self, origin, twin=None, next=None, prev=None, face=None):
        self.origin = origin
        self.twin = twin
        self.next = next
        self.prev = prev
        self.face = face


class Face:
    __slots__ = ("edge")

    def __init(self, edge):
        self.edge = edge


def get_next_closest_edge_cw(he):
    pass


def get_prev_closest_edge_cw(he):
    pass


class Edge:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __eq__(self, other):
        return self.a == other.a and self.b == other.b


def event(he1, he2, point):
    # ----------- new edges
    h11 = HalfEdge(Edge(he1.origin.a, point))
    h12 = HalfEdge(Edge(point, he1.origin.b))
    h13 = HalfEdge(Edge(he1.origin.b, point))
    h14 = HalfEdge(Edge(point, he1.origin.a))

    h21 = HalfEdge(Edge(he2.origin.a, point))
    h22 = HalfEdge(Edge(point, he2.origin.b))
    h23 = HalfEdge(Edge(he2.origin.b, point))
    h24 = HalfEdge(Edge(point, he2.origin.a))

    # ------------ Twin()
    h11.twin = h14
    h14.twin = h11
    h12.twin = h13
    h13.twin = h12

    h21.twin = h24
    h24.twin = h21
    h22.twin = h23
    h23.twin = h22

    # ------------ Next()
    h11.next = h22
    h22.next = h23
    h23.next = h12
    h12.next = h13
    h13.next = h24
    h24.next = h21
    h21.next = h14
    h14.next = h11

    # ------------ Prev()
    h11.prev = h14
    h22.prev = h11
    h23.prev = h22
    h12.prev = h23
    h13.prev = h12
    h24.prev = h13
    h21.prev = h24
    h14.prev = h21

    return [h11, h12, h13, h14, h21, h22, h23, h24]


def print_error(msg, i=0):
    print("Test №{} failed".format(i + 1))
    print(msg)


def test_event(f, n=1):
    for j in range(0, n):
        if j % 2 == 0 and j != 0:
            print('passed {} tests'.format(j))

        he1 = HalfEdge(Edge(Point(1, 2), Point(3, 2)))
        he1t = HalfEdge(Edge(Point(3, 2), Point(1, 2)))
        he1.twin = he1t
        he1t.twin = he1
        he2 = HalfEdge(Edge(Point(2, 1), Point(2, 3)))
        he2t = HalfEdge(Edge(Point(2, 3), Point(2, 1)))
        he2.twin = he2t
        he2t.twin = he2
        p = Point(2, 2)

        answer = event(he1, he2, p)
        result = f(he1, he2, p)
        if len(result) == len(answer):
            for i in range(0, len(result)):
                if result[i].origin != answer[i].origin:
                    print_error("incorrect origin", j)
                elif result[i].twin.origin != answer[i].twin.origin:
                    print_error("incorrect twin", j)
                elif result[i].next.origin != answer[i].next.origin:
                    print_error("incorrect next", j)
                elif result[i].prev.origin != answer[i].prev.origin:
                    print_error("incorrect prev", j)
                else:
                    continue
                return
        else:
            print_error("incorrect amount of half-edges", j)
            return
    print("All tests passed")


# ______________________________________________________________________________________________________________________

MAX_X = 20
MIN_X = 0
MAX_Y = 20
MIN_Y = 0
COL_POINTS_FIRST = 20
COL_POINTS_SECOND = 20

import math, random
import matplotlib.pyplot as plt
import numpy as np
from shapely.geometry.polygon import Polygon
from descartes import PolygonPatch
from IPython.display import display


def overlaying(p1, p2):
    return p1.intersection(p2)


# ______________________________________________________________________________________________________________________

class OverlayModel:
    def __init__(self, f=overlaying):
        self.f = f
        self.fig = plt.figure(figsize=(3, 3))
        self.ax1 = plt.subplot(111, aspect='equal')
        self.q = []

    def clip(self, x, min, max):
        if min > max:
            return x
        elif x < min:
            return min
        elif x > max:
            return max
        else:
            return x

    def generate_figure(self, ctrX, ctrY, aveRadius, irregularity, spikeyness, numVerts):
        irregularity = self.clip(irregularity, 0, 1) * 2 * math.pi / numVerts
        spikeyness = self.clip(spikeyness, 0, 1) * aveRadius

        # generate n angle steps
        angle_steps = []
        lower = (2 * math.pi / numVerts) - irregularity
        upper = (2 * math.pi / numVerts) + irregularity
        sum = 0
        for i in range(numVerts):
            tmp = random.uniform(lower, upper)
            angle_steps.append(tmp)
            sum = sum + tmp

        # normalize the steps so that point 0 and point n+1 are the same
        k = sum / (2 * math.pi)
        for i in range(numVerts):
            angle_steps[i] = angle_steps[i] / k

        # now generate the points
        points = []
        angle = random.uniform(0, 2 * math.pi)
        for i in range(numVerts):
            r_i = self.clip(random.gauss(aveRadius, spikeyness), 0, 2 * aveRadius)
            x = ctrX + r_i * math.cos(angle)
            y = ctrY + r_i * math.sin(angle)
            points.append((int(x), int(y)))

            angle = angle + angle_steps[i]

        return points

    def draw_point(self, point, color='red', look='.'):
        q1, = self.ax1.plot(point[0], point[1], look, color=color)
        self.q.insert(-1, q1)

    def get_polygon(self, p):
        points = []
        for i in range(-1, len(p)):
            points.insert(-1, (p[i][0], p[i][1]))
        return Polygon(points)

    def draw_line(self, pointStart, pointEnd, color='red', look='-'):
        q1, = self.ax1.plot([pointStart[0], pointEnd[0]], [pointStart[1], pointEnd[1]], look, color=color)
        self.q.insert(-1, q1)

    def redraw_closest(self, point, color='black', look='--'):
        points = np.array(point)
        for i in range(len(points)):
            self.draw_point(point[i], color)
            self.draw_line(point[i - 1], point[i], color, look)

    def on_release(self, event):
        for i in range(len(event)):
            event[i].remove()
        self.q = []

    def draw(self, p1, p2):
        self.fig.canvas.mpl_connect('button_release_event', self.on_release)
        self.redraw_closest(p1, 'black', '-')
        self.redraw_closest(p2, 'red', '-')

        p1 = self.get_polygon(p1)
        p2 = self.get_polygon(p2)
        if p1.intersects(p2):
            p3 = self.f(p1, p2)
            print("result={}".format(p3))

            x, y = p3.exterior.coords.xy
            self.ax1.add_patch(PolygonPatch(p3))
        self.ax1.set_xlim(MIN_X - 1, MAX_X + 1)
        self.ax1.set_ylim(MIN_Y - 1, MAX_X + 1)

        display(self.fig)
        plt.close()
        if p1.intersects(p2):
            return p3
        return None


# ______________________________________________________________________________________________________________________

def get_poligons(model, size_x, size_y):
    p1 = model.generate_figure(MIN_X + size_x / 2, MIN_Y + size_y / 2, min(size_x, size_y) / 2.5, 0.35, 0.2,
                               COL_POINTS_FIRST)
    p2 = model.generate_figure(MIN_X + size_x / 2, MIN_Y + size_y / 2, min(size_x, size_y) / 2.5, 0.35, 0.2,
                               COL_POINTS_SECOND)
    p11 = model.get_polygon(p1)
    p22 = model.get_polygon(p2)
    return p11, p22, p1, p2


def test_overlaying(f, n=10):
    model = OverlayModel()
    for i in range(0, n):
        if i % 2 == 0 and i != 0:
            print('passed {} tests'.format(i))
        size_x = MAX_X - MIN_X - 1
        if size_x < 0:
            raise Exception('MAX_X must be more than MIN_X')
        size_y = MAX_Y - MIN_Y - 1
        if size_y < 0:
            raise Exception('MAX_Y must be moer than MIN_Y')
        p11, p22, p1, p2 = get_poligons(model, size_x, size_y)
        result = overlaying(p11, p22)
        answer = f(p11, p22)
        if answer == result:
            continue
        else:
            print("Test №{} failed".format(i + 1))
            print("Expected {}, result {}".format(answer, result))
            print("points_1={}".format(p1))
            print("points_2={}".format(p2))
            model.draw(p1, p2)
            return
    print("All tests passed")


def show_test(p1, p2, f=overlaying):
    model = OverlayModel(f)
    model.draw(p1, p2)


def inside(g1, g2):
    p1 = Polygon(g1)
    p2 = Polygon(g2)
    return p1.contains(p2)


def test_inside(f, n=10):
    model = OverlayModel()
    for i in range(0, n):
        if i % 2 == 0 and i != 0:
            print('passed {} tests'.format(i))
        p1, p2, arr1, arr2 = get_poligons(model, MAX_X - MIN_X - 1, MAX_Y - MIN_Y - 1)
        answer = inside(arr1, arr2)
        result = f(arr1, arr2)
        if answer == result:
            continue
        else:
            print("Test №{} failed".format(i + 1))
            print("Expected {}, result {}".format(answer, result))
            print("points_1={}".format(arr1))
            print("points_2={}".format(arr2))
            model.draw(p1, p2)
            return
    print("All tests passed")
