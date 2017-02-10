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
    ax1.clear() 
    printStep(points, 0, step, 0, 20, 0, 20)
    p = np.array(points)
    ax1.plot(p[:, 0], p[:, 1], 'o', color='red')
    ax1.set_xlim(0, 20)
    ax1.set_ylim(0, 20)
    display(fig)
    return

def generatePoints(n, N):
    points = {(randint(0, n), randint(0, n)) for i in range(N)}
    while len(points) < N:
        points |= {(randint(0, n), randint(0, n))}
    return list(list(x) for x in points)

points = generatePoints(20, 20)

def printStep(points, i, stepsLeft, left, right, floor, ceil):
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

    if (stepsLeft == 0):
        col = 'r'
    else:
        col = 'k'
            
    if (len(A) + len(B) >= 2):
        if (i == 0):
            ax1.plot([mean, mean], [floor, ceil], color=col, linestyle='-', linewidth=1)
        else:
            ax1.plot([left, right], [mean, mean], color=col, linestyle='-', linewidth=1)
            
    if (len(A) <= 1 and len(B) <= 1):
        return 1
    else: 
        if (i == 0):
            printStep(A, (i + 1) % 2, stepsLeft - 1, left, mean, floor, ceil)
            printStep(B, (i + 1) % 2, stepsLeft - 1, mean, right, floor, ceil)
        else:
            printStep(A, (i + 1) % 2, stepsLeft - 1, left, right, floor, mean)
            printStep(B, (i + 1) % 2, stepsLeft - 1, left, right, mean, ceil)
                
def visualize():
    global points, fig, ax1 
    steps = countSteps(points, 0) 
    p = np.array(points)
    ax1.plot(p[:, 0], p[:, 1], 'o', color='red')
    ax1.set_xlim(0, 20)
    ax1.set_ylim(0, 20)
    display(interactive(changeStep, step=(0, steps)))
