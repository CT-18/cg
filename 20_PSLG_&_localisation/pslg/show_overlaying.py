class Point:
    __slots__ = ("x", "y", "enger")

    def __init__(self, x, y, enger):
        self.x = x
        self.y = y
        self.enger = rep

    def __lt__(self, p):
        return self.x < p.x or (self.x == p.x and self.y < p.y)

    def __eq__(self, p):
        return self.x == p.x and self.y == p.y

    def __gt__(self, p):
        return not (self < p or self == p)

    def __repr__(self):
        return "(%r,%r)" % (self.x, self.y)

    def __hash(self):
        return hash(str(selft))


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


# ________________________________________________________________________________________________

import math, random
import matplotlib.pyplot as plt
import numpy as np
from descartes import PolygonPatch
from sympy import Polygon as sympyPolygon  # -> пересечение границ
from sympy import Segment, Point2D

from ipywidgets import interact
from IPython.display import display

MAX_X = 20
MIN_X = 0
MAX_Y = 20
MIN_Y = 0
COL_POINTS_FIRST = 20
COL_POINTS_SECOND = 20


def generateFigure(ctrX, ctrY, aveRadius, irregularity, spikeyness, numVerts):
    irregularity = clip(irregularity, 0, 1) * 2 * math.pi / numVerts
    spikeyness = clip(spikeyness, 0, 1) * aveRadius

    # generate n angle steps
    angleSteps = []
    lower = (2 * math.pi / numVerts) - irregularity
    upper = (2 * math.pi / numVerts) + irregularity
    sum = 0
    for i in range(numVerts):
        tmp = random.uniform(lower, upper)
        angleSteps.append(tmp)
        sum = sum + tmp

    # normalize the steps so that point 0 and point n+1 are the same
    k = sum / (2 * math.pi)
    for i in range(numVerts):
        angleSteps[i] = angleSteps[i] / k

    # now generate the points
    points = []
    angle = random.uniform(0, 2 * math.pi)
    for i in range(numVerts):
        r_i = clip(random.gauss(aveRadius, spikeyness), 0, 2 * aveRadius)
        x = ctrX + r_i * math.cos(angle)
        y = ctrY + r_i * math.sin(angle)
        points.append((int(x), int(y)))

        angle = angle + angleSteps[i]

    return points


def clip(x, min, max):
    if (min > max):
        return x
    elif (x < min):
        return min
    elif (x > max):
        return max
    else:
        return x


fig = plt.figure(figsize=(6, 6))
ax1 = plt.subplot(111, aspect='equal')

q = []


def redrawClosest(point, color='black', look='--', lookPoint='o'):
    for i in range(len(point)):
        drawPoint(point[i], color, lookPoint)
        drawLine(point[i - 1], point[i], color, look)


def drawIntersection(p):
    return


def drawPoint(point, color='red', look='.'):
    q1, = ax1.plot(point[0], point[1], look, color=color)
    q.insert(-1, q1)


def drawLine(pointStart, pointEnd, color='red', look='-'):
    q1, = ax1.plot([pointStart[0], pointEnd[0]], [pointStart[1], pointEnd[1]], look, color=color)
    q.insert(-1, q1)


def onRelease(event):
    for i in range(len(q)):
        q[i].remove();
    q = []


def getPolygon(p):
    points = []
    for i in range(-1, len(p)):
        points.insert(-1, (p[i][0], p[i][1]))
    return sympyPolygon(*points)


fig.canvas.mpl_connect('button_release_event', onRelease)
size_x = MAX_X - MIN_X - 1
if size_x < 0:
    raise Exception('MAX_X must be more than MIN_X')
size_y = MAX_Y - MIN_Y - 1
if size_y < 0:
    raise Exception('MAX_Y must be moer than MIN_Y')
p1 = generateFigure(MIN_X + size_x / 2, MIN_Y + size_y / 2, min(size_x, size_y) / 2.5, 0.35, 0.2, COL_POINTS_FIRST)
p2 = generateFigure(MIN_X + size_x / 2, MIN_Y + size_y / 2, min(size_x, size_y) / 2.5, 0.35, 0.2, COL_POINTS_SECOND)
redrawClosest(p1, 'blue', '-', '.')
redrawClosest(p2, 'green', '-', '.')

p1 = getPolygon(p1)
p2 = getPolygon(p2)

p3 = p1.intersection(p2)
# x, y = p3.exterior.coords.xy

