import ipywidgets as widgets
from IPython.display import Image

widget = None
def insertion_slideshow():
    def browse_images(arr):
        n = len(arr)
        def view_image(i):
            global widget
            f = open(arr[i], "rb")
            image = f.read()
            if widget != None:
                widget.value = image
                return
            widget = widgets.Image(value=image, format='jgp', width='80%')
            return widget
        widgets.interact(view_image, i=(0, n-1))
    
    images = []
    for i in range(8):
        imageName = 'images/segment/'+ str(i + 1) + '.jpg'
        images.append(imageName)
    browse_images(images)
    
lwidget = None
def localization_slideshow():
    def browse_images(arr):
        n = len(arr)
        def view_image(i):
            global lwidget
            f = open(arr[i], "rb")
            image = f.read()
            if lwidget != None:
                lwidget.value = image
                return
            lwidget = widgets.Image(value=image, format='jgp', width='100%')
            return lwidget
        widgets.interact(view_image, i=(0, n-1))
    
    images = []
    for i in range(12):
        imageName = 'images/map/'+ str(i + 1) + '.jpg'
        images.append(imageName)
    browse_images(images)