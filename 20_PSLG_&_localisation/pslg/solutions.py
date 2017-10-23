class Point:
    __slots__ = ("x", "y", "enger")

    def __init__(self, x, y, enger):
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

    def __init__(self, origin, twin, next, prev, face):
        self.origin = origin
        self.twin = twin
        self.next = next
        self.prev = prev
        self.face = face


class Face:
    __slots__ = ("edge")

    def __init(self, edge):
        self.edge = edge


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
        self.fig = plt.figure(figsize=(6, 6))
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

        p3 = self.f(p1, p2)

        x, y = p3.exterior.coords.xy
        self.ax1.add_patch(PolygonPatch(p3))
        self.ax1.set_xlim(MIN_X - 1, MAX_X + 1)
        self.ax1.set_ylim(MIN_Y - 1, MAX_X + 1)
        print("result={}".format(p3))
        display(self.fig)
        plt.close()
        return p3


# ______________________________________________________________________________________________________________________

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
        p1 = model.generate_figure(MIN_X + size_x / 2, MIN_Y + size_y / 2, min(size_x, size_y) / 2.5, 0.35, 0.2,
                                   COL_POINTS_FIRST)
        p2 = model.generate_figure(MIN_X + size_x / 2, MIN_Y + size_y / 2, min(size_x, size_y) / 2.5, 0.35, 0.2,
                                   COL_POINTS_SECOND)
        p11 = model.get_polygon(p1)
        p22 = model.get_polygon(p2)
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


def show_test(p1, p2, f):
    model = OverlayModel(f)
    model.draw(p1, p2)
