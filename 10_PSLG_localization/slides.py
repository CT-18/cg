import ipywidgets as widgets
from IPython.display import Image
import matplotlib.pyplot as plt

def slideshow(period = 1500):
    images = []
    n = 2
    image_width = '40%'
    comments = ['Красным цветом отмечены точки, которые будут удалены',
                'Перетриангулированный после удаления точек PSLG']
    for i in range(n):
        imageName = 'images/kirkpatrick' + str(i + 3) + '.png'
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
    text = widgets.Textarea(
        value=comments[0],
        placeholder='',
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

