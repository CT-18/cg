import re
import os

import matplotlib.pyplot as plt
import ipywidgets as widgets
import traitlets

def natural_sort(l): 
    convert = lambda text: int(text) if text.isdigit() else text.lower() 
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(l, key = alphanum_key)

def draw_points(source, types=False):
    def type_color(v):
        if v.vtype == 'regular':
            return 'ok'
        if v.vtype == 'start':
            return 'sy'
        if v.vtype == 'end':
            return 'sg'
        if v.vtype == 'split':
            return '^r'
        if v.vtype == 'merge':
            return 'vb'
    xmin, xmax = min([i.x for i in source]) - 2, max([i.x for i in source]) + 2
    ymin, ymax = min([i.y for i in source]) - 2, max([i.y for i in source]) + 2
    plt.plot([i.x for i in source + [source[0]]], [i.y for i in source + [source[0]]],'k-', zorder=0)
    if types:
        for v in source:
            plt.plot(v.x, v.y,type_color(v), zorder=1)
    else:
        for v in source:
            plt.plot(v.x, v.y,'ko', zorder=1)
    plt.axis([xmin,xmax, ymin,ymax])
    plt.show()

def visual_dump_state(cur_v, D,D1,T,Q,filename):
    xmin, xmax = min([i.x for i in Q]) - 2, max([i.x for i in Q]) + 2
    ymin, ymax = min([i.y for i in Q]) - 2, max([i.y for i in Q]) + 2
    fig = plt.figure()
    for h in D:
        xs = [h.origin.x, h.twin.origin.x]
        ys = [h.origin.y, h.twin.origin.y]
        plt.plot(xs,ys,'k-')
    for h in D1:
        xs = [h.origin.x, h.twin.origin.x]
        ys = [h.origin.y, h.twin.origin.y]
        plt.plot(xs,ys,'b:')
    for h in T:
        xs = [h.origin.x, h.twin.origin.x]
        ys = [h.origin.y, h.twin.origin.y]
        plt.plot(xs,ys,'b-')
    for q in Q:
        if cur_v is None or q < cur_v:
            plt.plot(q.x, q.y, 'ko')
    if not cur_v is None:
        plt.plot(cur_v.x, cur_v.y, 'ro')
    plt.axis([xmin,xmax, ymin,ymax])
    plt.savefig(filename)
    plt.close(fig)

def visual_dump_triang(cur_v,D,D1,S,Q,filename):
    xmin, xmax = min([i.x for i in Q]) - 2, max([i.x for i in Q]) + 2
    ymin, ymax = min([i.y for i in Q]) - 2, max([i.y for i in Q]) + 2
    fig = plt.figure()
    for h in D:
        xs = [h.origin.x, h.twin.origin.x]
        ys = [h.origin.y, h.twin.origin.y]
        plt.plot(xs,ys,'k-')
    for h in D1:
        xs = [h.origin.x, h.twin.origin.x]
        ys = [h.origin.y, h.twin.origin.y]
        plt.plot(xs,ys,'b:')
    for q in Q:
        if cur_v is None or q < cur_v:
            plt.plot(q.x, q.y, 'ko')
    for q in S:
        plt.plot(q.x, q.y, 'yo')
    if not cur_v is None:
        plt.plot(cur_v.x, cur_v.y, 'ro')
    plt.axis([xmin,xmax, ymin,ymax])
    plt.savefig(filename)
    plt.close(fig)
    
def SlideShower(folder, frame_duration=800):
    slides = list([open(os.path.join(folder,s), 'rb').read()
                   for s in natural_sort(os.listdir(folder))])

    img = widgets.Image(value=slides[0],width=600,height=400)

    def on_frame(change):
        n = change['new']
        img.value = slides[n]

    play = widgets.Play(
        value=0,
        min=0,
        max=len(slides)-1,
        step=1,
        interval=frame_duration,
        disabled=False
    )
    slider = widgets.IntSlider(
        value=0,
        min=0,
        max=len(slides)-1,
        step=1
    )
    slider.observe(on_frame, names='value')
    widgets.jslink((play, 'value'), (slider, 'value'))
    box = widgets.VBox([img, widgets.HBox([play, slider])])
    return box
