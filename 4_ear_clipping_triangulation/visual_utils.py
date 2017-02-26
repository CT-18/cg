import re
import os
import shutil
import struct
from collections import defaultdict

import matplotlib.pyplot as plt
import ipywidgets as widgets
import traitlets

from cg import Point
from hidden import VType, append_shorthands 

def natural_sort(l): 
    convert = lambda text: int(text) if text.isdigit() else text.lower() 
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(l, key = alphanum_key)

def _type_color(v):
        if v.vtype == VType.regular:
            return 'ok'
        if v.vtype == VType.start:
            return 'sy'
        if v.vtype == VType.end:
            return 'sg'
        if v.vtype == VType.split:
            return '^r'
        if v.vtype == VType.merge:
            return 'vb'

def draw_points(source, types=False):
    xmin, xmax = min([i.x for i in source]) - 2, max([i.x for i in source]) + 2
    ymin, ymax = min([i.y for i in source]) - 2, max([i.y for i in source]) + 2
    plt.figure(figsize=(6,6))
    plt.plot([i.x for i in source + [source[0]]], [i.y for i in source + [source[0]]],'k-', zorder=0)
    if types:
        d = defaultdict(list)
        for v in source:
            d[_type_color(v)].append(v)
        for k in d:
            plt.plot([v.x for v in d[k]], [v.y for v in d[k]], k, label=str(d[k][0].vtype).split('.')[1], zorder=1)
        plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.,numpoints=1)
    else:
        for v in source:
            plt.plot(v.x, v.y,'ko', zorder=1)
    plt.axis([xmin,xmax, ymin,ymax])
    plt.show()

def visual_dump_pieces(cur_v, D,D1,T,Q,filename):
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
    for h in T:
        xs = [h.origin.x, h.twin.origin.x]
        ys = [h.origin.y, h.twin.origin.y]
        plt.plot(xs,ys,'b-')
    d = defaultdict(list)
    for v in Q:
        d[_type_color(v)].append(v)
    for k in d:
            plt.plot([v.x for v in d[k]], [v.y for v in d[k]], k, label=str(d[k][0].vtype).split('.')[1], zorder=100)
    if not cur_v is None:
        plt.axhline(cur_v.y, xmin=0.05, xmax=0.95, color='black',linestyle='dashed')
    plt.axis([xmin,xmax, ymin,ymax])
    lgd = plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.,numpoints=1)
    plt.savefig(filename, bbox_extra_artists=(lgd,), bbox_inches='tight')
    plt.close(fig)

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
    
from enum import Enum
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
        for i in range(3):
            xs = [args['triangle'][i].x, args['triangle'][(i + 1) % 3].x]
            ys = [args['triangle'][i].y, args['triangle'][(i + 1) % 3].y]
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