s = Segment(Point2D(0, 0), Point2D(0, 1))
p3Res = []
for x in p3:
    if type(x) is type(s.p1):
        p3Res.insert(-1, [x.x, x.y])
# ax1.add_patch(PolygonPatch(p3))
redrawClosest(p3Res, 'grey', '.', 'o')
ax1.set_xlim(MIN_X - 1, MAX_X + 1)
ax1.set_ylim(MIN_Y - 1, MAX_X + 1)

# display(fig) todo
plt.close()

# ____________________________________________________________________________________________________________________________

import math, random
import matplotlib.pyplot as plt
import numpy as np
from shapely.geometry.polygon import Polygon
from shapely.geometry import Point
from descartes import PolygonPatch

from ipywidgets import interact
from IPython.display import display

MAX_X = 20
MIN_X = 0
MAX_Y = 20
MIN_Y = 0
COL_POINTS_FIRST = 20
COL_POINTS_SECOND = 20


def generateFigure(ctrX, ctrY, aveRadius, irregularity, spikeyness, numVerts):
    irregularity = clip(irregularity, 0, 1) * 2 * math.pi / numVerts
    spikeyness = clip(spikeyness, 0, 1) * aveRadius

    # generate n angle steps
    angleSteps = []
    lower = (2 * math.pi / numVerts) - irregularity
    upper = (2 * math.pi / numVerts) + irregularity
    sum = 0
    for i in range(numVerts):
        tmp = random.uniform(lower, upper)
        angleSteps.append(tmp)
        sum = sum + tmp

    # normalize the steps so that point 0 and point n+1 are the same
    k = sum / (2 * math.pi)
    for i in range(numVerts):
        angleSteps[i] = angleSteps[i] / k

    # now generate the points
    points = []
    angle = random.uniform(0, 2 * math.pi)
    for i in range(numVerts):
        r_i = clip(random.gauss(aveRadius, spikeyness), 0, 2 * aveRadius)
        x = ctrX + r_i * math.cos(angle)
        y = ctrY + r_i * math.sin(angle)
        points.append((int(x), int(y)))

        angle = angle + angleSteps[i]

    return points


def clip(x, min, max):
    if (min > max):
        return x
    elif (x < min):
        return min
    elif (x > max):
        return max
    else:
        return x


fig = plt.figure(figsize=(6, 6))
ax1 = plt.subplot(111, aspect='equal')

q = []


def redrawClosest(point, color='black', look='--'):
    points = np.array(point)
    for i in range(len(points)):
        drawPoint(point[i], color)
        drawLine(point[i - 1], point[i], color, look)


def drawPoint(point, color='red', look='.'):
    q1, = ax1.plot(point[0], point[1], look, color=color)
    q.insert(-1, q1)


def drawLine(pointStart, pointEnd, color='red', look='-'):
    q1, = ax1.plot([pointStart[0], pointEnd[0]], [pointStart[1], pointEnd[1]], look, color=color)
    q.insert(-1, q1)


def onRelease(event):
    for i in range(len(q)):
        q[i].remove();
    q = []


def getPolygon(p):
    points = []
    for i in range(-1, len(p)):
        points.insert(-1, (p[i][0], p[i][1]))
    return Polygon(points)


fig.canvas.mpl_connect('button_release_event', onRelease)
size_x = MAX_X - MIN_X - 1
if size_x < 0:
    raise Exception('MAX_X must be more than MIN_X')
size_y = MAX_Y - MIN_Y - 1
if size_y < 0:
    raise Exception('MAX_Y must be moer than MIN_Y')
p1 = generateFigure(MIN_X + size_x / 2, MIN_Y + size_y / 2, min(size_x, size_y) / 2.5, 0.35, 0.2, COL_POINTS_FIRST)
p2 = generateFigure(MIN_X + size_x / 2, MIN_Y + size_y / 2, min(size_x, size_y) / 2.5, 0.35, 0.2, COL_POINTS_SECOND)
redrawClosest(p1, 'black', '-')
redrawClosest(p2, 'red', '-')

p1 = getPolygon(p1)
p2 = getPolygon(p2)

p3 = p1.intersection(p2)
x, y = p3.exterior.coords.xy
pRes3 = list([x[i], y[i]] for i in range(1, len(x)))
ax1.add_patch(PolygonPatch(p3))

ax1.set_xlim(MIN_X - 1, MAX_X + 1)
ax1.set_ylim(MIN_Y - 1, MAX_X + 1)
print("result={}".format(p3))
display(fig)
plt.close()
