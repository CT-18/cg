import itertools

import numpy as np
import matplotlib.pyplot as plt
from sympy import Point, Line, Segment, Ray, intersection
from cg.point import Point as cgPoint
from cg.point import turn
from my_utils import *


#-------------------NodeWithNeighbours-------------------------------------------#
def line_walk_node_with_neighbours(triang, a, v1, v2, b):
    b, ray = inf_ray(a, b, 1000)
    e = Segment(v1, v2)
    node_a = None
    node_v1 = None
    node_v2 = None
    count = 0

    for idr, node in triang.items():
        if count == 3:
            break
        if node.p.equals(a):
            node_a = node
            count = count + 1
        if node.p.equals(v1):
            node_v1 = node
            count = count + 1
        if node.p.equals(v2):
            node_v2 = node
            count = count + 1
        
    if is_vertex_of_segment(a, e):
        yield from line_walk_node_with_neighbours_v(node_a, ray, b)
    else:
        yield e
        yield from line_walk_node_with_neighbours_e(node_v1, node_v2, ray, b)


def line_walk_node_with_neighbours_v(node, ray, b):
    for n_node in node.neigh_nodes:
        p = n_node.p
        s = Segment(node.p, p) 
        inter = intersection(s, ray)
        
        if inter != [] and is_segment(inter[0]):
            yield s
            yield from line_walk_node_with_neighbours_v(n_node, Ray(p, b), b)
            raise StopIteration
            

    for i, j in itertools.combinations(node.neigh_nodes, r=2):
        if i in set(j.neigh_nodes):
            s = Segment(i.p, j.p)
            inter = intersection(s, ray)
            
            if inter != []:
                yield s
                yield from line_walk_node_with_neighbours_e(i, j, Ray(inter[0], b), b) 
                raise StopIteration


def line_walk_node_with_neighbours_e(v1, v2, ray, b):
    s_b = turn(cgPoint(int(b.x), int(b.y)), cgPoint(int(v1.p.x), int(v1.p.y)), cgPoint(int(v2.p.x), int(v2.p.y)))
    s = Segment(v1.p, v2.p) 
    inter = intersection(s, ray)

    if inter != [] and is_segment(inter[0]):
        end_node = v1
        if ray.contains(v2.p):
            end_node = v2
        yield from line_walk_node_with_neighbours_v(end_node, Ray(end_node.p, b), b)
        raise StopIteration

    vs = list(set(v1.neigh_nodes) & set(v2.neigh_nodes))
    v3 = [i for i in vs 
          if s_b == turn(cgPoint(int(i.p.x), int(i.p.y)), cgPoint(int(v1.p.x), int(v1.p.y)), cgPoint(int(v2.p.x), int(v2.p.y)))
         ]
    
    if v3 == []:
        raise StopIteration
    
    e1 = Segment(v1.p, v3[0].p)
    e2 = Segment(v2.p, v3[0].p)
    inter1 = intersection(e1, ray)
    inter2 = intersection(e2, ray)
    
    if inter1 != [] and inter2 != []:
        yield from line_walk_node_with_neighbours_v(v3[0], Ray(inter1[0], b), b)
        raise StopIteration
    if inter1 != []:
        yield e1
        yield from line_walk_node_with_neighbours_e(v1, v3[0], Ray(inter1[0], b), b)
        raise StopIteration
    if inter2 != []:
        yield e2
        yield from line_walk_node_with_neighbours_e(v2, v3[0], Ray(inter2[0], b), b)
        raise StopIteration


#-------------------NodesAndTriangles------------------------------------------#
def line_walk_nodes_and_triangles(triang, a, v1, v2, b):  
    b, ray = inf_ray(a, b, 1000)
    e = Segment(v1, v2)
    node_a = None
    node_v1 = None
    node_v2 = None
    count = 0

    for idr, node in triang[0].items():
        if count == 3:
            break
        if node.p.equals(a):
            node_a = node
            count = count + 1
        if node.p.equals(v1):
            node_v1 = node
            count = count + 1
        if node.p.equals(v2):
            node_v2 = node
            count = count + 1

    if is_vertex_of_segment(a, e):
        yield from line_walk_nodes_and_triangles_v(node_a, ray, b)
        raise StopIteration
    else:
        yield e
        yield from line_walk_nodes_and_triangles_e(node_v1, node_v2, ray, b)
    

