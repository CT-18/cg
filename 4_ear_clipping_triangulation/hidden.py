from enum import Enum
from cg import Point


def turn(v1, v2, v3):
    return (v2.x - v1.x) * (v3.y - v1.y) - (v3.x - v1.x) * (v2.y - v1.y)

    
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

def add_diagonal2(hfrom, hto):
    d = Hedge(hfrom.origin)
    d.twin = Hedge(hto.origin)
    
    hfrom.prev.next = d
    d.prev = hfrom.prev
    hfrom.prev.twin.pred = d.twin
    d.twin.next = hfrom.prev.twin

    hto.prev = d
    d.next = hto
    d.twin.prev = hto.twin
    hto.twin.next = d.twin
    
    return d

def add_diagonal_with_next(hfrom, hto):
    d = Hedge(hfrom.origin)
    d.twin = Hedge(hto.origin)

    d.next = hto
    return d

def merge_polygons(outer_polygon, outer_h, inner_polygon, inner_h):
    outer_prev = outer_h.prev
    inner_prev = inner_h.prev

    def add_edge(from_h, to_h):
            # новое ребро
            tmp = Point(int(from_h.next.origin.x),int(from_h.next.origin.y))
            h = Hedge(tmp)
            tmp = Point(int(to_h.origin.x), int(to_h.origin.y))
            h.twin = Hedge(tmp)
            h.twin.twin = h

            # from -> new 
            from_h.next = h
            h.prev = from_h  
            from_h.twin.prev = h.twin
            h.twin.next = from_h.twin

            # new -> to
            h.next = to_h
            to_h.prev = h
            h.twin.prev = to_h.twin
            to_h.twin.prev = h.twin
            
            return h

    h1 = add_edge(outer_prev, inner_h)
    h2 = add_edge(inner_prev, outer_h)

    outer_polygon.append(h1)
    outer_polygon.append(h2)
    for hedge in inner_polygon:
        outer_polygon.append(hedge)
    inner_polygon.clear()

    return outer_polygon
