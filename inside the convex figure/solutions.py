import numpy as np
from sympy import convex_hull
from shapely.geometry.polygon import Polygon
from shapely.geometry import Point
import matplotlib.pyplot as plt
from IPython.display import display

def orientation(points, p):
    """Возвращает ориентацию точки p относительно точек points (0, 1 или -1)."""
    return np.sign(np.linalg.det(np.array(points) - p))

def generateTest():
    randpoints = np.random.randint(0,25,size=(30,2))
    hull = convex_hull(*randpoints)
    points=[]
    for point in hull.vertices:
        points.insert(len(points),[point.x,point.y])
    return points

def check(points,point): 
    p = Polygon(points)
    point = Point(point)
    return p.contains(Point(point))


def draw(points,point):
    fig = plt.figure(figsize = (6, 6))
    ax1 = plt.subplot(111, aspect = 'equal')
    ax1.plot(point[0], point[1], 'o', color = 'g')
    points.insert(len(points), [points[0][0], points[0][1]])
    points_t = np.array(points).T
    ax1.plot(points_t[0,], points_t[1,], '--', c='r')
    ax1.scatter(points_t[0,], points_t[1,], c='r')
    ax1.plot(points[0][0], points[0][1], '.', color='b')
    ax1.set_xlim(0 - 1, 25 + 1)
    ax1.set_ylim(0 - 1, 25 + 1)
    display(fig)
    plt.close()
    
def test(f, n = 200):
    for i in range(0,n):
        points = generateTest()
        if i % 50 == 0 and i != 0:
            print('passed {} tests'.format(i))
        for j in range(0, 2*len(points)):
            point = np.random.randint(0, 25, size = (2))
            answer = check(points, point)
            for k in range(0, len(points) - 1):
                points.insert(len(points), points[0])
                points.remove(points[0])
                result = f(points, point)
                if(result is answer):
                    continue
                print("Test №{} failed".format(i + 1))
                print("Expected {}, result {}".format(answer, result))
                print("points={}".format(points))
                print("point={}".format(point))
                draw(points, point)
                return
    print("All tests ok")
    