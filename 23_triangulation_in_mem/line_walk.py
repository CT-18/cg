import itertools
from my_utils import *
import numpy as np
import matplotlib.pyplot as plt
from sympy import Point, Line, Segment, Ray, intersection

#-------------------NodeWithNeighbours-------------------------------------------#
def line_walk_node_with_neighbours(tri_node_with_neighbours, a, v1, v2, b, edges):  
    b, ray = inf_ray(a, b, 1000)
    e = Segment(v1, v2)
    node_a = None
    node_v1 = None
    node_v2 = None
    count = 0
    for idr, node in tri_node_with_neighbours.items():
        if (count == 3):
            break
        if (node.p.equals(a)):
            node_a = node
            count = count + 1
        if (node.p.equals(v1)):
            node_v1 = node
            count = count + 1
        if (node.p.equals(v2)):
            node_v2 = node
            count = count + 1

    if (is_vertex_of_segment(a, e)):
        return line_walk_node_with_neighbours_v(tri_node_with_neighbours, node_a, ray, b, edges)
    else:
        return line_walk_node_with_neighbours_e(tri_node_with_neighbours, node_v1, node_v2, ray, b, edges + [e])
                
        
def line_walk_node_with_neighbours_v(tri_node_with_neighbours, node_a, ray, b, edges):
    for idr_n_node in node_a.neigh_nodes:
        c_node = tri_node_with_neighbours[idr_n_node]
        p = c_node.p
        s = Segment(node_a.p, p) 
        inter = intersection(s, ray)
        if (inter != [] and is_segment(inter[0])):
            return line_walk_node_with_neighbours_v(tri_node_with_neighbours, c_node, Ray(p, b), b, edges + [s])
    for i,j in itertools.combinations(node_a.neigh_nodes, r=2):
        if i in set(tri_node_with_neighbours[j].neigh_nodes):
            node_i = tri_node_with_neighbours[i]
            node_j = tri_node_with_neighbours[j]
            s = Segment(node_i.p, node_j.p)
            inter = intersection(s, ray)
            if (inter != []): 
                return line_walk_node_with_neighbours_e(tri_node_with_neighbours, node_i, node_j, Ray(inter[0], b), b, edges + [s]) 
    return edges
        
def line_walk_node_with_neighbours_e(tri_node_with_neighbours, v1, v2, ray, b, edges):
    s_b = turn(b, v1.p, v2.p)
    s = Segment(v1.p, v2.p) 
    inter = intersection(s, ray) 
    if (inter != [] and is_segment(inter[0])):
        p = v1
        if (ray.contains(v2.p)):
            p = v2
        return line_walk_node_with_neighbours_v(tri_node_with_neighbours, p, Ray(p.p, b), b, edges)
    vs = list(set(v1.neigh_nodes) & set(v2.neigh_nodes))
    v3 = [i for i in vs if s_b == turn(tri_node_with_neighbours[i].p, v1.p, v2.p)]
    if (v3 == []):
        return edges
    e1 = Segment(v1.p, tri_node_with_neighbours[v3[0]].p)
    e2 = Segment(v2.p, tri_node_with_neighbours[v3[0]].p)
    inter1 = intersection(e1, ray)
    inter2 = intersection(e2, ray)
    if (inter1 != [] and inter2 != []):
        node_a = None
        for idr, node in tri_node_with_neighbours.items():
            if (node.p.equals(inter1[0])):
                node_a = node
                break        
        return line_walk_node_with_neighbours_v(tri_node_with_neighbours, node_a, Ray(inter1[0], b), b, edges)
    if (inter1 != []):
        return line_walk_node_with_neighbours_e(tri_node_with_neighbours, v1, tri_node_with_neighbours[v3[0]], Ray(inter1[0], b), b, edges + [e1])
    if (inter2 != []):
        return line_walk_node_with_neighbours_e(tri_node_with_neighbours, v2, tri_node_with_neighbours[v3[0]], Ray(inter2[0], b), b, edges + [e2])
    return edges


