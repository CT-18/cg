from graphviz import Graph
from IPython.display import IFrame
import os

n = 32
last_level = n // 2 - 1 
points = [1, 2, 5, 8, 10, 15, 18]
new_node = ['?', '?', False, False]
inf = ['+inf', '+inf', False, False]

def make_last_level_node(gr, i, points):
    p = (i - last_level) // 2
    if i == n - 3:
        gr[i] = [points[len(points) - 1], '+inf', False, False]
        return
    elif p >= len(points):
        gr[i] = inf
        return

    if i % 2 != 0:
        if i == last_level:
            gr[i] = ['-inf', points[0], False, False]
        else:
            gr[i] = [points[p - 1], points[p], False, False]
    else:
        gr[i] = [points[p], points[p], True, True]

def build_tree(gr, i):
    if i < last_level:
        l = i * 2 + 1
        r = i * 2 + 2
        build_tree(gr, l)
        build_tree(gr, r)
        gr[i] = [gr[l][0], gr[r][1], gr[l][2], gr[r][3]]

def build_empty_interior_tree(gr, i, points):
    if i >= n: 
        return
    if i < last_level:
        build_empty_interior_tree(gr, i * 2 + 1, points)
        build_empty_interior_tree(gr, i * 2 + 2, points)
    else:
        make_last_level_node(gr, i, points)

def get_node_name(node):
    s = ''.join(['[' if node[2] else '(', str(node[0]), ':', str(node[1]), ']' if node[3] else ')'])
    return s

def show_tree(gr):
    g = Graph('G', filename='tree')
    os.makedirs('out', exist_ok = True)
    for i in range(len(gr[0]) - 1):
        color = 'green1'
        if get_node_name(gr[0][i]) != get_node_name(gr[1][i]):
            color = 'red'
        if i < last_level:
            g.node(str(i), str(get_node_name(gr[0][i])), style='filled', fillcolor=color)
        else:
            g.node(str(i), str(get_node_name(gr[0][i])), shape='square', style='filled', fillcolor=color)
    for i in range(len(gr[0])):
        l = i * 2 + 1
        r = i * 2 + 2
        if l < len(gr[0]) and l != 31:
            g.edge(str(i), str(l))
        if r < len(gr[0]):
            g.edge(str(i), str(r))
    g.render('out/tree')
    
def gen_problem():
    t = [new_node for i in range(n - 1)] 
    build_empty_interior_tree(t, 0, points)
    show_tree([t, t])


def test(test_building):
    gr = [[new_node for i in range(n)] for i in range(2)]
    for g in gr:
        build_empty_interior_tree(g, 0, points)
    test_building(gr[0], 0)
    build_tree(gr[1], 0)
    failed = False
    for i in range(len(gr[0])):
        if get_node_name(gr[0][i]) != get_node_name(gr[1][i]):
            print('К сожалению, ваш алгоритм неправильный!\nПосмотрите ошибку на рисунке и попробуйте снова.')
            failed = True
            break

    if not failed:
        print('Поздравляем! Вы успешно справились с этим заданием!')
    show_tree(gr)

