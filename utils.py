import matplotlib.pyplot as plt
import numpy as np
import functools as fc

TURN_LEFT, TURN_RIGHT, TURN_NONE = (1, -1, 0)

def cmp(a, b):
    return (a > b) - (a < b)

def turn(p, q, r):
    #предикат поворота, возвращает 1, -1, 0, если точки p, q, r  образуют левый, правый повороты 
    #или лежат на одной прямой, соответственно.
    return cmp((q[0] - p[0])*(r[1] - p[1]) - (r[0] - p[0])*(q[1] - p[1]), 0)

def dist(q, p):
    #считаем расстояние 
    dx, dy = q[0] - p[0], q[1] - p[1]
    return dx * dx + dy * dy

def plot_melkman(points, ans):
	xs = [x[0] for x in points]
	ys = [y[1] for y in points]
	plt.plot(xs, ys, 'o-', color='black', linewidth=2)

	x = [x[0] for x in ans]
	y = [x[1] for x in ans]
	plt.plot(x, y, 'k-', color='#00ff00', linewidth=3)
	plt.plot(x, y, 'o', color='red', markersize=8)
	plt.axis([0, 15, -1, 10])
	plt.show()
