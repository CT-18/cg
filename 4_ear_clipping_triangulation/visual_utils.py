import re
import os
import shutil
import struct
from collections import defaultdict

import matplotlib.pyplot as plt
import ipywidgets as widgets
import traitlets

from cg import Point
# from cg import turn
from hidden import turn
from enum import Enum

def natural_sort(l): 
    convert = lambda text: int(text) if text.isdigit() else text.lower() 
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(l, key = alphanum_key)

def visual_dump_triang(cur_v,D,D1,S,Q,filename):
    xmin, xmax = min([i.x for i in Q]) - 2, max([i.x for i in Q]) + 2
    ymin, ymax = min([i.y for i in Q]) - 2, max([i.y for i in Q]) + 2
    fig = plt.figure(figsize=(5,5))
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

def visual_dump_ear_clipping_triangulation(cur_v, D, D1, S, filename):
    xmin, xmax = min([i.origin.x for i in D]) - 2, max([i.origin.x for i in D]) + 2
    ymin, ymax = min([i.origin.y for i in D]) - 2, max([i.origin.y for i in D]) + 2
    fig = plt.figure(figsize=(5,5))
    for h in D:
        xs = [h.origin.x, h.twin.origin.x]
        ys = [h.origin.y, h.twin.origin.y]
        plt.plot(xs,ys,'k-')
    for h in D1:
        xs = [h.origin.x, h.twin.origin.x]
        ys = [h.origin.y, h.twin.origin.y]
        plt.plot(xs,ys,'b:')
    for h in S:
        xs = [h.origin.x, h.twin.origin.x]
        ys = [h.origin.y, h.twin.origin.y]
        plt.plot(xs,ys,'r')
    if not cur_v is None:
        plt.plot(cur_v.x, cur_v.y, 'yo')
    plt.axis([xmin,xmax, ymin,ymax])
    plt.savefig(filename)
    plt.close(fig)
    
def visual_dump_bypass(cur_v, D, filename):
    xmin, xmax = min([i.origin.x for i in D]) - 2, max([i.origin.x for i in D]) + 2
    ymin, ymax = min([i.origin.y for i in D]) - 2, max([i.origin.y for i in D]) + 2
    fig = plt.figure(figsize=(5,5))
    for h in D:
        xs = [h.origin.x, h.twin.origin.x]
        ys = [h.origin.y, h.twin.origin.y]
        plt.plot(xs,ys,'k-')
    if not cur_v is None:
        plt.plot(cur_v.x, cur_v.y, 'yo')
    plt.axis([xmin,xmax, ymin,ymax])
    plt.savefig(filename)
    plt.close(fig)
    
class Merging_step(Enum):
    BEFORE_START = 0
    LEFT_LOWER = 1
    RAY = 2
    INTERSECTED = 3
    REFLEX_VERTEXES = 4
    REFLEX_SORTING = 5
    CLOSEST = 6
    MERGE = 7

def visual_dump_holes_merging(args, D, holes, filename):
    xmin, xmax = min([i.origin.x for i in D]) - 2, max([i.origin.x for i in D]) + 2
    ymin, ymax = min([i.origin.y for i in D]) - 2, max([i.origin.y for i in D]) + 2
    fig = plt.figure(figsize=(5,5))

    def draw_ray(args):
        xs = [args['ray'][0].x, args['ray'][1].x]
        ys = [args['ray'][0].y, args['ray'][1].y]
        plt.plot(xs, ys, 'g--')

    def draw_triangle(args):
        xs = [args['triangle'][0].x, args['triangle'][1][0]]
        ys = [args['triangle'][0].y, args['triangle'][1][1]]
        plt.plot(xs,ys,'m--')
        xs = [args['triangle'][1][0], args['triangle'][2].x]
        ys = [args['triangle'][1][1], args['triangle'][2].y]
        plt.plot(xs,ys,'m--')
        xs = [args['triangle'][2].x, args['triangle'][0][0]]
        ys = [args['triangle'][2].y, args['triangle'][0][1]]
        plt.plot(xs,ys,'m--')

    for h in D:
        xs = [h.origin.x, h.twin.origin.x]
        ys = [h.origin.y, h.twin.origin.y]
        plt.plot(xs,ys,'k-')
    for hole in holes:
        for h in hole:
            xs = [h.origin.x, h.twin.origin.x]
            ys = [h.origin.y, h.twin.origin.y]
            plt.plot(xs,ys,'k-')
    
    step = args['step']
    if step == Merging_step.BEFORE_START:
        pass
    elif step == Merging_step.LEFT_LOWER:
        plt.plot(args['llh'].origin.x, args['llh'].origin.y, 'yo')
    elif step == Merging_step.RAY:
        draw_ray(args)
    elif step == Merging_step.INTERSECTED:
        draw_ray(args)
        for x, y, h in args['intersected']:
            xs = [h.origin.x, h.twin.origin.x]
            ys = [h.origin.y, h.twin.origin.y]
            plt.plot(xs,ys,'r-')
    elif step == Merging_step.REFLEX_VERTEXES:
        draw_ray(args)
        if isinstance(args['closest'], Point):
            plt.plot(args['closest'].x, args['closest'].y, 'ro')
        else:
            xs = [args['closest'].origin.x, args['closest'].twin.origin.x]
            ys = [args['closest'].origin.y, args['closest'].twin.origin.y]
            plt.plot(xs,ys,'r-')
    elif step == Merging_step.REFLEX_SORTING:
        draw_triangle(args)
        for h in args['reflex']:
            plt.plot(h.origin.x, h.origin.y, 'ro')
            xs = [args['triangle'][0].x, h.origin.x]
            ys = [args['triangle'][0].y, h.origin.y]
            plt.plot(xs,ys,'b:')
            
    elif step == Merging_step.CLOSEST:
        draw_triangle(args)
        plt.plot(args['closest'].origin.x, args['closest'].origin.y, 'ro')
    elif step == Merging_step.MERGE:
        for h in args['polygon']:
            xs = [h.origin.x, h.twin.origin.x]
            ys = [h.origin.y, h.twin.origin.y]
            plt.plot(xs,ys,'k-')
    
    plt.axis([xmin,xmax, ymin,ymax])
    plt.savefig(filename)
    plt.close(fig)

def create_dump_func(folder, func, *args):
    c = 0
    shutil.rmtree(folder, ignore_errors=True)
    os.makedirs(folder, exist_ok=True)
    def dump(v):
        nonlocal c
        func(v, *args, filename = os.path.join(folder,'{}.png'.format(c)))
        c += 1
    return dump

def _get_png_info(data):
    w, h = struct.unpack('>LL', data[16:24])
    width = int(w)
    height = int(h)
    return width, height
    
def SlideShower(folder, frame_duration=800):
    slides = list([open(os.path.join(folder,s), 'rb').read()
                   for s in natural_sort(os.listdir(folder))])

    x, y = _get_png_info(slides[0])
    img = widgets.Image(value=slides[0], width=x, height=y)

    def on_frame(change):
        n = change['new']
        img.value = slides[n]

    play = widgets.Play(
        value=0,
        min=0,
        max=len(slides),
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
