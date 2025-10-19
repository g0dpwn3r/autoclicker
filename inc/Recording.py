import time
import pynput.mouse
import os
import json
import pyautogui
from inc import Clicker
from inc import ConfigParse
from inc import Timer

from pynput import mouse
from pynput import keyboard
from pynput.keyboard import Key


class Recording:

    key = None
    recording = False
    waiting_for_start = False
    timer = None
    c = None
    guic = None
    append_mode = False
 
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

    def __init__(self, modelist='easeInQuad easeOutQuad easeInOutQuad easeOutQuart easeInOutQuart easeInQuad easeInBack', key='Key.space', radius=5, angle=360, start=2.0, end=5.0, startc=0, endc=5.0, append_mode=False):
        self.ModeList = modelist
        self.key = getattr(Key, key.split('.')[-1]) if isinstance(key, str) and key.startswith('Key.') else key
        self.angle = angle
        self.start = start
        self.end = end
        self.startc = startc
        self.endc = endc
        self.radius = radius
        self.append_mode = append_mode
        self.timer = Timer()
        self.parse_config()

    def record(self):
        with keyboard.Listener(on_press=self.on_press) as k, mouse.Listener(on_click=self.on_click) as m:
            while True:
                if self.waiting_for_start:
                    time.sleep(0.1)  # Small delay to prevent busy waiting
                else:
                    time.sleep(0.1)  # Small delay to prevent busy waiting


    def parse_config(self):
        try:
            cp = ConfigParse()
            if not cp.check_config():
                cp.write_config(self.ModeList, self.key, self.start, self.end, self.startc, self.endc, self.radius, self.angle, self.timeout)
            else:
                cp.read_config()
                self.c = Clicker(cp.ModeList, cp.keyOption['keybind'], cp.MouseOptions['startmove'], cp.MouseOptions['startclick'], cp.MouseOptions['endmove'], cp.MouseOptions['endclick'], cp.MouseOptions['radius'], cp.MouseOptions['angle'], cp.MouseOptions['timeout'])
        except Exception as e:
            print(f"Error parsing config: {e}")
            raise

    def start_recording(self):
        """Start recording mouse positions. In append mode, keep existing positions."""
        if not self.append_mode:
            self.mousePositions = []
        self.timer = Timer()
        self.recording = True
        if hasattr(self, 'c') and self.c:
            self.c.recording = self.recording
        print("Recording started." if not self.append_mode else "Recording started (append mode).")

    def stop_recording(self):
        """Stop recording and prepare for starting autoclicking."""
        self.recording = False
        self.waiting_for_start = True
        if hasattr(self, 'c') and self.c:
            self.c.recording = self.recording
        print("Recording stopped. Right-click to start autoclicking.")

    def start_clicking(self, continuous=False):
        """Start clicking sequence. If continuous=True, loop indefinitely until interrupted."""
        if not self.c or not self.mousePositions:
            print("DEBUG: No clicker or mouse positions available")
            return

        # Add coordinates once before the loop to prevent accumulation
        self.c.add_coordinates(self.mousePositions)
        print(f"DEBUG: Added {len(self.mousePositions)} coordinates to clicker")

        loop_count = 0
        while True:
            loop_count += 1
            try:
                print(f"DEBUG: Starting autoclicking loop {loop_count} with {len(self.c.all_coordinates)} total coordinates")
                self.c.click()
                print(f"DEBUG: Autoclicking loop {loop_count} completed successfully")

                if not continuous:
                    print("DEBUG: Single loop completed, stopping")
                    break

                print(f"DEBUG: Continuous mode - starting loop {loop_count + 1}")

            except pyautogui.FailSafeException as e:
                print(f"DEBUG: Playback interrupted by failsafe at loop {loop_count}: {e}")
                print("DEBUG: Continuous playback stopped by user")
                break
            except Exception as e:
                print(f"Error during autoclicking loop {loop_count}: {e}")
                break

        # Reset state after completion or interruption
        self.recording = False
        self.waiting_for_start = False
        # Do not clear mousePositions to allow restart
        self.timer = Timer()

    def save_recording(self, filename):
        """Save the current recording to a JSON file."""
        if not self.mousePositions:
            print("No recording to save.")
            return False
        try:
            data = {
                'mousePositions': self.mousePositions,
                'timestamp': time.time(),
                'config': {
                    'modeList': self.ModeList,
                    'key': str(self.key),
                    'angle': self.angle,
                    'start': self.start,
                    'end': self.end,
                    'startc': self.startc,
                    'endc': self.endc,
                    'radius': self.radius,
                    'timeout': self.timeout
                }
            }
            filepath = os.path.join('recordings', f"{filename}.json")
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=4)
            print(f"Recording saved to {filepath}")
            return True
        except Exception as e:
            print(f"Error saving recording: {e}")
            return False

    def load_recording(self, filename):
        """Load a recording from a JSON file."""
        try:
            filepath = os.path.join('recordings', f"{filename}.json")
            with open(filepath, 'r') as f:
                data = json.load(f)
            self.mousePositions = data.get('mousePositions', [])
            config = data.get('config', {})
            self.ModeList = config.get('modeList', self.ModeList)
            self.angle = config.get('angle', self.angle)
            self.start = config.get('start', self.start)
            self.end = config.get('end', self.end)
            self.startc = config.get('startc', self.startc)
            self.endc = config.get('endc', self.endc)
            self.radius = config.get('radius', self.radius)
            self.timeout = config.get('timeout', self.timeout)
            print(f"Recording loaded from {filepath}")
            return True
        except FileNotFoundError:
            print(f"Recording file {filename}.json not found.")
            return False
        except Exception as e:
            print(f"Error loading recording: {e}")
            return False

    def append_recording(self, filename):
        """Append the current recording to an existing recording file."""
        try:
            filepath = os.path.join('recordings', f"{filename}.json")
            if os.path.exists(filepath):
                with open(filepath, 'r') as f:
                    data = json.load(f)
                existing_positions = data.get('mousePositions', [])
                # Create a new list to avoid modifying the original
                combined_positions = existing_positions + self.mousePositions
                data['mousePositions'] = combined_positions
                data['timestamp'] = time.time()  # Update timestamp
            else:
                data = {
                    'mousePositions': self.mousePositions,
                    'timestamp': time.time(),
                    'config': {
                        'modeList': self.ModeList,
                        'key': str(self.key),
                        'angle': self.angle,
                        'start': self.start,
                        'end': self.end,
                        'startc': self.startc,
                        'endc': self.endc,
                        'radius': self.radius,
                        'timeout': self.timeout
                    }
                }
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=4)
            print(f"Recording appended to {filepath}")
            return True
        except Exception as e:
            print(f"Error appending recording: {e}")
            return False

    def on_click(self, x, y, button, pressed):
        if pressed:
            if button == pynput.mouse.Button.left:
                if self.recording:
                    try:
                        # Use pyautogui for consistent coordinates
                        pos = pyautogui.position()
                        self.timer.start()
                        self.mousePositions.append([pos.x, pos.y])
                        self.x = pos.x
                        self.y = pos.y
                        self.timer.stop()
                        self.m_interval = self.timer.elapsed_time
                        print(f"Elapsed time: {self.m_interval:0.4f} seconds")
                        self.c_interval = pressed
                    except Exception as e:
                        print(f"Error during recording click: {e}")
                        self.recording = False
                        self.waiting_for_start = False
                else:
                    return False
            elif button == pynput.mouse.Button.right:
                if self.waiting_for_start:
                    self.waiting_for_start = False
                    print("Starting autoclicking...")
                    self.start_clicking(continuous=True)
                else:
                    return False

    def on_press(self, key):
        if key == self.key:
            if self.recording:
                self.stop_recording()
            elif self.waiting_for_start:
                self.waiting_for_start = False
                print("Waiting cancelled. Press hotkey to start recording.")
            else:
                self.start_recording()
        if key == Key.esc:
            print("System exit!")
            self.recording = False
            self.waiting_for_start = False
            if hasattr(self, 'c') and self.c:
                self.c.recording = False
            return False



if __name__ == '__main__':
    r  = Recording(' '.join(['easeInQuad', 'easeOutQuad', 'easeInOutQuad', 'easeOutQuart', 'easeInOutQuart', 'easeInQuad', 'easeInBack']), 'Key.space', 360, 2.0, 5.0, 0, 4.0, 5)
    r.record()
