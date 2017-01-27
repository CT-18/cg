import ipywidgets as widgets
from IPython.display import Image

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
                    'Обновленная локализационная структура',
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
        placeholder='Type something',
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