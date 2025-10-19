import pyautogui

import random
import math
import time

from inc.GUIConsole import GUIConsole

class Clicker:

    quadRandomList = []
    cor = []
    all_coordinates = []
    key = ""
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

    def __init__(self, RandomMode, key, start, startc, end, endc, radius, angle, timeout):
        try:
            self.quadRandomList = RandomMode
            self.key = key
            self.start = float(start)
            self.startc = float(startc)
            self.end = float(end)
            self.endc = float(endc)
            self.radius = int(radius)
            self.angle = int(angle)
            self.timeout = float(timeout)
            try:
                self.guic = GUIConsole.get_instance()
                print("DEBUG: GUIConsole instance obtained")
            except Exception as e:
                print(f"DEBUG: Error getting GUIConsole instance: {e}")
                self.guic = None
            self.all_coordinates = []
        except (ValueError, TypeError) as e:
            print(f"Error initializing Clicker: {e}")
            raise

    def set_random(self):
        self.duration = random.uniform(self.start, self.end)
        self.interval = random.uniform(self.startc, self.endc)
        self.quad = random.choice(self.quadRandomList)
        if self.quad is None or not callable(self.quad):
            # Use linear easing as default fallback
            self.quad = pyautogui.linear


    def add_coordinates(self, coordinates):
        """Add new coordinates to the accumulated list."""
        self.all_coordinates.extend(coordinates)

    def set_radius(self, MousePos, radius, angle):
        self.cor = list()
        angle_rad = math.radians(angle)
        x = 0
        y = 0
        for m in MousePos:
            x = radius * math.cos(angle_rad)
            y = radius * math.sin(angle_rad)
            nx = random.uniform((m[0] - x), (m[0] + x))
            ny = random.uniform((m[1] - y), (m[1] + y))
            self.cor.append([nx, ny])

    def click(self):
        try:
            print(f"DEBUG: Clicker.click called with {len(self.all_coordinates)} coordinates")
            if not self.all_coordinates:
                print("No coordinates to click.")
                return 0
            self.set_radius(self.all_coordinates, int(self.radius), int(self.angle))
            print(f"DEBUG: After set_radius, cor has {len(self.cor)} positions")
            for i, mouse in enumerate(self.cor):
                print(f"DEBUG: Processing position {i+1}/{len(self.cor)}: {mouse}")
                if not self.recording:
                    self.set_random()
                    print(f"DEBUG: Duration: {self.duration}, Interval: {self.interval}, Quad: {self.quad}")
                    if self.guic:
                        self.guic.insert_column(round(mouse[0], 2), round(mouse[1], 2), round(self.duration, 2), round(self.interval, 2))
                    else:
                        print(f"DEBUG: No GUIConsole instance, skipping insert_column")
                    try:
                        print(f"DEBUG: Moving to {mouse[0]}, {mouse[1]} with duration {self.duration}")
                        pyautogui.moveTo(mouse[0], mouse[1], self.duration, self.quad if self.quad else pyautogui.linear)
                        print("DEBUG: Clicking")
                        pyautogui.click(mouse[0], mouse[1], button="left")
                        print("DEBUG: Click completed")
                    except pyautogui.FailSafeException as e:
                        print(f"PyAutoGUI FailSafe triggered at position {i+1}: {e}")
                        print(f"DEBUG: Playback interrupted, {len(self.cor) - i - 1} positions remaining")
                        raise
                    except Exception as e:
                        print(f"Error during mouse operation at position {i+1}: {e}")
                        raise
            print(f"DEBUG: Sleeping for {self.timeout} seconds")
            time.sleep(self.timeout)
            print("DEBUG: Playback completed successfully")
        except Exception as e:
            print(f"Error in click method: {e}")
            raise
        return 0