def line_walk_nodes_and_triangles_v(node, ray, b):
    for n_triangles in node.triangles:
        if n_triangles == None:
            continue 

        for n_node in n_triangles.nodes:
            if n_node == node:
                continue

            end_node = n_node.p
            s = Segment(node.p, end_node) 
            inter = intersection(s, ray) 
            
            if inter != [] and is_segment(inter[0]):
                yield s
                yield from line_walk_nodes_and_triangles_v(n_node, Ray(end_node, b), b)
                raise StopIteration

    for n_triangles in node.triangles:
        if n_triangles == None:
            continue

        ds = set(n_triangles.nodes)
        ds.remove(node)
        pnts = list(ds)
        node_i = pnts[0]
        node_j = pnts[1]
        s = Segment(node_i.p, node_j.p)
        inter = intersection(s, ray)

        if inter != []: 
            yield s
            yield from line_walk_nodes_and_triangles_e(node_i, node_j, Ray(inter[0], b), b)
            raise StopIteration
    
    raise StopIteration


def line_walk_nodes_and_triangles_e(v1, v2, ray, b):
    s_b = turn(cgPoint(int(b.x), int(b.y)), cgPoint(int(v1.p.x), int(v1.p.y)), cgPoint(int(v2.p.x), int(v2.p.y)))
    s = Segment(v1.p, v2.p) 
    inter = intersection(s, ray) 

    if inter != [] and is_segment(inter[0]):
        end_node = v1
    
        if ray.contains(v2.p):
            end_node = v2
        
        yield from line_walk_nodes_and_triangles_v(end_node, Ray(end_node.p, b), b)

    tp = set(v1.triangles) & set(v2.triangles)
    tp.discard(None)
    vs = list(tp)
    vp = []

    for i in vs:
        ts = set(i.nodes)
        ts.discard(v1)
        ts.discard(v2)
        vp = vp + list(ts)
    
    v3 = [i for i in vp 
          if s_b == turn(cgPoint(int(i.p.x), int(i.p.y)), cgPoint(int(v1.p.x), int(v1.p.y)), cgPoint(int(v2.p.x), int(v2.p.y)))
         ]
    
    if v3 == []:
        raise StopIteration

    e1 = Segment(v1.p, v3[0].p)
    e2 = Segment(v2.p, v3[0].p)
    inter1 = intersection(e1, ray)
    inter2 = intersection(e2, ray)

    if inter1 != [] and inter2 != []:
        yield from line_walk_nodes_and_triangles_v(v3[0], Ray(inter1[0], b), b)
        raise StopIteration
    if inter1 != []:
        yield e1
        yield from line_walk_nodes_and_triangles_e(v1, v3[0], Ray(inter1[0], b), b)
        raise StopIteration
    if inter2 != []:
        yield e2
        yield from line_walk_nodes_and_triangles_e(v2, v3[0], Ray(inter2[0], b), b)
        raise StopIteration
    
    raise StopIteration


#-------------------NodesAndEdgesAndTriangles------------------------------------------------------#
def line_walk_nodes_and_edges_and_triangles(triang, a, v1, v2, b):
    b, ray = inf_ray(a, b, 1000)
    e = Segment(v1, v2)
    node_a = None
    node_v1 = None
    node_v2 = None
    count = 0

    for idr, node in triang[0].items():
        if count == 3:
            break
        if node.p.equals(a):
            node_a = node
            count = count + 1
        if node.p.equals(v1):
            node_v1 = node
            count = count + 1
        if node.p.equals(v2):
            node_v2 = node
            count = count + 1

    if is_vertex_of_segment(a, e):
        yield from line_walk_nodes_and_edges_and_triangles_v(node_a, ray, b)
        raise StopIteration
    else:
        yield e
        yield from line_walk_nodes_and_edges_and_triangles_e(node_v1, node_v2, ray, b)
        raise StopIteration
    

