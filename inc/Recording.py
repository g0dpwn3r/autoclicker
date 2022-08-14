import pynput.mouse
import os, sys
from inc import Clicker
from inc import ConfigParse
from pynput import mouse
from pynput import keyboard
from pynput.keyboard import Key


class Recording:

    key = None
    recording = True
    c = None
    mousePositions = list()
    angle = 360
    start = 2
    startc = 0
    end = 5
    endc = 5
    radius = 5
    timeout = 2
    ModeList = 'easeInQuad easeOutQuad easeInOutQuad easeOutQuart easeInOutQuart easeInQuad easeInBack'

    def record(self):
        with keyboard.Listener(on_press=self.on_press) as k:
            while True:
                self.get_positions()
                self.start_clicking()
                self.mousePositions = []



    def parse_config(self):
        cp = ConfigParse.ConfigParse()
        if not cp.check_config():
            cp.write_config(self.ModeList, self.start, self.end, self.startc, self.endc, self.radius, self.angle, self.timeout)
        else:
            cp.read_config()
            self.c = Clicker.Clicker(cp.ModeList, cp.MouseOptions['startmove'], cp.MouseOptions['startclick'], cp.MouseOptions['endmove'], cp.MouseOptions['endclick'], cp.MouseOptions['radius'], cp.MouseOptions['angle'], cp.MouseOptions['timeout'])

    def start_clicking(self):
        while not self.recording:
            print(self.mousePositions)
            self.c.click(self.mousePositions)
            pass

    def on_click(self, x, y, button, pressed):
        if pressed and button == pynput.mouse.Button.left:
            if self.recording:
                self.mousePositions.append([x, y])
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

