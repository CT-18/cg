import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
from matplotlib.patches import Polygon
from cg import Point, turn


def my_turn(a, b, c):
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
            edges.append([Point(x1, y1), Point(x2, y2)])
        fin.close()
        return Slab(edges)

    def convert(self):
        result = list()
        for segment in self.edges:
            x1, y1 = segment[0].coord[0], segment[0].coord[1]
            x2, y2 = segment[1].coord[0], segment[1].coord[1]
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
            plt.plot(point.coord[0], point.coord[1], 'o')
        
        plt.margins(0.1)
        plt.show()


def convert_edge(edge):
    x1, y1 = edge[0]
    x2, y2 = edge[1]
    return ([x1, x2], [y1, y2])


def correct_comparator(a, b):
    first = turn(a[0], a[1], b[0])
    second = turn(a[0], a[1], b[1])
    if first * second == 1:
        if turn(a[0], a[1], b[0]) < 0:
            return True
        else:
            return False
    elif first * second == 0:
        if first < 0 or second < 0:
            return True
        else:
            return False
    else:
        return not correct_comparator(b, a)



def test_comparator(comp):
    edges = [
    [Point(0, 0), Point(1, 0)],
    [Point(0, 1), Point(1, 1)],
    [Point(0, 0), Point(1, 0)],
    [Point(0, 0), Point(1, 1)],
    [Point(0, 0), Point(1, 0)],
    [Point(0, 1), Point(1, 0)],
    [Point(0, 0), Point(1, 0)],
    [Point(-4, 1), Point(8, 9)],
    [Point(-5, -1), Point(1, 9)],
    [Point(0, 0), Point(1, 0)],
    [Point(0, 0), Point(1, 0)],
    [Point(0, 9), Point(4, -1)]
    ]
    
    for i in range(0, len(edges), 2):
        print("Running test #", (i // 2) + 1)
        if comp(edges[i], edges[i + 1]) != correct_comparator(edges[i], edges[i + 1]):
            print("Failure")
            return
        print("Passed")
        
    print("Passed all tests")
    
class Vertex:

    def __init__(self):
        self.version = None
        self.left = None
        self.right = None
        self.next = None
        self.edge = None
        self.is_left = None


class Slabs:

    def __init__(self, xx, yy, edges, vertices, roots):
        self.xx = xx
        self.yy = yy
        self.edges = edges
        self.vertices = vertices
        self.roots = roots

    @staticmethod
    def read_slabs(path):
        fin = open(path, 'r')
        xx = [e for e in map(int, fin.readline().rstrip().split())]
        yy = [e for e in map(int, fin.readline().rstrip().split())]
        n = int(fin.readline().rstrip())
        edges = list()
        for i in range(n):
            x1, y1, x2, y2 = map(int, fin.readline().rstrip().split())
            edges.append([Point(x1, y1), Point(x2, y2)])
        n = int(fin.readline().rstrip())
        vertices = [Vertex() for i in range(n)]
        for i in range(n):
            edge, left, right, next2, direction, version = fin.readline().rstrip().split()
            edge, left, right, next2, version = int(edge), int(left), int(right), int(next2), int(version)
            vertices[i].version = version
            vertices[i].edge = edges[edge - 1]
            if left != -1:
                vertices[i].left = vertices[left]
            if right != -1:
                vertices[i].right = vertices[right]
            if next2 != -1:
                vertices[i].next = vertices[next2]
                vertices[i].is_left = direction == 'l'

        roots = [vertices[e] if e != -1 else None for e in map(int, fin.readline().rstrip().split())]
        fin.close()
        return Slabs(xx, yy, edges, vertices, roots)

    
    def convert(self):
        result = list()
        for segment in self.edges:
            x1, y1 = segment[0].coord[0], segment[0].coord[1]
            x2, y2 = segment[1].coord[0], segment[1].coord[1]
            result.append(([x1, x2], [y1, y2]))
        return result

    def draw(self, location=None, point=None):
        segments = self.convert()
        for i in range(len(segments)):
            x, y = segments[i]
            plt.plot(x, y, 'k-', color='black')

        if point is not None:
            plt.plot(point.coord[0], point.coord[1], 'o')
            
        if location is not None:
            x1, y1 = location[0].coord[0], location[0].coord[1]
            x2, y2 = location[1].coord[0], location[1].coord[1]
            plt.plot([x1, x2], [y1, y2], 'k-', color='red', linewidth=3)

        for x in self.xx:
            plt.plot([x, x], self.yy, 'r--')

        plt.margins(0.1)
        plt.show()
