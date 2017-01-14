import numpy as np
from sympy import convex_hull
from shapely.geometry.polygon import Polygon
from shapely.geometry import Point

def orientation(points, p):
    """Возвращает ориентацию точки p относительно точек points (0, 1 или -1)."""
    return np.sign(np.linalg.det(np.array(points) - p))

def generateTest():
    randpoints=np.random.randint(0,20,size=(30,2))
    hull = convex_hull(*randpoints)
    points=[]
    for point in hull.vertices:
        points.insert(len(points),[point.x,point.y])
    return [points,np.random.randint(0,20,size=(2))]

def check(points,point): 
    p=Polygon(points)
    point=Point(point)
    return 'in' if p.contains(Point(point)) else 'out'
    