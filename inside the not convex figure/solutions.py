import numpy as np
from shapely.geometry.polygon import Polygon
from shapely.geometry import Point
import math, random
from sympy import Ray as sRay, Segment as sSegment
from sympy import Point as sPoint, Polygon as sPolygon
from sympy import intersection
from random import randint
import matplotlib.pyplot as plt
from IPython.display import display

def orientation(points, p):
    """Возвращает ориентацию точки p относительно точек points (0, 1 или -1)."""
    return np.sign(np.linalg.det(np.array(points) - p))

def check(points, point): 
    p=Polygon(points)
    point=Point(point)
    return p.contains(point)


def generateTest(ctrX, ctrY, aveRadius, irregularity, spikeyness, numVerts):
    irregularity = clip( irregularity, 0,1 ) * 2*math.pi / numVerts
    spikeyness = clip( spikeyness, 0,1 ) * aveRadius

    # generate n angle steps
    angleSteps = []
    lower = (2 * math.pi / numVerts) - irregularity
    upper = (2 * math.pi / numVerts) + irregularity
    sum = 0
    for i in range(numVerts) :
        tmp = random.uniform(lower, upper)
        angleSteps.append( tmp )
        sum = sum + tmp

    # normalize the steps so that point 0 and point n+1 are the same
    k = sum / (2 * math.pi)
    for i in range(numVerts) :
        angleSteps[i] = angleSteps[i] / k

    # now generate the points
    points = []
    angle = random.uniform(0, 2*math.pi)
    for i in range(numVerts) :
        r_i = clip( random.gauss(aveRadius, spikeyness), 0, 2*aveRadius )
        x = ctrX + r_i*math.cos(angle)
        y = ctrY + r_i*math.sin(angle)
        points.append( (int(x),int(y)) )
        angle = angle + angleSteps[i]

    return points

def clip(x, min, max) :
    if( min > max ) :  return x    
    elif( x < min ) :  return min
    elif( x > max ) :  return max
    else :             return x
    
def intersect(ray, segment):
    ray = sRay(sPoint(*ray[0]),sPoint(*ray[1]))
    segment = sSegment(segment[0],segment[1])
    return len(intersection(ray,segment)) != 0
    
def isBetween(point1, point2, point):
    x1 = min(point1[0], point2[0])
    x2 = max(point1[0], point2[0])
    y1 = min(point1[1], point2[1])
    y2 = max(point1[1], point2[1])
    return x1 <= point[0] and point[0] <= x2 and y1 <= point[1] and y2 <= point[1]

def isOnSegment(point,segment):
    s = sSegment(segment[0],segment[1])
    p = sPoint(*point)
    return len(intersection(s,p)) != 0
    
def draw(points,point):
    fig = plt.figure(figsize = (6, 6))
    ax1 = plt.subplot(111, aspect = 'equal')
    ax1.plot(point[0], point[1], 'o', color = 'g')
    points.insert(len(points), [points[0][0], points[0][1]])
    points_t = np.array(points).T
    ax1.plot(points_t[0,], points_t[1,], '--', c='r')
    ax1.scatter(points_t[0,], points_t[1,], c='r')
    ax1.set_xlim(0 - 1, 25 + 1)
    ax1.set_ylim(0 - 1, 25 + 1)
    display(fig)
    plt.close()
    
def test(f, n = 200):
    for i in range(0,n):
        points = generateTest(10, 10, 7, 0.35, 0.2, 30)
        if i % 50 == 0 and i != 0:
            print('passed {} tests'.format(i))
        for j in range(0, 200):
            point = np.random.randint(0, 25, size = (2))
            answer = check(points, point)
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
    
    
    