#-------------------NodesAndTriangles------------------------------------------#
def line_walk_nodes_and_triangles(tri_nodes_and_triangles, a, v1, v2, b, edges):  
    b, ray = inf_ray(a, b, 1000)
    e = Segment(v1, v2)
    node_a = None
    node_v1 = None
    node_v2 = None
    count = 0
    for idr, node in tri_nodes_and_triangles[0].items():
        if (count == 3):
            break
        if (node.p.equals(a)):
            node_a = node
            count = count + 1
        if (node.p.equals(v1)):
            node_v1 = node
            count = count + 1
        if (node.p.equals(v2)):
            node_v2 = node
            count = count + 1

    if (is_vertex_of_segment(a, e)):
        return line_walk_nodes_and_triangles_v(tri_nodes_and_triangles, node_a, ray, b, edges)
    else:
        return line_walk_nodes_and_triangles_e(tri_nodes_and_triangles, node_v1, node_v2, ray, b, edges + [e])
    
def line_walk_nodes_and_triangles_v(tri_nodes_and_triangles, node_a, ray, b, edges):
    for idr_n_triangles in node_a.triangles:
        for idr_n_node in tri_nodes_and_triangles[1][idr_n_triangles].nodes:
            c_node = tri_nodes_and_triangles[0][idr_n_node]
            if (c_node.idr == node_a.idr):
                continue
            p = c_node.p
            s = Segment(node_a.p, p) 
            inter = intersection(s, ray) 
            if (inter != [] and is_segment(inter[0])):
                return line_walk_nodes_and_triangles_v(tri_nodes_and_triangles, c_node, Ray(p, b), b, edges + [s])
    for idr_n_triangles in node_a.triangles:
        ds = set(tri_nodes_and_triangles[1][idr_n_triangles].nodes)
        ds.remove(node_a.idr)
        pnts = list(ds)
        node_i = tri_nodes_and_triangles[0][pnts[0]]
        node_j = tri_nodes_and_triangles[0][pnts[1]]
        s = Segment(node_i.p, node_j.p)
        inter = intersection(s, ray)
        if (inter != []): 
            return line_walk_nodes_and_triangles_e(tri_nodes_and_triangles, node_i, node_j, Ray(inter[0], b), b, edges + [s]) 
    return edges

def line_walk_nodes_and_triangles_e(tri_nodes_and_triangles, v1, v2, ray, b, edges):
    s_b = turn(b, v1.p, v2.p)
    s = Segment(v1.p, v2.p) 
    inter = intersection(s, ray) 
    if (inter != [] and is_segment(inter[0])):
        p = v1
        if (ray.contains(v2.p)):
            p = v2
        return line_walk_nodes_and_triangles_v(tri_nodes_and_triangles, p, Ray(p.p, b), b, edges)

    tp = set(v1.triangles) & set(v2.triangles)
    tp.discard(-1)
    vs = list(tp)
    vp = []
    for i in vs:
        ts = set(tri_nodes_and_triangles[1][i].nodes)
        ts.discard(v1.idr)
        ts.discard(v2.idr)
        vp = vp + list(ts)
    v3 = [i for i in vp if s_b == turn(tri_nodes_and_triangles[0][i].p, v1.p, v2.p)]
    if (v3 == []):
        return edges
    e1 = Segment(v1.p, tri_nodes_and_triangles[0][v3[0]].p)
    e2 = Segment(v2.p, tri_nodes_and_triangles[0][v3[0]].p)
    inter1 = intersection(e1, ray)
    inter2 = intersection(e2, ray)
    if (inter1 != [] and inter2 != []):
        node_a = None
        for idr, node in tri_nodes_and_triangles[0].items():
            if (node.p.equals(inter1[0])):
                node_a = node
                break        
        return line_walk_nodes_and_triangles_v(tri_nodes_and_triangles, node_a, Ray(inter1[0], b), b, edges)
    if (inter1 != []):
        return line_walk_nodes_and_triangles_e(tri_nodes_and_triangles, v1, tri_nodes_and_triangles[0][v3[0]], Ray(inter1[0], b), b, edges + [e1])
    if (inter2 != []):
        return line_walk_nodes_and_triangles_e(tri_nodes_and_triangles, v2, tri_nodes_and_triangles[0][v3[0]], Ray(inter2[0], b), b, edges + [e2])
    return edges

