from random import randint
from scipy.spatial import Delaunay
import matplotlib.pyplot as plt
import numpy as np
from ipywidgets import interact, interactive, IntSlider
from IPython.display import display
from random import random

fig = plt.figure(figsize=(6, 6))
ax1 = plt.subplot(111, aspect='equal')

def countSteps(points, i):
    if (len(points) == 0):
        return 0;
    p = np.array(points)
    mean = np.mean(p[:, i])
    
    A = list()
    B = list()

    for p in points:
        if (p[i] < mean):
            A.append(p)
        else:
            B.append(p)

    #print(A, mean, B, i)

    if (len(A) <= 1 and len(B) <= 1):
        return 1
    else: 
        return max(countSteps(A, (i + 1) % 2), countSteps(B, (i + 1) % 2)) + 1;


def changeStep(step = 0):
    #ax1.clear() 
    return

def generatePoints(n, N):
    points = {(randint(0, n), randint(0, n)) for i in range(N)}
    while len(points) < N:
        points |= {(randint(0, n), randint(0, n))}
    return list(list(x) for x in points)

points = generatePoints(20, 20)

def printStep(points, i, stepsLeft):
    if (len(points) == 0 or stepsLeft == -1):
        return;
    p = np.array(points)
    mean = np.mean(p[:, i])
   
    A = list()
    B = list()

    for p in points:
        if (p[i] < mean):
            A.append(p)
        else:
            B.append(p)

    #print(A, mean, B, i)

    if (len(A) <= 1 and len(B) <= 1):
        return 1
    else: 
        PrintStep(A, (i + 1) % 2, step - 1)
        PrintStep(B, (i + 1) % 2, step - 1)

def visualize():
    global points, fig, ax1 
    steps = countSteps(points, 0) 
    p = np.array(points)
    ax1.plot(p[:, 0], p[:, 1], 'o', color='red')
    display(interactive(changeStep, step=(0, steps)))
    

