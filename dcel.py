class vertex(object):
    def __init__(self, name, x, y):
        self.x = x
        self.y = y
        self.name = name
    
    def set_edge(self, edge):
        self.edge = edge

class face(object):
    def __init__(self, name, outer_edge, inner_edges):
        self.outer_edge = outer_edge
        self.inner_edges = inner_edges
        self.name = name

class hedge(object):
    def __init__(self, origin_vertex):
        self.origin_vertex = origin_vertex

    def set_edges(self, prev_edge, next_edge, twin_edge):
        self.prev_edge = prev_edge
        self.next_edge = next_edge
        self.twin_edge = twin_edge

    def set_face(self, incident_face):
        self.incident_face = incident_face