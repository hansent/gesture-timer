from pymt import *
from time import time
import pickle

class MultiTouchTime(MTWidget):
    def __init__(self, **kwargs):
        super(MultiTouchTime, self).__init__(**kwargs)
        getWindow().push_handlers(on_key_down=self.keyboard)
        self.size = getWindow().size
        self.touches = []
        self.start_time = 0.0
        self.trial_done = True
        self.sessions = pickle.load(open('gesture_time.data', 'r'))
        self.user = max(self.sessions.keys()) if self.sessions.keys() else "0"
        self.start_session()

    def keyboard(self, key, scan, unicode):
        if unicode == u's':
            self.start_session()
        if unicode == u'r':
            self.sessions = {}
            self.user = 0
            self.start_session()


    def start_session(self):
        pickle.dump(self.sessions, open('gesture_time.data', 'w'))
        self.user = str(int(self.user)+1)
        self.sessions[self.user] = []

    def end_trial(self):
        if len(self.touches):
            self.sessions[self.user].append([t.userdata['start_time'] for t in self.touches])
        self.touches = []
        self.trial_done = False
        self.start_time = time()

    def on_touch_down(self, touch):
        if self.trial_done:
            self.end_trial()
        t = time()
        touch.userdata['color'] = get_random_color()
        touch.userdata['start_time'] = t - self.start_time
        self.touches.append(touch)

    def on_touch_up(self, touch):
        self.trial_done = True

    def draw(self):
        set_color(1,1,1)
        drawLabel("User #: %s"%self.user, pos=(20, self.top-30), anchor_x="left", halign="left")
        for i in range(len(self.touches)):
            touch = self.touches[i]
            t = touch.userdata['start_time']
            drawLabel("touch %d : %f s"%(i, t), pos=(20,20+i*20), anchor_x="left", halign="left")
            set_color(*touch.userdata['color'])
            drawRectangle(pos=(300,20+i*20), size=(5+ self.width*t, 20))
            c = touch.userdata['color']
            if self.trial_done == False:
                set_color(c[0], c[1], c[2], 1.0)
            else:
                set_color(c[0], c[1], c[2], 0.3)
            drawCircle(pos=touch.pos, radius=30)

runTouchApp(MultiTouchTime())