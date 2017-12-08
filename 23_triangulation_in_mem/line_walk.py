import itertools

import numpy as np
import matplotlib.pyplot as plt
from sympy import Point, Line, Segment, Ray, intersection

from my_utils import *

#-------------------NodeWithNeighbours-------------------------------------------#
def line_walk_node_with_neighbours(triang, a, v1, v2, b, edges):
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
        return line_walk_node_with_neighbours_v(node_a, ray, b, edges)
    else:
        edges.append(e)
        return line_walk_node_with_neighbours_e(node_v1, node_v2, ray, b, edges)


def line_walk_node_with_neighbours_v(node, ray, b, edges):
    for n_node in node.neigh_nodes:
        p = n_node.p
        s = Segment(node.p, p) 
        inter = intersection(s, ray)
        if (inter == None):
            print(s)
            print(ray)
        if inter != [] and is_segment(inter[0]):
            edges.append(s)
            return line_walk_node_with_neighbours_v(n_node, Ray(p, b), b, edges)

    for i, j in itertools.combinations(node.neigh_nodes, r=2):
        if i in set(j.neigh_nodes):
            s = Segment(i.p, j.p)
            inter = intersection(s, ray)
            
            if inter != []:
                edges.append(s)
                return line_walk_node_with_neighbours_e(i, j, Ray(inter[0], b), b, edges) 

    return edges


def line_walk_node_with_neighbours_e(v1, v2, ray, b, edges):
    s_b = turn(b, v1.p, v2.p)
    s = Segment(v1.p, v2.p) 
    inter = intersection(s, ray)

    if inter != [] and is_segment(inter[0]):
        end_node = v1
        if ray.contains(v2.p):
            end_node = v2
        return line_walk_node_with_neighbours_v(end_node, Ray(end_node.p, b), b, edges)

    vs = list(set(v1.neigh_nodes) & set(v2.neigh_nodes))
    v3 = [i for i in vs if s_b == turn(i.p, v1.p, v2.p)]
    
    if v3 == []:
        return edges
    
    e1 = Segment(v1.p, v3[0].p)
    e2 = Segment(v2.p, v3[0].p)
    inter1 = intersection(e1, ray)
    inter2 = intersection(e2, ray)
    
    if inter1 != [] and inter2 != []:
        return line_walk_node_with_neighbours_v(v3[0], Ray(inter1[0], b), b, edges)
    if inter1 != []:
        edges.append(e1)
        return line_walk_node_with_neighbours_e(v1, v3[0], Ray(inter1[0], b), b, edges)
    if inter2 != []:
        edges.append(e2)
        return line_walk_node_with_neighbours_e(v2, v3[0], Ray(inter2[0], b), b, edges)
    
    return edges


#-------------------NodesAndTriangles------------------------------------------#
def line_walk_nodes_and_triangles(triang, a, v1, v2, b, edges):  
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
        return line_walk_nodes_and_triangles_v(node_a, ray, b, [])
    else:
        return line_walk_nodes_and_triangles_e(node_v1, node_v2, ray, b, [e])
    

def line_walk_nodes_and_triangles_v(node, ray, b, edges):
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
                edges.append(s)
                return line_walk_nodes_and_triangles_v(n_node, Ray(end_node, b), b, edges)

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
            edges.append(s)
            return line_walk_nodes_and_triangles_e(node_i, node_j, Ray(inter[0], b), b, edges) 
    
    return edges


def line_walk_nodes_and_triangles_e(v1, v2, ray, b, edges):
    s_b = turn(b, v1.p, v2.p)
    s = Segment(v1.p, v2.p) 
    inter = intersection(s, ray) 

    if inter != [] and is_segment(inter[0]):
        end_node = v1
    
        if ray.contains(v2.p):
            end_node = v2
        
        return line_walk_nodes_and_triangles_v(end_node, Ray(end_node.p, b), b, edges)

    tp = set(v1.triangles) & set(v2.triangles)
    tp.discard(None)
    vs = list(tp)
    vp = []

    for i in vs:
        ts = set(i.nodes)
        ts.discard(v1)
        ts.discard(v2)
        vp = vp + list(ts)
    
    v3 = [i for i in vp if s_b == turn(i.p, v1.p, v2.p)]
    
    if v3 == []:
        return edges

    e1 = Segment(v1.p, v3[0].p)
    e2 = Segment(v2.p, v3[0].p)
    inter1 = intersection(e1, ray)
    inter2 = intersection(e2, ray)

    if inter1 != [] and inter2 != []:
        return line_walk_nodes_and_triangles_v(v3[0], Ray(inter1[0], b), b, edges)
    if inter1 != []:
        edges.append(e1)
        return line_walk_nodes_and_triangles_e(v1, v3[0], Ray(inter1[0], b), b, edges)
    if inter2 != []:
        edges.append(e2)
        return line_walk_nodes_and_triangles_e(v2, v3[0], Ray(inter2[0], b), b, edges)
    
    return edges