#-------------------NodesAndEdgesAndTriangles------------------------------------------------------#
def line_walk_nodes_and_edges_and_triangles(tri_nodes_and_edges_and_triangles, a, v1, v2, b, edges):
    b, ray = inf_ray(a, b, 1000)
    e = Segment(v1, v2)
    node_a = None
    node_v1 = None
    node_v2 = None
    count = 0
    for idr, node in tri_nodes_and_edges_and_triangles[0].items():
        if (count == 3):
            break
        if (node.p.equals(a)):
            node_a = node
            count = count + 1
        if (node.p.equals(v1)):
            node_v1 = node
            count = count + 1
        if (node.p.equals(v2)):
            node_v2 = node
            count = count + 1

    if (is_vertex_of_segment(a, e)):
        return line_walk_nodes_and_edges_and_triangles_v(tri_nodes_and_edges_and_triangles, node_a, ray, b, edges)
    else:
        return line_walk_nodes_and_edges_and_triangles_e(tri_nodes_and_edges_and_triangles, node_v1, node_v2, ray, b, edges + [e])
    
def line_walk_nodes_and_edges_and_triangles_v(tri_nodes_and_edges_and_triangles, node_a, ray, b, edges):
    for idr_n_triangles in node_a.triangles:
        for idr_n_edges in tri_nodes_and_edges_and_triangles[3][idr_n_triangles].edges:
            c_edge = tri_nodes_and_edges_and_triangles[2][idr_n_edges]
            p = None
            if (c_edge.nodes[0] == node_a.idr):
                p = tri_nodes_and_edges_and_triangles[0][c_edge.nodes[1]]
            elif (c_edge.nodes[1] == node_a.idr):
                p = tri_nodes_and_edges_and_triangles[0][c_edge.nodes[0]]
            else:
                continue
            s = Segment(node_a.p, p.p) 
            inter = intersection(s, ray) 
            if (inter != [] and is_segment(inter[0])):
                return line_walk_nodes_and_edges_and_triangles_v(tri_nodes_and_edges_and_triangles, p, Ray(p.p, b), b, edges + [s])
    for idr_n_triangles in node_a.triangles:
        for idr_n_edges in tri_nodes_and_edges_and_triangles[3][idr_n_triangles].edges:
            c_edge = tri_nodes_and_edges_and_triangles[2][idr_n_edges]
            if (c_edge.nodes[0] != node_a.idr and c_edge.nodes[1] != node_a.idr):
                node_i = tri_nodes_and_edges_and_triangles[0][c_edge.nodes[0]]
                node_j = tri_nodes_and_edges_and_triangles[0][c_edge.nodes[1]]
                s = Segment(node_i.p, node_j.p)
                inter = intersection(s, ray)
                if (inter != []): 
                    return line_walk_nodes_and_edges_and_triangles_e(tri_nodes_and_edges_and_triangles, node_i, node_j, Ray(inter[0], b), b, edges + [s]) 
    return edges

