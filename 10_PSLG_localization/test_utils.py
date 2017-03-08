import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import PatchCollection
from matplotlib.patches import Polygon


def turn(a, b, c):
    x1 = b[0] - a[0]
    y1 = b[1] - a[1]
    x2 = c[0] - a[0]
    y2 = c[1] - a[1]
    temp = x1 * y2 - x2 * y1
    if temp < 0:
        return -1
    elif temp > 0:
        return 1
    else:
        return 0


class Slab:
    def __init__(self, edges: list):
        self.iter = None
        self.edges = edges
        self.edges.sort()
        # self.fig, self.ax = plt.subplots()

    @staticmethod
    def read_slab(file):
        fin = open(file, "r")
        edges = list()
        for line in fin:
            x1, y1, x2, y2 = map(int, line.rstrip().split())
            edges.append([[x1, y1], [x2, y2]])
        fin.close()
        return Slab(edges)

    def convert(self):
        result = list()
        for segment in self.edges:
            x1, y1 = segment[0]
            x2, y2 = segment[1]
            result.append(([x1, x2], [y1, y2]))
        return result

    def draw(self, location=None, point=None):
        segments = self.convert()
        for i in range(len(segments)):
            x, y = segments[i]
            if location is not None and i in location:
                plt.plot(x, y, 'k-', color='red', linewidth=3)
            else:
                plt.plot(x, y, 'k-', color='black')

        if point is not None:
            plt.plot(point[0], point[1], 'o')
        
        plt.margins(0.1)
        plt.show()


def convert_edge(edge):
    x1, y1 = edge[0]
    x2, y2 = edge[1]
    return ([x1, x2], [y1, y2])


def correct_comparator(a, b):
    if turn(a[0], a[1], b[0]) * turn(a[0], a[1], b[1]) == 1:
        if turn(a[0], a[1], b[0]) < 0:
            return True
        else:
            return False
    else:
        return not correct_comparator(b, a)



def test_comparator(comp):
    edges = [
    [(0, 0), (1, 0)],
    [(0, 1), (1, 1)],
    [(0, 0), (1, 0)],
    [(0, 0), (1, 1)],
    [(0, 0), (1, 0)],
    [(0, 1), (1, 0)],
    [(0, 0), (1, 0)],
    [(-4, 1), (8, 9)],
    [(-5, -1), (1, 9)],
    [(0, 0), (1, 0)],
    [(0, 0), (1, 0)],
    [(0, 9), (4, -1)]
    ]
    
    for i in range(0, len(edges), 2):
        print("Running test #", (i // 2) + 1)
        if comp(edges[i], edges[i + 1]) != correct_comparator(edges[i], edges[i + 1]):
            print("Failure")
            return
        print("Passed")
        
    print("Passed all tests")
