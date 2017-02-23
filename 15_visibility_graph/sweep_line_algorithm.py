from random import randint
import matplotlib.pyplot as plt
import numpy as np
from ipywidgets import interact, interactive, IntSlider
from IPython.display import display
from random import random
from matplotlib.path import Path
import matplotlib.patches as patches
from scipy.spatial import ConvexHull


def sweep_task(solution):

    def generatePoints(x1, x2, y1, y2, N):
        points = {(randint(x1, x2), randint(y1, y2)) for i in range(N)}
        while len(points) < N:
            points |= {(randint(x1, x2), randint(y1, y2))}
        return list(list(x) for x in points)

    polygon = generatePoints(20, 40, 0, 20, 7)
    hull = ConvexHull(polygon)
    polygon_np = np.array(polygon)

    point = [10, 10]

    fig = plt.figure(figsize=(6, 6))
    ax1 = plt.subplot(111, aspect='equal')
    ax1.set_xlim(-5,45)
    ax1.set_ylim(-5,25)

    ax1.plot(point[0], point[1], 'ro');

    points = []
    polygon_hul = []

    for simplex in hull.simplices:
        ax1.plot(polygon_np[simplex, 0], polygon_np[simplex, 1], 'k-')
    for v in hull.vertices:
        polygon_hul.append(polygon[v])

    ans = solution(point, polygon)

    print(ans)

    for v in ans:
        p1 = v[0]
        p2 = v[1]
        ax1.plot([p1[0], p2[0]], [p1[1], p2[1]], color='r', linestyle='-', linewidth=1)

    display(fig)

    ans1 = naive_algorithm(point, polygon)

    ans.sort()
    ans1.sort()

    if ans1 == ans:
        print("Accepted")
    else:
        print("WA 1")

def naive_algorithm(point, polygon):

    points = list(polygon)
    points += point

    def area(a, b, c):
        return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])

    def intersect1(x1, y1, x2, y2):
        if x1 > y1:
            x1, y1 = y1, x1
        if x2 > y2:
            x2, y2 = y2, x2
        return max(x1, x2) <= min(y1, y2)

    def intersect_line(a, b, c, d):
        return (intersect1(a[0], b[0], c[0], d[0])
            and intersect1(a[1], b[1], c[1], d[1])
            and area(a, b, c) * area(a, b, d) <= 0
            and area(c, d, a) * area(c, d, b) <= 0)

    ans = []

    for p2 in polygon: 
        t1 = list(point)
        t2 = list(p2)
        t2[0] -= 0.00001
        intersect = False

        for i in range(len(polygon) - 1):
            if intersect_line(t1, t2, polygon[i], polygon[i + 1]):
                intersect = True
        if intersect_line(t1, t2, polygon[-1], polygon[0]):
            intersect = True

        if not intersect:
            ans.append([t1, t2])

    return ans