def line_walk_nodes_and_edges_and_triangles_e(tri_nodes_and_edges_and_triangles, v1, v2, ray, b, edges):
    if (v1.idr > v2.idr):
        v1, v2 = v2, v1
    s = Segment(v1.p, v2.p) 
    inter = intersection(s, ray) 
    if (inter != [] and is_segment(inter[0])):
        c_e = tri_nodes_and_edges_and_triangles[2][tri_nodes_and_edges_and_triangles[1][(v1.idr, v2.idr)]]
        m_p = tri_nodes_and_edges_and_triangles[0][c_e.nodes[0]]
        p = tri_nodes_and_edges_and_triangles[0][c_e.nodes[1]]
        if (ray.contains(m_p.p)):
            p = m_p
        return line_walk_nodes_and_edges_and_triangles_v(tri_nodes_and_edges_and_triangles, p, Ray(p.p, b), b, edges)
    s_b = turn(b, v1.p, v2.p)
    idr_v = tri_nodes_and_edges_and_triangles[1][(v1.idr, v2.idr)]
    edge_v = tri_nodes_and_edges_and_triangles[2][idr_v]
    se = None
    for i, n_triangle in enumerate(edge_v.triangles):
        mb_e = set(tri_nodes_and_edges_and_triangles[3][n_triangle].edges)
        mb_e.remove(idr_v)
        mb_e = list(mb_e)
        o_v_idr = set(tri_nodes_and_edges_and_triangles[2][mb_e[0]].nodes) & set(tri_nodes_and_edges_and_triangles[2][mb_e[1]].nodes)
        o_v_idr = list(o_v_idr)[0]
        o_v = tri_nodes_and_edges_and_triangles[0][o_v_idr]
        if s_b != turn(o_v.p, v1.p, v2.p):
            continue
        t_e1 = tri_nodes_and_edges_and_triangles[2][mb_e[0]].nodes
        t_e2 = tri_nodes_and_edges_and_triangles[2][mb_e[1]].nodes
        v1 = tri_nodes_and_edges_and_triangles[0][t_e1[0]]
        v1_n = tri_nodes_and_edges_and_triangles[0][t_e1[1]]
        e1 = Segment(v1.p, v1_n.p)
        v2 = tri_nodes_and_edges_and_triangles[0][t_e2[0]]
        v2_n = tri_nodes_and_edges_and_triangles[0][t_e2[1]]
        e2 = Segment(v2.p, v2_n.p)
        inter1 = intersection(e1, ray)
        inter2 = intersection(e2, ray)
        if (inter1 != [] and inter2 != []):      
            return line_walk_nodes_and_edges_and_triangles_v(tri_nodes_and_edges_and_triangles, o_v, Ray(inter1[0], b), b, edges)
        if (inter1 != []):
            return line_walk_nodes_and_edges_and_triangles_e(tri_nodes_and_edges_and_triangles, v1, v1_n, Ray(inter1[0], b), b, edges + [e1])
        if (inter2 != []):
            return line_walk_nodes_and_edges_and_triangles_e(tri_nodes_and_edges_and_triangles, v2, v2_n, Ray(inter2[0], b), b, edges + [e2])    
    return edges

#-------------------DoubleEdges----------------------------------#
def line_walk_double_edges(tri_double_edges, a, v1, v2, b, edges):
    b, ray = inf_ray(a, b, 1000)
    e = Segment(v1, v2)
    if (is_vertex_of_segment(a, e)):
        node_a = None
        for idr, node in tri_double_edges[0].items():
            if (node.p.equals(a)):
                node_a = node       
                break
        return line_walk_double_edges_v(tri_double_edges, node_a, ray, b, edges)
    else:
        l_he = [] 
        for idr, c_he in tri_double_edges[1].items():
            if ((tri_double_edges[0][c_he.node].p.equals(v1) and \
                tri_double_edges[0][tri_double_edges[1][c_he.nxt].node].p.equals(v2)) or \
               (tri_double_edges[0][c_he.node].p.equals(v2) and \
                tri_double_edges[0][tri_double_edges[1][c_he.nxt].node].p.equals(v1))):
                l_he.append(c_he)
        if (len(l_he) == 2):
            nxt = tri_double_edges[1][l_he[0].nxt]
            prev = tri_double_edges[1][l_he[0].prev]
            v1 = tri_double_edges[0][l_he[0].node].p
            v2 = tri_double_edges[0][nxt.node].p
            v3 = tri_double_edges[0][prev.node].p
            fi = intersection(Segment(v1, v2), ray)
            si = intersection(Segment(v2, v3), ray)
            ti = intersection(Segment(v3, v1), ray)
            if ((fi != [] and is_segment(fi[0])) or si != [] or ti != []):
                return line_walk_double_edges_e(tri_double_edges, l_he[0], ray, b, edges + [e])
            else:
                return line_walk_double_edges_e(tri_double_edges, l_he[1], ray, b, edges + [e])
        else:
            return line_walk_double_edges_e(tri_double_edges, l_he[0], ray, b, edges + [e])

