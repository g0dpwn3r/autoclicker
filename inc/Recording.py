import pynput.mouse
import os
from inc import Clicker
from inc import ConfigParse
from inc import Timer

from pynput import mouse
from pynput import keyboard
from pynput.keyboard import Key


class Recording:

    key = None
    recording = True
    timer = None
    c = None
    guic = None

    mousePositions = []

    x = 0
    y = 0
    angle = 360
    start = 2
    startm = 0
    startc = 0
    end = 5
    endc = 5
    m_interval = 0
    c_interval = 0
    radius = 5
    timeout = 2

    ModeList = 'easeInQuad easeOutQuad easeInOutQuad easeOutQuart easeInOutQuart easeInQuad easeInBack'

    def __init__(self, modelist='easeInQuad easeOutQuad easeInOutQuad easeOutQuart easeInOutQuart easeInQuad easeInBack', key='Key.space', radius=5, angle=360, start=2.0, end=5.0, startc=0, endc=5.0):
        self.ModeList = modelist
        self.key = key
        self.angle = angle
        self.start = start
        self.end = end
        self.startc = startc
        self.endc = endc
        self.radius = radius
        self.timer = Timer()
        self.parse_config()

    def record(self):
        with keyboard.Listener(on_press=self.on_press) as k:
            while True:
                self.get_positions()
                self.start_clicking()
                self.mousePositions = []


    def parse_config(self):
        cp = ConfigParse()
        if not cp.check_config():
            cp.write_config(self.ModeList, self.key, self.start, self.end, self.startc, self.endc, self.radius, self.angle, self.timeout)
        else:
            cp.read_config()
            self.c = Clicker(cp.ModeList, cp.keyOption['keybind'], cp.MouseOptions['startmove'], cp.MouseOptions['startclick'], cp.MouseOptions['endmove'], cp.MouseOptions['endclick'], cp.MouseOptions['radius'], cp.MouseOptions['angle'], cp.MouseOptions['timeout'])

    def start_clicking(self):
        while not self.recording:
            self.c.click(self.mousePositions)
            pass

    def on_click(self, x, y, button, pressed):
        if not self.timer._start_time:
            self.timer.start()
        if pressed and button == pynput.mouse.Button.left:
            if self.recording:
                self.mousePositions.append([x, y])
                if self.timer._start_time:
                    self.timer.stop()
                self.x = x
                self.y = y
                self.m_interval = self.timer.elapsed_time
                self.c_interval = pressed
            else:
                return False

    def on_press(self, key):
        if key == self.key:
            self.recording = not self.recording
            self.c.recording = self.recording
        if key == Key.esc:
            print("System exit!")
            os._exit(0)

    def get_positions(self):
        with mouse.Listener(on_click=self.on_click) as m:
            m.join()


if __name__ == '__main__':
    r  = Recording(' '.join(['easeInQuad', 'easeOutQuad', 'easeInOutQuad', 'easeOutQuart', 'easeInOutQuart', 'easeInQuad', 'easeInBack']), 'Key.space', 360, 2.0, 5.0, 0, 4.0, 5)
    r.record()
