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
        self.fig, self.ax = plt.subplots()

    @staticmethod
    def read_slab(file):
        fin = open(file, "r")
        edges = list()
        for line in fin:
            x1, y1, x2, y2 = map(int, line.rstrip().split())
            edges.append([[x1, y1], [x2, y2]])
        fin.close()
        return Slab(edges)

    def __convert(self):
        result = list()
        for segment in self.edges:
            x1, y1 = segment[0]
            x2, y2 = segment[1]
            result.append(([x1, x2], [y1, y2]))
        return result

    def draw(self, indices=None, point=None):
        if indices is not None:
            i, j = indices
            if i == -1:
                down = [[self.edges[j][0][0], self.edges[j][1] - 1], [self.edges[j][1][0], self.edges[j][1][1] - 1]]
            else:
                down = self.edges[i]
            if j == len(self.edges):
                up = [[self.edges[i][0][0], self.edges[i][1] + 1], [self.edges[i][1][0], self.edges[i][1][1] + 1]]
            else:
                up = self.edges[j]
            a = np.array([down[0], down[1], up[1], up[0]])
            polygon = Polygon(a)
            colors = plt.cm.colors.hex2color("#FF0000")
            p = PatchCollection([polygon])
            self.ax.add_collection(p)
            p.set_color(colors)
            self.ax.autoscale_view()
        if point is not None:
            plt.plot(point[0], point[1], 'o')

        segments = self.__convert()
        for x, y in segments:
            plt.plot(x, y, 'k-')
        plt.margins(0.1)
        plt.show()

    def redraw(self, indices=None, point=None):
        self.fig.clf()
        self.fig, self.ax = plt.subplots()
        cib = self.fig.canvas.mpl_connect('button_release_event', on_click)
        if indices is not None:
            i, j = indices
            if i == -1:
                down = [[self.edges[j][0][0], self.edges[j][1] - 1], [self.edges[j][1][0], self.edges[j][1][1] - 1]]
            else:
                down = self.edges[i]
            if j == len(self.edges):
                up = [[self.edges[i][0][0], self.edges[i][1] + 1], [self.edges[i][1][0], self.edges[i][1][1] + 1]]
            else:
                up = self.edges[j]
            a = np.array([down[0], down[1], up[1], up[0]])
            polygon = Polygon(a)
            colors = plt.cm.colors.hex2color("#FF0000")
            p = PatchCollection([polygon])
            p.set_color(colors)
            self.ax.add_collection(p)
            self.ax.autoscale_view()
        if point is not None:
            plt.plot(point[0], point[1], 'o')

        segments = self.__convert()
        for x, y in segments:
            plt.plot(x, y, 'k-')
        plt.margins(0.1)
        plt.show()
		return cib


slab1 = Slab.read_slab("sample01.txt")
print(slab1.iter)

# TODO: make it interactive
# TODO: generate a good test case
# def on_click(event):
#    print("click", event.xdata, event.ydata)
#    slab.redraw([0, 1], [event.xdata, event.ydata])


#slab.fig.canvas.mpl_connect('button_release_event', on_click)
#slab.draw()
