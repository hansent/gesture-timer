from pymt import *
from time import time

class DelayWidget(MTWidget):

    def __init__(self, **kwargs):
        super(DelayWidget, self).__init__(**kwargs)
        self.delay = 0.1
        self.waiting_touches = []

    def on_touch_down(self, touch):
        touch.userdata['start-time'] = time()
        self.waiting_touches.append(touch)

    def on_touch_move(self, touch):
        if touch in self.waiting_touches:
            if  time() -touch.userdata['start-time']> self.delay:
                self.waiting_touches.remove(touch)
                super(DelayWidget, self).on_touch_down( touch)
            return
        super(DelayWidget, self).on_touch_move( touch)

    def on_touch_up(self, touch):
        if touch in self.waiting_touches:
            self.waiting_touches.remove(touch)
            return
        super(DelayWidget, self).on_touch_up( touch)



class TouchViz(MTWidget):
    def __init__(self, **kwargs):
        super(TouchViz, self).__init__(**kwargs)
        self.touches = []

    def on_touch_down(self, touch):
        self.touches.append(touch)

    def on_touch_up(self, touch):
        self.touches.remove(touch)

    def draw(self):
        for t in self.touches:
            drawCircle(pos=t.pos, radius=30)




d = DelayWidget()
d.add_widget(TouchViz())
runTouchApp(d)