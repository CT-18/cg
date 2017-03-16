from random import randint
from scipy.spatial import Delaunay
import matplotlib.pyplot as plt
import numpy as np
from ipywidgets import interact, interactive, IntSlider
from IPython.display import display
from random import random

levels = None
currentLevel = None
fig = plt.figure(figsize=(6, 6))
ax1 = plt.subplot(111, aspect='equal')
q, = ax1.plot([10], [10], 'o', color='yellow')

def generatePoints(n, N):
    points = {(randint(0, n), randint(0, n)) for i in range(N)}
    while len(points) < N:
        points |= {(randint(0, n), randint(0, n))}
    return list(list(x) for x in points)

def createLevels(points, probability):
    def pushPoints(levels, probability):
        if (len(levels[-1]) == 1):
            return
        levels.append([])
        for p in levels[-2]:
            if (random() < probability):
                levels[-1] += [p]
        if len(levels[-1]) == 0:
            del levels[-1]
        elif len(levels[-1]) == len(levels[-2]):
            del levels[-1]
            pushPoints(levels, probability)
        else:
            pushPoints(levels, probability)

    levels = [[]]
    for p in points:
        levels[-1] += [tuple(p)]
    pushPoints(levels, probability)
    return levels

def redrawClosest(q, points, ax1):
    def nn(q, points):
        def dist(x):
            return (x[0] - q[0]) * (x[0] - q[0]) + (x[1] - q[1]) * (x[1] - q[1])
        return sorted(points, key=dist)[0]

    if redrawClosest.closestPoint is not None:
        redrawClosest.closestPoint.remove()
    closest = nn((q.get_xdata()[0], q.get_ydata()[0]), points)
    redrawClosest.closestPoint, = ax1.plot([closest[0]], [closest[1]], 'o', color='blue')
redrawClosest.closestPoint = None

def printLevel(fig, ax1, q, levels, i, isBackground = False, redraw = True):
    global currentLevel
    currentLevel = i
    
    if printLevel.prevEdges is not None:
        for x in printLevel.prevEdges:
            x.remove()
        printLevel.prevEdges = None
    if printLevel.prevPoints is not None:
        printLevel.prevPoints.remove()
            
    color = 'grey' if isBackground else 'red'
    
    points = np.array(levels[i])
    if (len(points) == 3):
        printLevel.prevEdges = ax1.triplot(points[:, 0], points[:, 1], np.array([[0, 1, 2]]), color=color)
    if (len(points) >= 4):
        tri = Delaunay(points)
        printLevel.prevEdges = ax1.triplot(points[:, 0], points[:, 1], tri.simplices.copy(), color=color)
    printLevel.prevPoints, = ax1.plot(points[:, 0], points[:, 1], 'o', color=color)
    if isBackground:
        printLevel.prevPoints = printLevel.prevEdges = None
        
    redrawClosest(q, points, ax1)
    
    if redraw:
        display(fig)
    ax1.set_xlim(0, 20)
    ax1.set_ylim(0, 20)
printLevel.prevPoints = printLevel.prevEdges = None

def onRelease(event):
    global q, currentLevel, levels, ax1
    if q is not None:
        q.remove()
    q, = ax1.plot([event.xdata], [event.ydata], 'o', color='yellow')
    points = np.array(levels[currentLevel])
    redrawClosest(q, points, ax1)
    display(fig)

def changeLevel(уровень = 0):
    if changeLevel.suspend:
        return
    printLevel(fig, ax1, q, levels, уровень)
changeLevel.suspend = True

def visualize():
    global currentLevel, levels, fig, ax1, q
    changeLevel.suspend = True
    fig.canvas.mpl_connect('button_release_event', onRelease)
    
    redrawClosest.closestPoint = None
    printLevel.prevEdges = None
    printLevel.prevPoints = None
    ax1.clear()
	
    q, = ax1.plot([10], [10], 'o', color='yellow')
    
    points = generatePoints(20, 20)
    levels = createLevels(points, .4)
    printLevel(fig, ax1, q, levels, 0, True) # printing gray imprint
    
    #ax1.text(2, 2, len(levels))
    
    changeLevel.suspend = False
    display(interactive(changeLevel, уровень=(0, len(levels) - 1)))
    printLevel(fig, ax1, q, levels, 0, redraw = False)