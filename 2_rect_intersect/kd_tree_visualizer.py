from random import randint
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from ipywidgets import interact, interactive, IntSlider
from IPython.display import display
from random import random
from cg.utils import *

# подсчет глубины kd-дерева
def countSteps(points, axis):
    if (len(points) <= 2):
        return 1;
    
    sorted_points = points.sort(lambda first, second: first[axis] - second[axis], False)
    mean = len(points) // 2
    
    return max(countSteps(sorted_points[:mean], (axis + 1) % 2), countSteps(sorted_points[mean:], (axis + 1) % 2)) + 1;

# Визуализотор построения kd-дерева на заданных точках
def kd_tree_visualize_build(points):
    
    fig = plt.figure(figsize=(6, 6), num=' ')
    ax = plt.subplot(111, aspect='equal')
    ax.plot(points.points[:, 0], points.points[:, 1], 'o', color='red')
    max_point = points.max()
    min_point = points.max(lambda f,s : -cmp_(f, s))
    #ax.set_xlim(min_point[0], max_point[0])
    #ax.set_ylim(min_point[1], max_point[1])
    ax.set_xlim(0, 20)
    ax.set_ylim(0, 20)

    steps = countSteps(points, 0) 
    
    # Построение дерева до steps шагов, [left, right, floor, ceil] - текущая область, которую мы рассматриваем
    # i == 0 на этом шаге добавляем вертикальную прямую, иначе горизонтальную
    def printStep(points, axis, steps, left, right, floor, ceil):
        if (len(points) == 0 or steps == -1):
            return;
  
        sorted_points = points.sort(lambda first, second: first[axis] - second[axis], False)
        mean = len(points) // 2
        mean_val = sorted_points[mean][axis]
        
        if (steps == 0):
            col = 'r'
        else:
            col = 'k'
            
        if (len(points) >= 2):
            if (axis == 0):
                ax.plot([mean_val, mean_val], [floor, ceil], color=col, linestyle='-', linewidth=1)
            else:
                ax.plot([left, right], [mean_val, mean_val], color=col, linestyle='-', linewidth=1)
            
        if (len(points) <= 2):
            return 
        else: 
            if (axis == 0):
                printStep(sorted_points[:mean], (axis + 1) % 2, steps - 1, left, mean_val, floor, ceil)
                printStep(sorted_points[mean:], (axis + 1) % 2, steps - 1, mean_val, right, floor, ceil)
            else:
                printStep(sorted_points[:mean], (axis + 1) % 2, steps - 1, left, right, floor, mean_val)
                printStep(sorted_points[mean:], (axis + 1) % 2, steps - 1, left, right, mean_val, ceil)
    
    def changeStep(step = 0):
        ax.clear() 
        printStep(points, 0, step, 0, 20, 0, 20)
        ax.plot(points.points[:, 0], points.points[:, 1], 'o', color='red')
        ax.set_xlim(0, 20)
        ax.set_ylim(0, 20)
        #ax.set_xlim(min_point[0], max_point[0])
        #ax.set_ylim(min_point[1], max_point[1])
        display(fig)
        print(points)
        print(max_point)
        print(min_point)
    
    display(interactive(changeStep, step=(0, steps)))

def inside(box1, box2):
    if (box1[0] >= box2[0] and box1[0] <= box2[2] and 
        box1[2] >= box2[0] and box1[2] <= box2[2] and
        box1[1] >= box2[1] and box1[1] <= box2[3] and 
        box1[3] >= box2[1] and box1[3] <= box2[3]):
        return True
    else:
        return False

def inside_p(x, y, box):
    if (x >= box[0] and x <= box[2] and 
        y >= box[1] and y <= box[3]):
        return True
    else:
        return False
    
def intersect(a, b):
    if (a[3] < b[1] or a[1] > b[3] or a[2] < b[0] or a[0] > b[2]):
        return False
    return True
    
def kd_tree_search_visualize(box, points):
    fig1 = plt.figure(figsize=(6, 6), num='  ')
    ax1 = plt.subplot(111, aspect='equal')
    p = np.array(points)
    ax1.plot(p[:, 0], p[:, 1], 'o', color='red')
    ax1.set_xlim(0, 20)
    ax1.set_ylim(0, 20)
    ax1.add_patch(patches.Rectangle((box[0], box[1]), box[2] - box[0], box[3] - box[1], alpha=0.2))
    
    # Нода kd-дерева 
    class node:
        def __init__(self, points, box, i):
            self.points = points # точки находящиеся в области box
            self.box = box       # часть пространства соответствующая ноде
            self.left = None     # левый сын
            self.right = None    # правый сын 
                                 # если оба сына == None, то нода - лист и содержит только одну точку в points
            self.mean = None     # медиана points
            self.i = i           # если i == 0 то нода разделяет область по вертикали, иначе по горизонтали

        # запрос
        # возвращает массив точек содержащихся в box
        def search(self, box):
            if (inside(self.box, box)):
                ax1.add_patch(patches.Rectangle((self.box[0], self.box[1]), self.box[2] - self.box[0], self.box[3] - self.box[1], color='b', alpha=0.1))
                return self.points
            ans = []
            if (self.left == None and self.right == None):
                if (intersect(box, self.box)):
                    ax1.add_patch(patches.Rectangle((self.box[0], self.box[1]), self.box[2] - self.box[0], self.box[3] - self.box[1], color='b', alpha=0.1))
                for p in self.points:
                    if (inside_p(p[0], p[1], box)):
                        ans += p
            if (self.left != None):
                ans += self.left.search(box)
            if (self.right != None):
                ans += self.right.search(box)
            return ans
        
        # построение дерева
        def build(self):
            if (len(self.points) == 0):
                return;
        
            # ищем медиану точек и делим их на 2 части
            p = np.array(self.points)
            self.mean = np.mean(p[:, self.i])
            A = list()
            B = list()
            for p in self.points:
                if (p[self.i] < self.mean):
                    A.append(p)
                else:
                    B.append(p)
            # визуализация разделяющей прямой
            if (len(A) + len(B) >= 2):
                if (self.i == 0):
                    ax1.plot([self.mean, self.mean], [self.box[1], self.box[3]], color='k', linestyle='-', linewidth=1)
                else:
                    ax1.plot([self.box[0], self.box[2]], [self.mean, self.mean], color='k', linestyle='-', linewidth=1)
        
            # построение детей
            if (len(A) <= 1 and len(B) <= 1):
                return 1
            else: 
                if (self.i == 0):
                    self.left = node(A, [self.box[0], self.box[1], self.mean, self.box[3]], (self.i + 1) % 2)
                    self.left.build()
                    self.right = node(B, [self.mean, self.box[1], self.box[2], self.box[3]], (self.i + 1) % 2)
                    self.right.build()
                else:
                    self.left = node(A, [self.box[0], self.box[1], self.box[2], self.mean], (self.i + 1) % 2)
                    self.left.build()
                    self.right = node(B, [self.box[0], self.mean, self.box[2], self.box[3]], (self.i + 1) % 2)
                    self.right.build()
    
    # корень kd-дерева, содержит все точки и соответсвует всей плоскости, вервый разделитель - вертикальный
    root = node(points, [0, 0, 20, 20], 0)
    root.build()
    print (root.search(box))