#-------------------NodesAndEdgesAndTriangles------------------------------------------------------#
def line_walk_nodes_and_edges_and_triangles(triang, a, v1, v2, b, edges):
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
        return line_walk_nodes_and_edges_and_triangles_v(node_a, ray, b, [])
    else:
        return line_walk_nodes_and_edges_and_triangles_e(node_v1, node_v2, ray, b, [e])
    

def line_walk_nodes_and_edges_and_triangles_v(node, ray, b, edges):
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
                edges.append(s)
                return line_walk_nodes_and_edges_and_triangles_v(end_node, Ray(end_node.p, b), b, edges)

    for n_triangles in node.triangles:
        for n_edge in n_triangles.edges:
            if n_edge.nodes[0] != node and n_edge.nodes[1] != node:
                node_i = n_edge.nodes[0]
                node_j = n_edge.nodes[1]
                s = Segment(node_i.p, node_j.p)
                inter = intersection(s, ray)
                
                if inter != []:
                    edges.append(s)
                    return line_walk_nodes_and_edges_and_triangles_e(node_i, node_j, Ray(inter[0], b), b, edges) 
    return edges


def line_walk_nodes_and_edges_and_triangles_e(v1, v2, ray, b, edges):
    s = Segment(v1.p, v2.p)
    edge = list(set(v1.edges) & set(v2.edges))[0]
    inter = intersection(s, ray)

    if (inter != [] and is_segment(inter[0])):
        end_node1 = edge.nodes[0]
        end_node2 = edge.nodes[1]

        if ray.contains(end_node2.p):
            end_node1 = end_node2
        return line_walk_nodes_and_edges_and_triangles_v(end_node1, Ray(end_node1.p, b), b, edges)

    s_b = turn(b, v1.p, v2.p)
    se = None
    
    for index, n_triangle in enumerate(edge.triangles):
        mb_e = set(n_triangle.edges)
        mb_e.remove(edge)
        mb_e = list(mb_e)
        o_v = list(set(mb_e[0].nodes) & set(mb_e[1].nodes))[0]
    
        if s_b != turn(o_v.p, v1.p, v2.p):
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
            return line_walk_nodes_and_edges_and_triangles_v(o_v, Ray(inter1[0], b), b, edges)
        if inter1 != []:
            edges.append(e1)
            return line_walk_nodes_and_edges_and_triangles_e(v1, v1_n, Ray(inter1[0], b), b, edges)
        if inter2 != []:
            edges.append(e2)
            return line_walk_nodes_and_edges_and_triangles_e(v2, v2_n, Ray(inter2[0], b), b, edges)    
    
    return edges


#-------------------DoubleEdges----------------------------------#
def line_walk_double_edges(triang, a, v1, v2, b, edges):
    b, ray = inf_ray(a, b, 1000)
    e = Segment(v1, v2)

    if is_vertex_of_segment(a, e):
        node_a = None

        for index, n in triang[0].items():
            if n.p.equals(a):
                node_a = n       
                break

        return line_walk_double_edges_v(node_a, ray, b, edges)
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
                edges.append(e)
                return line_walk_double_edges_e(l_he[0], ray, b, edges)
            else:
                edges.append(e)
                return line_walk_double_edges_e(l_he[1], ray, b, edges)
        else:
            edges.append(e)
            return line_walk_double_edges_e(l_he[0], ray, b, edges)


def line_walk_double_edges_e(he, ray, b, edges):
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
        return line_walk_double_edges_v(end_node, Ray(end_node.p, b), b, edges)

    e1 = Segment(v1.p, v3.p)
    e2 = Segment(v3.p, v2.p)
    inter1 = intersection(e1, ray)
    inter2 = intersection(e2, ray)

    if inter1 != [] and inter2 != []:       
        return line_walk_double_edges_v(v3, Ray(inter1[0], b), b, edges)
    if inter1 != []:
        edges.append(e1)
        if (prev.twin != None):
            return line_walk_double_edges_e(prev.twin, Ray(inter1[0], b), b, edges)
    if inter2 != []:
        edges.append(e2)
        if (nxt.twin != None):
            return line_walk_double_edges_e(nxt.twin, Ray(inter2[0], b), b, edges)
    return edges


def line_walk_double_edges_v(node, ray, b, edges):
    
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
            edges.append(s)
            return line_walk_double_edges_v(v2, Ray(v2.p, b), b, edges)

        s = Segment(v1.p, v3.p) 
        inter = intersection(s, ray)
        
        if inter != [] and is_segment(inter[0]):
            edges.append(s)
            return line_walk_double_edges_v(v3, Ray(v3.p, b), b, edges)
        
        s = Segment(v3.p, v2.p) 
        inter = intersection(s, ray)
        
        if inter != []:
            edges.append(s)
            if he_nxt.twin != None:
                return line_walk_double_edges_e(he_nxt.twin, Ray(inter[0], b), b, edges)
            else:
                return edges
    return edges