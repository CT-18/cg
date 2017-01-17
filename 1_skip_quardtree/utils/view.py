import matplotlib.pyplot as plt
from IPython.display import display

def debug_node(node, axis):
    if node.empty():
        return
    if node.simple():
        axis.plot(node.data[0], node.data[1], 'bo')
        return
    left, right, bottom, top = node.bounds
    x_mid = (left + right)/2
    y_mid = (top + bottom)/2
    axis.plot((left, left), (bottom, top), 'b')
    axis.plot((right, right), (bottom, top), 'b')
    axis.plot((x_mid, x_mid), (bottom, top), 'b--')
    axis.plot((left, right), (bottom, bottom), 'b')
    axis.plot((left, right), (top, top), 'b')
    axis.plot((left, right), (y_mid, y_mid), 'b--')
    for child in node.children.values():
        debug_node(child, axis)
    
def debug_cqtree(tree, axis):
    root = tree.root
    left, right, bottom, top = root.bounds
    debug_node(root, axis)
    axis.set_xlim(left, right)
    axis.set_ylim(bottom, top)

def apply_operation(tree, op):
    t, x, y = op
    if t == 'insert':
        tree.insert((x, y))
    elif t == 'remove':
        tree.remove((x, y))
    else:
        raise Exception('Uhdefined command')

def display_cqtree_dump(tree, ops, scale=3):
    plot, axes = plt.subplots(1, len(ops), figsize=(scale * len(ops), scale))
    for op, axis in zip(ops, axes):
        apply_operation(tree, op)
        debug_cqtree(tree, axis)
        axis.set_title("{} ({}, {})".format(*op))
    return plot