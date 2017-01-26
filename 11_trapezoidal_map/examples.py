import ipywidgets as widgets
from IPython.display import Image

def slideshow(folder = 'insert', period = 1500):
    images = []
    if folder == 'insert':
        n = 8
        image_width = '80%'
    else:
        n = 12
        image_width = '100%'
    for i in range(n):
        imageName = 'images/' + folder + '/'+ str(i + 1) + '.jpg'
        images.append(open(imageName, 'rb').read())
    widget = widgets.Image(value=images[0], format='jgp', width=image_width)
    
    def view_image(i):
        widget.value = images[i['new']]
    
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
    slider.observe(view_image, names='value')
    widgets.jslink((play, 'value'), (slider, 'value'))
    box = widgets.VBox([widget, widgets.HBox([play, slider])])
    return box