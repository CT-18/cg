import matplotlib.pyplot as plt
import ipywidgets as widgets
from IPython.display import display

def point_style(actual_point, applied):
    if (applied[0] == 'insert' or applied[0] == 'toggle') and actual_point[0] == applied[1] and actual_point[1] == applied[2]:
        return 'ro'
    else: 
        return 'bo'

def border_style(node, op_type, res):
    if op_type == 'localize' and node == res:
        return ('r', 'r--')
    else:
        return ('b', 'b--')
    
def debug_node(node, axis, applied, res):
    if node.empty():
        return
    if node.simple():
        axis.plot(node.data[0], node.data[1], point_style(node.data, applied))
        return
    b, b_ = border_style(node, applied[0], res)
    left, right, bottom, top = node.bounds
    x_mid = (left + right)/2
    y_mid = (top + bottom)/2
    axis.plot((left, left), (bottom, top), b)
    axis.plot((right, right), (bottom, top), b)
    axis.plot((x_mid, x_mid), (bottom, top), b_)
    axis.plot((left, right), (bottom, bottom), b)
    axis.plot((left, right), (top, top), b)
    axis.plot((left, right), (y_mid, y_mid), b_)
    for child in node.children.values():
        debug_node(child, axis, applied, res)
    
def debug_cqtree(tree, axis, applied=('none'), res=None):
    root = tree.root
    left, right, bottom, top = root.bounds
    debug_node(root, axis, applied, res)
    axis.set_xlim(left, right)
    axis.set_ylim(bottom, top)
    
def debug_sqtree(tree, axis, level_id, applied=('none'), res=None):
    debug_cqtree(tree.levels[level_id], axis, applied, res)

def apply_operation(tree, op):
    t = op[0]
    if t == 'none':
        return
    if t == 'localize':
        return tree.localize((op[1], op[2]))
    if t == 'insert':
        return tree.insert((op[1], op[2]))
    if t == 'remove':
        return tree.remove((op[1], op[2]))    
    if t == 'toggle':
        return tree.toggle((op[1], op[2]))
    raise Exception('Unknown command')
    
def init_tree(tree, points):
    for point in points:
        tree.insert(point)
    
def apply_operations(tree, ops):
    for op in ops:
        apply_operation(tree, op)

def display_cqtree_dump(tree, ops, scale=3):
    fig, axes = plt.subplots(1, len(ops), figsize=(scale * len(ops), scale))
    for op, axis in zip(ops, axes):
        apply_operation(tree, op)
        debug_cqtree(tree, axis, op)
        axis.set_title("{} ({}, {})".format(*op))

_tree = None
_ax = None
_slider = None

def cqtree_press_callback(event):
    global _ax, _tree
    
    x = int(round(event.xdata))
    y = int(round(event.ydata))
    op_type = 'localize' if event.button == 3 else 'toggle'
    op = (op_type, x, y)
    
    res = apply_operation(_tree, op)
    
    _ax.clear()
    debug_cqtree(_tree, _ax, op, res)
    display(_ax.figure)

def sqtree_press_callback(event):
    global _tree, _slider
    
    x = int(round(event.xdata))
    y = int(round(event.ydata))
    op_type = 'remove' if event.button == 3 else 'insert'
    op = (op_type, x, y)
    
    res = apply_operation(_tree, op)
    _slider.max = len(_tree.levels)
    
    sqtree_display(_slider.value - 1, op, res)
    
def sqtree_level_change(change):
    level_id = change['new'] - 1
    sqtree_display(level_id, ('none'), None)
    
def sqtree_display(level_id, op, res):
    global _ax, _tree, _slider
    _ax.clear()
    debug_sqtree(_tree, _ax, level_id, op, res)
    
def display_cqtree_interactive(tree, scale=10):
    global _ax, _tree
    
    _tree = tree
    fig = plt.figure(1, figsize=(scale, scale))
    _ax = plt.subplot(111)
    fig.canvas.mpl_connect('button_press_event', cqtree_press_callback)
    debug_cqtree(_tree, _ax)
    
def display_sqtree_interactive(tree, scale=10):
    global _ax, _tree, _slider
    
    _tree = tree
    fig = plt.figure(1, figsize=(scale, scale))
    _ax = plt.subplot(111)
    _slider = widgets.IntSlider(min=1,max=len(_tree.levels),description='Level: ')
    _slider.observe(sqtree_level_change, names='value')
    fig.canvas.mpl_connect('button_press_event', sqtree_press_callback)
    debug_sqtree(_tree, _ax, 0) 
    display(_slider)
    