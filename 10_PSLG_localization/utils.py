import heapq
from enum import Enum
from sortedcontainers import SortedSet


class Segment:
    def __init__(self, a, b):
        self.origin = a
        self.destination = b
        if self.destination < self.origin:
            self.origin, self.destination = self.destination, self.origin

    def __lt__(self, other):
        if self.origin < other.origin:
            return True
        elif self.origin > other.origin:
            return False

        temp = turn(self.origin, self.destination, other.distination)

        if temp == -1:
            return True
        elif temp == 1:
            return False
        else:
            return self.destination < other.distination


class Event:

    class EventType(Enum):
        INSERT = 1
        DELETE = 2

    def __init__(self, point, segment: Segment, insert: EventType):
        self.x, self.y = point
        self.edge = segment
        self.insert = insert


class Node:

    __version = 0

    def __init__(self, data):
        self.left = None
        self.right = None
        self.version = Node.__version
        self.data = data

    @staticmethod
    def increase_version():
        Node.__version += 1

    def copy(self):
        result = Node(self.data)
        result.left = self.left
        result.right = self.right

