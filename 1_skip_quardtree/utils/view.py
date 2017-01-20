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
    fig, axes = plt.subplots(1, len(ops), figsize=(scale * len(ops), scale))
    for op, axis in zip(ops, axes):
        apply_operation(tree, op)
        debug_cqtree(tree, axis)
        axis.set_title("{} ({}, {})".format(*op))

viewer = None
        
class TreeViewer:
    
    def __init__(self, tree, ax):
        self.tree = tree
        self.ax = ax
        ax.figure.canvas.mpl_connect('button_press_event', self.press_callback)
        
    def press_callback(self, event):
        self.tree.insert((event.xdata, event.ydata))
        self.ax.clear()
        debug_cqtree(self.tree, self.ax)
        display(self.ax.figure)


def display_cqtree_interactive(tree, scale=3):
    fig = plt.figure(1, figsize=(scale, scale))
    ax = plt.subplot(111)
    global viewer
    viewer = TreeViewer(tree, ax)
    debug_cqtree(tree, ax)