def line_walk_nodes_and_edges_and_triangles_v(node, ray, b):
    for n_triangles in node.triangles:
        for n_edge in n_triangles.edges:
            end_node = None
            
            if n_edge.nodes[0] == node:
                end_node = n_edge.nodes[1]
            elif n_edge.nodes[1] == node:
                end_node = n_edge.nodes[0]
            else:
                continue

            s = Segment(node.p, end_node.p) 
            inter = intersection(s, ray) 

            if inter != [] and is_segment(inter[0]):
                yield s
                yield from line_walk_nodes_and_edges_and_triangles_v(end_node, Ray(end_node.p, b), b)
                raise StopIteration

    for n_triangles in node.triangles:
        for n_edge in n_triangles.edges:
            if n_edge.nodes[0] != node and n_edge.nodes[1] != node:
                node_i = n_edge.nodes[0]
                node_j = n_edge.nodes[1]
                s = Segment(node_i.p, node_j.p)
                inter = intersection(s, ray)
                
                if inter != []:
                    yield s
                    yield from line_walk_nodes_and_edges_and_triangles_e(node_i, node_j, Ray(inter[0], b), b)
                    raise StopIteration
    raise StopIteration


def line_walk_nodes_and_edges_and_triangles_e(v1, v2, ray, b):
    s = Segment(v1.p, v2.p)
    edge = list(set(v1.edges) & set(v2.edges))[0]
    inter = intersection(s, ray)

    if (inter != [] and is_segment(inter[0])):
        end_node1 = edge.nodes[0]
        end_node2 = edge.nodes[1]

        if ray.contains(end_node2.p):
            end_node1 = end_node2
            
        yield from line_walk_nodes_and_edges_and_triangles_v(end_node1, Ray(end_node1.p, b), b)
        raise StopIteration
    s_b = turn(cgPoint(int(b.x), int(b.y)), cgPoint(int(v1.p.x), int(v1.p.y)), cgPoint(int(v2.p.x), int(v2.p.y)))
    se = None
    
    for index, n_triangle in enumerate(edge.triangles):
        mb_e = set(n_triangle.edges)
        mb_e.remove(edge)
        mb_e = list(mb_e)
        o_v = list(set(mb_e[0].nodes) & set(mb_e[1].nodes))[0]
    
        if s_b != turn(cgPoint(int(o_v.p.x), int(o_v.p.y)), cgPoint(int(v1.p.x), int(v1.p.y)),
                       cgPoint(int(v2.p.x), int(v2.p.y))):
            continue
        
        t_e1 = mb_e[0].nodes
        t_e2 = mb_e[1].nodes
        v1 = t_e1[0]
        v1_n = t_e1[1]
        e1 = Segment(v1.p, v1_n.p)
        v2 = t_e2[0]
        v2_n = t_e2[1]
        e2 = Segment(v2.p, v2_n.p)
        inter1 = intersection(e1, ray)
        inter2 = intersection(e2, ray)
        
        if inter1 != [] and inter2 != []:      
            yield from line_walk_nodes_and_edges_and_triangles_v(o_v, Ray(inter1[0], b), b)
            raise StopIteration
        if inter1 != []:
            yield e1
            yield from line_walk_nodes_and_edges_and_triangles_e(v1, v1_n, Ray(inter1[0], b), b)
            raise StopIteration
        if inter2 != []:
            yield e2
            yield from line_walk_nodes_and_edges_and_triangles_e(v2, v2_n, Ray(inter2[0], b), b)
            raise StopIteration
    
    raise StopIteration


