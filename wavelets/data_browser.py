import numpy as np

class PointBrowser(object):
    """
    Click on a point to select and highlight it -- the data that
    generated the point will be shown in the lower axes.  Use the 'n'
    and 'p' keys to browse through the next and previous points
    """

    def __init__(self):
        pass

    def on_button_release(self, mouse_event):
        # the click locations
        x = mouse_event.xdata
        y = mouse_event.ydata

        print("selected: {0:f}, {1:f}".format(x,y))
