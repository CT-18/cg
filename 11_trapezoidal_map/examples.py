from solution import *  # Реализация трапецоидной карты

import ipywidgets as widgets
from IPython.display import Image
import matplotlib.pyplot as plt
import math


def slideshow(folder='insert', period=1500):
    images = []
    if folder == 'insert':
        n = 8
        image_width = '80%'
        comments = ['Начало',
                    's17 пересекает Δ0, Δ5, Δ10, Δ14',
                    'Перестроили Δ0',
                    'Перестроили Δ5',
                    'Перестроили Δ10',
                    'Перестроили Δ14',
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
        imageName = 'images/' + folder + '/' + str(i + 1) + '.jpg'
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
        max=n - 1,
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


# Методы для отрисовки трапецоида
def perp(a):
    b = np.empty_like(a)
    b[0] = -a[1]
    b[1] = a[0]
    return b


def intersectionPoint(a1, a2, b1, b2):
    """Возвращает точку пересечения отрезков"""
    a1 = np.array([a1[0], a1[1]])
    a2 = np.array([a2[0], a2[1]])
    b1 = np.array([b1.coord[0], b1.coord[1]])
    b2 = np.array([b2.coord[0], b2.coord[1]])
    da = a2 - a1
    db = b2 - b1
    dp = a1 - b1
    dap = perp(da)
    denom = np.dot(dap, db)
    num = np.dot(dap, dp)
    return (num / denom.astype(float)) * db + b1


def points(trapezoid):
    """Возвращает угловые точки трапецоида"""
    q1 = [0, 0]
    q2 = [0, 500]
    q3 = [500, 500]
    q4 = [500, 0]
    if trapezoid.leftp is not None:
        q1[0] = trapezoid.leftp.coord[0]
        q2[0] = trapezoid.leftp.coord[0]
    if trapezoid.rightp is not None:
        q3[0] = trapezoid.rightp.coord[0]
        q4[0] = trapezoid.rightp.coord[0]
    if trapezoid.top is not None:
        intp = intersectionPoint(q1, q2, trapezoid.top.p, trapezoid.top.q)
        q2[1] = intp[1]
        intp = intersectionPoint(q3, q4, trapezoid.top.p, trapezoid.top.q)
        q3[1] = intp[1]
    if trapezoid.bottom is not None:
        intp = intersectionPoint(q1, q2, trapezoid.bottom.p, trapezoid.bottom.q)
        q1[1] = intp[1]
        intp = intersectionPoint(q3, q4, trapezoid.bottom.p, trapezoid.bottom.q)
        q4[1] = intp[1]
    return [q1, q2, q3, q4]


tmap = None
left_point = None
figure = None
chosen_point = None


def interactive_example():
    global left_point, tmap, figure
    tmap = TrapezoidMap()
    left_point = None
    figure = plt.figure(num=' ', figsize=(12, 5), dpi=65)
    plt.gcf().canvas.mpl_connect('button_press_event', on_click)
    plt.gcf().canvas.mpl_connect('motion_notify_event', on_move)
    plt.plot([0, 0, 500, 500, 0], [0, 500, 500, 0, 0], 'g--')
    plt.axis('off')
    plt.margins(0.01)
    plt.show()


def find_nearest_point(x, y):
    global tmap
    minx = x
    miny = y
    for segment in tmap.segments:
        dx = int(abs(x - segment.p.coord[0]))
        dy = int(abs(y - segment.p.coord[1]))
        dist = math.sqrt(dx * dx + dy * dy)
        if dist < 10.0:
            minx = segment.p.coord[0]
            miny = segment.p.coord[1]
            break
        dx = int(abs(x - segment.q.coord[0]))
        dy = int(abs(y - segment.q.coord[1]))
        dist = math.sqrt(dx * dx + dy * dy)
        if dist < 10.0:
            minx = segment.q.coord[0]
            miny = segment.q.coord[1]
            break
    return Point(int(minx), int(miny))


def on_click(event):
    global left_point, tmap
    if not event.dblclick:
        if left_point is None:
            left_point = find_nearest_point(int(round(event.xdata)), int(round(event.ydata)))
            plt.plot(left_point.coord[0], left_point.coord[1], 'ro')
        else:
            right_point = find_nearest_point(int(round(event.xdata)), int(round(event.ydata)))
            if right_point < left_point:
                left_point, right_point = right_point, left_point
            seg = Segment(left_point, right_point)
            insert(tmap, seg)
            # Очистим карту
            figure.clear()
            plt.axis('off')
            plt.margins(0.01)
            plt.plot([0, 0, 500, 500, 0], [0, 500, 500, 0, 0], 'g--')
            # Перерисуем карту
            for tr in tmap.tr:
                data = points(tr)
                if not tr.is_leftmost():
                    plt.plot([data[0][0], data[1][0]], [data[0][1], data[1][1]], 'k')
                if not tr.is_rightmost():
                    plt.plot([data[2][0], data[3][0]], [data[2][1], data[3][1]], 'k')
            for segment in tmap.segments:
                plt.plot([segment.p[0], segment.q[0]], [segment.p[1], segment.q[1]], 'r')
            plt.plot(left_point.coord[0], left_point.coord[1], 'ro')
            plt.plot(right_point.coord[0], right_point.coord[1], 'ro')
            left_point = None


def on_move(event):
    global chosen_point
    if event.xdata is None:
        return
    x = int(round(event.xdata))
    y = int(round(event.ydata))
    mouse_point = Point(x, y)
    nearest_point = find_nearest_point(x, y)
    if mouse_point == nearest_point:
        if chosen_point is not None:
            try:
                chosen_point.remove()
            except ValueError:
                pass
            chosen_point = None
    elif chosen_point is None:
            chosen_point, = plt.plot(nearest_point.coord[0], nearest_point.coord[1], 'co')
