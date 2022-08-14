import pyautogui

import random
import math
import time
from inc import Recording

class Clicker:

    quadRandomList = []
    cor = []
    duration = 0
    start = 0
    startc = 0
    end = 0
    endc = 0
    radius = 0
    angle = 0
    interval = 0
    timeout = 0
    recording = True
    quad = None
    r = None

    def __init__(self, RandomMode, start, startc, end, endc, radius, angle, timeout):
        self.quadRandomList = RandomMode
        self.start = float(start)
        self.startc = float(startc)
        self.end = float(end)
        self.endc = float(endc)
        self.radius = radius
        self.angle = angle
        self.timeout = timeout

    def set_random(self):
        self.duration = random.uniform(self.start, self.end)
        self.interval = random.uniform(self.startc, self.endc)
        self.quad = random.choice(self.quadRandomList)


    def set_radius(self, MousePos, radius, angle):
        self.cor = list()
        x = 0
        y = 0
        for m in MousePos:
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            nx = random.uniform((m[0] - x), (m[0] + x))
            ny = random.uniform((m[1] - y), (m[1] + y))
            self.cor.append([nx, ny])

    def click(self, mousePositions):
        try:
            self.set_radius(mousePositions, int(self.radius), int(self.angle))
            for mouse in self.cor:
                if not self.recording:
                    self.set_random()
                    pyautogui.moveTo(mouse[0], mouse[1], self.duration, self.quad)
                    pyautogui.click(interval=self.interval)

            time.sleep(self.timeout)
        except Exception as e:
            print(e)
        return 0