#-------------------DoubleEdges----------------------------------#
def line_walk_double_edges(triang, a, v1, v2, b):
    b, ray = inf_ray(a, b, 1000)
    e = Segment(v1, v2)

    if is_vertex_of_segment(a, e):
        node_a = None

        for index, n in triang[0].items():
            if n.p.equals(a):
                node_a = n       
                break

        yield from line_walk_double_edges_v(node_a, ray, b)
    else:
        l_he = [] 

        for index, he in triang[1].items():
            if he.node == None:
                continue
            if ((he.node.p.equals(v1) and he.nxt.node.p.equals(v2)) or
                (he.node.p.equals(v2) and he.nxt.node.p.equals(v1))):
                l_he.append(he)
        
        if len(l_he) == 2:
            nxt = l_he[0].nxt
            prev = l_he[0].prev
            v1 = l_he[0].node.p
            v2 = nxt.node.p
            v3 = prev.node.p
            fi = intersection(Segment(v1, v2), ray)
            si = intersection(Segment(v2, v3), ray)
            ti = intersection(Segment(v3, v1), ray)
            
            if (fi != [] and is_segment(fi[0])) or si != [] or ti != []:
                yield e
                yield from line_walk_double_edges_e(l_he[0], ray, b)
            else:
                yield e
                yield from line_walk_double_edges_e(l_he[1], ray, b)
        else:
            yield e
            yield from line_walk_double_edges_e(l_he[0], ray, b)


def line_walk_double_edges_e(he, ray, b):
    nxt = he.nxt
    prev = he.prev
    v1 = he.node
    v2 = nxt.node
    v3 = prev.node
    s = Segment(v1.p, v2.p) 
    inter = intersection(s, ray) 

    if inter != [] and is_segment(inter[0]):
        end_node = v1
        if ray.contains(v2.p):
            end_node = v2
        yield from line_walk_double_edges_v(end_node, Ray(end_node.p, b), b)
        raise StopIteration

    e1 = Segment(v1.p, v3.p)
    e2 = Segment(v3.p, v2.p)
    inter1 = intersection(e1, ray)
    inter2 = intersection(e2, ray)

    if inter1 != [] and inter2 != []:       
        yield from line_walk_double_edges_v(v3, Ray(inter1[0], b), b)
        raise StopIteration
    if inter1 != []:
        yield e1
        if (prev.twin != None):
            yield from line_walk_double_edges_e(prev.twin, Ray(inter1[0], b), b)
            raise StopIteration
    if inter2 != []:
        yield e2
        if (nxt.twin != None):
            yield from line_walk_double_edges_e(nxt.twin, Ray(inter2[0], b), b)
            raise StopIteration
    raise StopIteration


def line_walk_double_edges_v(node, ray, b):
    
    list_of_n_triangles = node.get_neighbor_triangles()
    
    for t in list_of_n_triangles:
        c_he = t.he
        
        while(c_he.node != node):
            c_he = c_he.nxt
       
        he_prev = c_he.prev
        he_nxt = c_he.nxt
        v1 = c_he.node
        v2 = he_nxt.node
        v3 = he_prev.node
        
        s = Segment(v1.p, v2.p) 
        inter = intersection(s, ray)

        if inter != [] and is_segment(inter[0]):
            yield s
            yield from line_walk_double_edges_v(v2, Ray(v2.p, b), b)
            raise StopIteration

        s = Segment(v1.p, v3.p) 
        inter = intersection(s, ray)
        
        if inter != [] and is_segment(inter[0]):
            yield s
            yield from line_walk_double_edges_v(v3, Ray(v3.p, b), b)
            raise StopIteration
        
        s = Segment(v3.p, v2.p) 
        inter = intersection(s, ray)
        
        if inter != []:
            yield s
            if he_nxt.twin != None:
                yield from line_walk_double_edges_e(he_nxt.twin, Ray(inter[0], b), b)
                raise StopIteration
            else:
                raise StopIteration
    raise StopIteration