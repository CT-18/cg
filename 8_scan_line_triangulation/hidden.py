from enum import Enum

def point_comp(self, other):
    return self.coord[1] > other.coord[1] or (self.coord[1] == other.coord[1] and self.coord[0] < other.coord[0])

class VType(Enum):
    start = 1
    split = 2
    end = 3
    merge = 4
    regular = 5
    
class Hedge:
    """
    Класс half-edge - одностороннего ребра, которое используется в DCEL.
    """
    def __init__(self, v):
        self.origin = v
        self.twin = None
        self.next = None
        self.prev = None
        
    def __repr__(self):
        return '{}->{}'.format(self.origin, self.twin.origin)

def build_dcel(vert):
    dcel = []
    start = Hedge(vert[0])
    start.twin = Hedge(vert[1])
    start.twin.twin = start
    dcel.append(start)
    prev = start
    lis = vert[1:] + [vert[0]]
    for i in range(0, len(lis)-1):
        cur = Hedge(lis[i])
        lis[i].hedge = cur
        cur.twin = Hedge(lis[i+1])
        cur.twin.twin = cur
        cur.prev = prev
        prev.next = cur
        prev.twin.prev = cur.twin
        cur.twin.next = prev.twin
        prev = cur
        dcel.append(cur)
    cur.next = start
    start.prev = cur
    start.twin.next = cur.twin
    cur.twin.prev = start.twin
    vert[0].hedge = start
    return dcel

def add_diagonal(hfrom, hto):
    d = Hedge(hfrom.origin)
    d.twin = Hedge(hto.origin)
    """
    hfrom.prev.next = d
    d.prev = hfrom.prev
    hfrom.prev = d.twin
    d.twin.next = hfrom
    hto.prev.next = d.twin
    d.twin.prev = hto.prev
    hto.prev = d
    d.next = hto
    """
    return d

