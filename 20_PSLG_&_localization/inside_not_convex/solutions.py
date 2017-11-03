import numpy as np
from shapely.geometry.polygon import Polygon
from shapely.geometry import Point
import math, random
from sympy import Ray as sRay, Segment as sSegment
from sympy import Point as sPoint
from sympy import intersection
import matplotlib.pyplot as plt
from IPython.display import display


def turn(points, p):
    return np.sign(np.linalg.det(np.array(points) - p))


def check(points, point):
    p = Polygon(points)
    point = Point(point)
    return p.contains(point)


def generate_test(ctr_x, ctr_y, aveRadius, irregularity, spikeyness, numVerts):
    irregularity = clip(irregularity, 0, 1) * 2 * math.pi / numVerts
    spikeyness = clip(spikeyness, 0, 1) * aveRadius

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
        r_i = clip(random.gauss(aveRadius, spikeyness), 0, 2 * aveRadius)
        x = ctr_x + r_i * math.cos(angle)
        y = ctr_y + r_i * math.sin(angle)
        points.append((int(x), int(y)))
        angle = angle + angle_steps[i]

    return points


def clip(x, min, max):
    if min > max:
        return x
    elif x < min:
        return min
    elif x > max:
        return max
    else:
        return x


def intersect(ray, segment):
    ray = sRay(sPoint(*ray[0]), sPoint(*ray[1]))
    segment = sSegment(segment[0], segment[1])
    return len(intersection(ray, segment)) != 0


def draw(points, point, title):
    fig = plt.figure(figsize=(6, 6))
    ax1 = plt.subplot(111, aspect='equal')
    ax1.plot(point[0], point[1], 'o', color='g')
    points.insert(len(points), [points[0][0], points[0][1]])
    points_t = np.array(points).T
    ax1.plot(points_t[0,], points_t[1,], '--', c='r')
    ax1.scatter(points_t[0,], points_t[1,], c='r')
    ax1.set_xlim(0 - 1, 30 + 1)
    ax1.set_ylim(0 - 1, 30 + 1)
    if title != "":
        ax1.set_title(title)
    display(fig)
    plt.close()


def test(f, n=200):
    for i in range(0, n):
        points = generate_test(15, 15, 10, 0.35, 0.35, 30)
        if i % 50 == 0 and i != 0:
            print('passed {} tests'.format(i))
        for j in range(0, 200):
            point = np.random.randint(0, 25, size=(2))
            answer = check(points, point)
            result = f(points, point)
            if result is answer:
                continue
            print("Test №{} failed".format(i + 1))
            print("Expected {}, result {}".format(answer, result))
            print("points={}".format(points))
            print("point={}".format(point))
            draw(points, point, "")
            return
    print("All tests passed")


def show_test(test, f):
    res = f(test[0], test[1])
    draw(test[0], test[1], "inside" if res else "outside")


def draw_segment(ax, segment, color):
    segment = np.array(segment).T
    ax.plot(segment[0,], segment[1,], c=color)
    ax.scatter(segment[0,], segment[1,], c=color)


def draw_ray(ax, ray, maxX, color):
    a = ray[0][1] - ray[1][1]
    b = ray[1][0] - ray[0][0]
    c = ray[0][0] * ray[1][1] - ray[1][0] * ray[0][1]
    y = (-c - a * maxX) / b
    ray[1] = [maxX, y]
    draw_segment(ax, ray, color)


def test_intersect(f, n=200):
    for i in range(1, n):
        if i % 50 == 0:
            print('passed {} tests'.format(i))
        ray = np.random.randint(0, 25, size=(2, 2))
        segment = np.random.randint(0, 25, size=(2, 2))
        answer = intersect(ray, segment)
        result = f(ray, segment)
        if f(ray, segment) is intersect(ray, segment):
            continue
        fig = plt.figure(figsize=(6, 6))
        ax1 = plt.subplot(111, aspect='equal')
        draw_ray(ax1, ray, 27, 'r')
        draw_segment(ax1, segment, 'g')
        ax1.set_xlim(0 - 1, 25 + 1)
        ax1.set_ylim(0 - 1, 25 + 1)
        ax1.set_title("expected {}, result {}".format(answer, result))
        display(fig)
        plt.close()
        return
    print("All tests passed")


def test_turn(f, n=200):
    for i in range(1, n):
        if i % 50 == 0:
            print('passed {} tests'.format(i))
        while True:
            points = np.random.randint(0, 25, size=(2, 2))
            point = np.random.randint(0, 25, size=(1, 2))
            if points[0] is points[1]:
                continue
            break
        answer = f(points, point)
        result = turn(points, point)
        if int(answer) == int(result):
            continue
        print("Test №{} failed".format(i + 1))
        print("Expected {}, result {}".format(answer, result))
        print("points={}".format(points))
        print("point={}".format(point))
    print("All tests passed")


def show_examples(tests, f):
    lines = len(tests) // 3 + (1 if len(tests) % 3 != 0 else 0)
    fig, axes = plt.subplots(lines, 3, figsize=(9, 3 * lines))

    while lines * 3 != len(tests):
        tests.insert(len(tests), [[-5, -5], [-5, -5], [-5, -5], [-5, -5]])

    for (a, b, c, d), axis in zip(tests, axes.reshape(len(tests))):
        if a[0] == a[1] == b[0] == b[1] == c[0] == c[1] == d[0] == d[1] == -5:
            continue
        draw_ray(axis, [a, b], 4, 'r')
        draw_segment(axis, [c, d], 'g')
        axis.set_xlim(-1, 3)
        axis.set_ylim(-1, 3)
        ray = [a, b]
        segment = [c, d]
        if f(ray, segment):
            title = "intersect"
        else:
            title = "not intersect"

        axis.set_title(title)
    plt.show()
    plt.close()
