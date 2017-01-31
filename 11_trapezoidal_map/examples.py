from solution import * # Реализация трапецоидной карты

import ipywidgets as widgets
from IPython.display import Image
import matplotlib.pyplot as plt

def slideshow(folder = 'insert', period = 1500):
    images = []
    if folder == 'insert':
        n = 8
        image_width = '80%'
        comments = ['Начало',
                    's17 пересекает Δ0, Δ5, Δ10, Δ14',
                    'Вставили p17 в Δ0',
                    'Вставили q17 в Δ14',
                    'Перестроили Δ5',
                    'Перестроили Δ10',
                    ' ',
                    'Конец']
    else:
        n = 12
        image_width = '100%'
        comments = ['Начало',
                   'q левее p5',
                   'q правее p12',
                   'q правее q12',
                   'q левее p22',
                   'q ниже s21',
                   'q выше s17',
                   'q правее q14',
                   'q левее q15',
                   'q выше s15',
                   'q выше s20',
                   'Ответ: Δ14']
    for i in range(n):
        imageName = 'images/' + folder + '/'+ str(i + 1) + '.jpg'
        images.append(open(imageName, 'rb').read())
    widget = widgets.Image(value=images[0], format='jgp', width=image_width)
    
    play = widgets.Play(
        value=0,
        min=0,
        max=n,
        step=1,
        interval=period,
        disabled=False
    )
    slider = widgets.IntSlider(
        value=0,
        min=0,
        max=n-1,
        step=1
    )
    text = widgets.Text(
        value='',
        placeholder=comments[0],
        description='',
        disabled=True
    )
    
    def view_image(i):
        widget.value = images[i['new']]
        text.value = comments[i['new']]
    
    slider.observe(view_image, names='value')
    widgets.jslink((play, 'value'), (slider, 'value'))
    box = widgets.VBox([widget, widgets.HBox([play, slider, text])])
    return box


tmap = None
leftPoint = None
def start():
    global leftPoint, tmap
    tmap = TrapezoidalMap()
    leftPoint = None
    plt.figure(num=1, figsize=(12,5), dpi=65)
    cid_up = plt.gcf().canvas.mpl_connect('button_press_event', OnClick)
    plt.plot([0, 0, 5, 5, 0], [0, 5, 5, 0, 0], 'g--')
    plt.axis('off')
    plt.margins(0.01)
    plt.show()

def OnClick(event):
    global leftPoint, tmap
    if not event.dblclick:
        plt.plot(event.xdata,event.ydata,'ro')
        if leftPoint == None:
            leftPoint = [event.xdata, event.ydata]
        else:
            rightPoint = [event.xdata, event.ydata]
            if (leftPoint[0] > rightPoint[0]):
                leftPoint, rightPoint = rightPoint, leftPoint
            seg = Segment(leftPoint, rightPoint)
            tmap.insert(seg)
            "Дорисуем последние 2 трапецоида"
            for i in range(2):
                data = points(tmap.tr[len(tmap.tr) - 2 - i])
                plt.plot([data[0][0], data[1][0]], [data[0][1], data[1][1]], 'k')
                plt.plot([data[2][0], data[3][0]], [data[2][1], data[3][1]], 'k')
                plt.plot([seg.p[0], seg.q[0]], [seg.p[1], seg.q[1]], 'r')
            leftPoint = None