def line_walk_double_edges_e(tri_double_edges, he, ray, b, edges):
    nxt = tri_double_edges[1][he.nxt]
    prev = tri_double_edges[1][he.prev]
    v1 = tri_double_edges[0][he.node]
    v2 = tri_double_edges[0][nxt.node]
    v3 = tri_double_edges[0][prev.node]
    s = Segment(v1.p, v2.p) 
    inter = intersection(s, ray) 
    if (inter != [] and is_segment(inter[0])):
        p = v1
        if (ray.contains(v2.p)):
            p = v2
        return line_walk_double_edges_v(tri_double_edges, p, Ray(p.p, b), b, edges)
    e1 = Segment(v1.p, v3.p)
    e2 = Segment(v3.p, v2.p)
    inter1 = intersection(e1, ray)
    inter2 = intersection(e2, ray)
    if (inter1 != [] and inter2 != []):
        node_a = None
        for idr, node in tri_double_edges[0].items():
            if (node.p.equals(inter1[0])):
                node_a = node
                break        
        return line_walk_double_edges_v(tri_double_edges, node_a, Ray(inter1[0], b), b, edges)
    if (inter1 != []):
        edges.append(e1)
        if (prev.twin != 0):
            return line_walk_double_edges_e(tri_double_edges, tri_double_edges[1][prev.twin], Ray(inter1[0], b), b, edges)
    if (inter2 != []):
        edges.append(e2)
        if (nxt.twin != 0):
            return line_walk_double_edges_e(tri_double_edges, tri_double_edges[1][nxt.twin], Ray(inter2[0], b), b, edges)
    return edges

def line_walk_double_edges_v(tri_double_edges, node_a, ray, b, edges):
    he = tri_double_edges[1][node_a.he]
    c_he = he
    while True:
        he_prev = tri_double_edges[1][c_he.prev]
        he_nxt = tri_double_edges[1][c_he.nxt]
        v1 = tri_double_edges[0][c_he.node]
        v2 = tri_double_edges[0][he_nxt.node]
        v3 = tri_double_edges[0][he_prev.node]
        s = Segment(v1.p, v2.p) 
        inter = intersection(s, ray)
        if (inter != [] and is_segment(inter[0])):
            return line_walk_double_edges_v(tri_double_edges, v2, Ray(v2.p, b), b, edges + [s])
        s = Segment(v1.p, v3.p) 
        inter = intersection(s, ray)
        if (inter != [] and is_segment(inter[0])):
            return line_walk_double_edges_v(tri_double_edges, v3, Ray(v3.p, b), b, edges + [s])
        s = Segment(v3.p, v2.p) 
        inter = intersection(s, ray)
        if (inter != []):
            edges.append(s)
            if (he_nxt.twin != 0):
                return line_walk_double_edges_e(tri_double_edges, tri_double_edges[1][he_nxt.twin], Ray(inter[0], b), b, edges)
            else:
                return edges
        if (he_prev.twin != 0):
            c_he = tri_double_edges[1][he_prev.twin]
        else:
            return edges
        if c_he.idr == he.idr:
            return edges


