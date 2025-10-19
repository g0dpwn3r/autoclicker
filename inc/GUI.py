from tkinter import *
from tkinter import messagebox as mb
from tkinter import ttk
from tkinter import simpledialog
from pynput import keyboard
import pyautogui as pag
import threading
import subprocess
import platform

from inc import Recording
from inc import ConfigParse


class GUI:

    root = Tk()
    key = StringVar()
    strkey = StringVar()
    movetimeFrom = StringVar(root, "2.0")
    movetimeTo = StringVar(root, "5.0")
    clicktimeFrom = StringVar(root, "0.0")
    clicktimeTo = StringVar(root,  "5.0")
    radius = StringVar(root, "5")
    angle = StringVar(root, "360")
    timeout = StringVar(root, "2.0")
    applist = []
    buttonAppList = []
    modelist = 'easeInQuad easeOutQuad easeInOutQuad easeOutQuart easeInOutQuart easeInQuad easeInBack'
    recording_instance = None
    current_preset = "Normal"  # Default preset
    appendMode = IntVar(root, 0)  # Keep for compatibility

    def __init__(self):
        try:
            self.root.title("Autoclicker")
            self.icon = PhotoImage(file="icon.ico")
            self.root.iconphoto(True, self.icon)
        except Exception as e:
            print(f"Warning: Could not load icon: {e}")
            self.root.title("Autoclicker")

        # Apple-inspired dark theme styling
        self.root.configure(bg='#1a1a1a')
        self.style = ttk.Style()
        self.style.configure('TLabel', background='#1a1a1a', foreground='#ffffff', font=('Helvetica', 12))
        self.style.configure('TEntry', fieldbackground='#333333', borderwidth=0, relief='flat', font=('Helvetica', 12))
        self.style.configure('TButton', background='#333333', foreground='#ffffff', borderwidth=0, relief='flat', font=('Helvetica', 12, 'bold'))
        self.style.map('TButton', background=[('active', '#555555')])

        # Custom button styling for large buttons
        large_button_style = {
            'bg': '#333333',
            'fg': '#ffffff',
            'activebackground': '#555555',
            'activeforeground': '#ffffff',
            'bd': 0,
            'relief': 'flat',
            'font': ('Helvetica', 16, 'bold'),
            'padx': 30,
            'pady': 20,
            'highlightthickness': 0,
            'width': 20
        }

        preset_button_style = {
            'bg': '#444444',
            'fg': '#ffffff',
            'activebackground': '#666666',
            'activeforeground': '#ffffff',
            'bd': 0,
            'relief': 'flat',
            'font': ('Helvetica', 12, 'bold'),
            'padx': 15,
            'pady': 10,
            'highlightthickness': 0
        }

        label_style = {
            'bg': '#1a1a1a',
            'fg': '#ffffff',
            'font': ('Helvetica', 16, 'bold')
        }

        entry_style = {
            'bg': '#333333',
            'fg': '#ffffff',
            'insertbackground': '#ffffff',
            'bd': 0,
            'relief': 'flat',
            'font': ('Helvetica', 12),
            'highlightthickness': 0
        }

        self.labelMain = Label(self.root, text="Auto Clicker", height=0, **label_style)
        self.labelMoveTime = Label(self.root, text="Move time:", **label_style)
        self.labelClickTime = Label(self.root, text="Click time:", **label_style)
        self.labelTo1 = Label(self.root, text="To:", **label_style)
        self.labelTo2 = Label(self.root, text="To:", **label_style)
        self.labelFrom1 = Label(self.root, text="From:", **label_style)
        self.labelFrom2 = Label(self.root, text="From:", **label_style)
        self.labelRadius = Label(self.root, text="Radius", **label_style)
        self.labelAngle = Label(self.root, text="Angle:", **label_style)
        self.labelTimeout = Label(self.root, text="Timeout:", **label_style)

        self.entryMoveTimeFrom = Entry(self.root, textvariable=self.movetimeFrom, validate="key", validatecommand=(self.root.register(self.validate_float), '%P'), **entry_style)
        self.entryMoveTimeTo = Entry(self.root, textvariable=self.movetimeTo, validate="key", validatecommand=(self.root.register(self.validate_float), '%P'), **entry_style)
        self.entryClickTimeFrom = Entry(self.root, textvariable=self.clicktimeFrom, validate="key", validatecommand=(self.root.register(self.validate_float), '%P'), **entry_style)
        self.entryClickTimeTo = Entry(self.root, textvariable=self.clicktimeTo, validate="key", validatecommand=(self.root.register(self.validate_float), '%P'), **entry_style)
        self.entryRadius = Entry(self.root, textvariable=self.radius, validate="key", validatecommand=(self.root.register(self.validate_int), '%P'), **entry_style)
        self.entryAngle = Entry(self.root, textvariable=self.angle, validate="key", validatecommand=(self.root.register(self.validate_int), '%P'), **entry_style)

        self.entryKey = Entry(self.root, textvariable=self.key, width=30, state=DISABLED, **entry_style)
        self.entryTimeout = Entry(self.root, textvariable=self.timeout, validate="key", validatecommand=(self.root.register(self.validate_float), '%P'), **entry_style)

        # Section labels
        self.labelRecording = Label(self.root, text="Recording", **label_style)
        self.labelPlayback = Label(self.root, text="Playback", **label_style)
        self.labelSettings = Label(self.root, text="Settings", **label_style)

        # Recording section buttons
        self.buttonKey = Button(self.root, text="Select Key", command=self.set_key, **large_button_style)
        self.buttonStart = Button(self.root, text="Start Recording", command=self.create_window, state=DISABLED, **large_button_style)
        self.buttonSave = Button(self.root, text="Save Recording", command=self.save_recording, state=DISABLED, **large_button_style)
        self.buttonLoad = Button(self.root, text="Load Recording", command=self.load_recording, **large_button_style)

        # Playback section button
        self.buttonPlayback = Button(self.root, text="Start Playback", command=self.start_playback, state=DISABLED, **large_button_style)

        # Settings section buttons
        self.buttonFast = Button(self.root, text="Fast", command=lambda: self.set_preset("Fast"), **preset_button_style)
        self.buttonNormal = Button(self.root, text="Normal", command=lambda: self.set_preset("Normal"), **preset_button_style)
        self.buttonSlow = Button(self.root, text="Slow", command=lambda: self.set_preset("Slow"), **preset_button_style)

        # Key display
        self.entryKey = Entry(self.root, textvariable=self.key, width=20, state=DISABLED, bg='#333333', fg='#ffffff', insertbackground='#ffffff', bd=0, relief='flat', font=('Helvetica', 14), highlightthickness=0)

        # Add hover effects
        self.add_hover_effect(self.buttonKey)
        self.add_hover_effect(self.buttonStart)
        self.add_hover_effect(self.buttonSave)
        self.add_hover_effect(self.buttonLoad)
        self.add_hover_effect(self.buttonPlayback)
        self.add_hover_effect(self.buttonFast)
        self.add_hover_effect(self.buttonNormal)
        self.add_hover_effect(self.buttonSlow)

    def add_hover_effect(self, button):
        def on_enter(e):
            button.config(bg='#555555')
        def on_leave(e):
            button.config(bg='#333333')
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)

        self.set_new_grid()
        self.set_preset("Normal")  # Set default preset

        self.read_config_values()

        self.root.mainloop()

    def set_new_grid(self):
        # New simplified layout with three sections
        # Recording section
        self.labelRecording.grid(row=0, column=0, columnspan=2, pady=(20, 10))
        self.buttonKey.grid(row=1, column=0, padx=10, pady=5)
        self.entryKey.grid(row=1, column=1, padx=10, pady=5)
        self.buttonStart.grid(row=2, column=0, columnspan=2, padx=10, pady=5)
        self.buttonSave.grid(row=3, column=0, padx=10, pady=5)
        self.buttonLoad.grid(row=3, column=1, padx=10, pady=5)

        # Playback section
        self.labelPlayback.grid(row=4, column=0, columnspan=2, pady=(20, 10))
        self.buttonPlayback.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

        # Settings section
        self.labelSettings.grid(row=6, column=0, columnspan=2, pady=(20, 10))
        self.buttonFast.grid(row=7, column=0, padx=10, pady=5)
        self.buttonNormal.grid(row=7, column=1, padx=10, pady=5)
        self.buttonSlow.grid(row=8, column=0, columnspan=2, padx=10, pady=5)

        # Advanced settings inputs
        self.labelAdvanced = Label(self.root, text="Advanced Settings", bg='#1a1a1a', fg='#ffffff', font=('Helvetica', 16, 'bold'))
        self.labelAdvanced.grid(row=9, column=0, columnspan=2, pady=(20, 10))

        # Move time range
        self.labelMoveTime.grid(row=10, column=0, padx=10, pady=5, sticky=W)
        self.entryMoveTimeFrom.grid(row=10, column=1, padx=10, pady=5)
        self.labelTo1.grid(row=11, column=0, padx=10, pady=5, sticky=W)
        self.entryMoveTimeTo.grid(row=11, column=1, padx=10, pady=5)

        # Click time range
        self.labelClickTime.grid(row=12, column=0, padx=10, pady=5, sticky=W)
        self.entryClickTimeFrom.grid(row=12, column=1, padx=10, pady=5)
        self.labelTo2.grid(row=13, column=0, padx=10, pady=5, sticky=W)
        self.entryClickTimeTo.grid(row=13, column=1, padx=10, pady=5)

        # Radius and Angle
        self.labelRadius.grid(row=14, column=0, padx=10, pady=5, sticky=W)
        self.entryRadius.grid(row=14, column=1, padx=10, pady=5)
        self.labelAngle.grid(row=15, column=0, padx=10, pady=5, sticky=W)
        self.entryAngle.grid(row=15, column=1, padx=10, pady=5)

        # Timeout
        self.labelTimeout.grid(row=16, column=0, padx=10, pady=5, sticky=W)
        self.entryTimeout.grid(row=16, column=1, padx=10, pady=5)

        # Easing modes checkboxes
        self.labelEasing = Label(self.root, text="Easing Modes:", bg='#1a1a1a', fg='#ffffff', font=('Helvetica', 16, 'bold'))
        self.labelEasing.grid(row=17, column=0, columnspan=2, pady=(20, 10))

        # Create checkboxes for easing modes
        self.easing_vars = {}
        easing_modes = ['easeInQuad', 'easeOutQuad', 'easeInOutQuad', 'easeOutQuart', 'easeInOutQuart', 'easeInQuad', 'easeInBack']
        for i, mode in enumerate(easing_modes):
            var = IntVar()
            self.easing_vars[mode] = var
            cb = Checkbutton(self.root, text=mode, variable=var, bg='#1a1a1a', fg='#ffffff', selectcolor='#333333', font=('Helvetica', 12), command=self.update_modelist)
            cb.grid(row=18 + i//2, column=i%2, padx=10, pady=2, sticky=W)

        # Initialize checkboxes based on current modelist
        self.initialize_easing_checkboxes()

    def set_preset(self, preset):
        """Set speed preset and update button styles"""
        self.current_preset = preset

        # Reset all button backgrounds
        self.buttonFast.config(bg='#444444')
        self.buttonNormal.config(bg='#444444')
        self.buttonSlow.config(bg='#444444')

        # Highlight selected preset
        if preset == "Fast":
            self.buttonFast.config(bg='#666666')
            self.movetimeFrom.set("0.5")
            self.movetimeTo.set("1.5")
            self.clicktimeFrom.set("0.0")
            self.clicktimeTo.set("0.5")
        elif preset == "Normal":
            self.buttonNormal.config(bg='#666666')
            self.movetimeFrom.set("2.0")
            self.movetimeTo.set("5.0")
            self.clicktimeFrom.set("0.0")
            self.clicktimeTo.set("2.0")
        elif preset == "Slow":
            self.buttonSlow.config(bg='#666666')
            self.movetimeFrom.set("4.0")
            self.movetimeTo.set("8.0")
            self.clicktimeFrom.set("1.0")
            self.clicktimeTo.set("3.0")

    def update_modelist(self):
        """Update modelist string based on selected easing mode checkboxes"""
        selected_modes = [mode for mode, var in self.easing_vars.items() if var.get() == 1]
        self.modelist = ' '.join(selected_modes)
        if not self.modelist:
            self.modelist = 'easeInQuad'  # Default if none selected

    def initialize_easing_checkboxes(self):
        """Initialize easing mode checkboxes based on current modelist"""
        current_modes = self.modelist.split()
        for mode, var in self.easing_vars.items():
            var.set(1 if mode in current_modes else 0)

    def set_key(self):
        self.entryKey.configure(state=NORMAL)
        try:
            with keyboard.Listener(on_press=self.on_press) as guik:
                guik.join()
        except Exception as e:
            print(f"Error setting key: {e}")

        self.entryKey.delete(0, END)
        self.entryKey.insert(0, self.strkey)
        self.entryKey.configure(state=DISABLED)
        self.buttonStart.configure(state=NORMAL)

    # Removed parse_quad method as checkboxes are no longer used

    def on_press(self, key):
        strkey = str(key)
        if "Key." in strkey:
            strkey = strkey.replace("Key.", "")
        else:
            strkey = strkey.replace("'", "")
        self.strkey = strkey
        self.key = key
        return False

    def create_window(self):
        print("DEBUG: Creating window list")
        self.applist = []
        self.windowList = Toplevel(self.root)
        self.windowList.title("Select program")
        self.windowList.configure(bg='#1a1a1a')
        # Force update to ensure window is ready
        self.windowList.update_idletasks()
        # Call render_list immediately instead of scheduling
        self.render_list()


    def read_config_values(self):
        try:
            cp = ConfigParse()
            if cp.check_config():
                cp.read_config()
                self.movetimeFrom.set(cp.MouseOptions['startmove'])
                self.movetimeTo.set(cp.MouseOptions['endmove'])
                self.clicktimeFrom.set(cp.MouseOptions['startclick'])
                self.clicktimeTo.set(cp.MouseOptions['endclick'])
                self.radius.set(cp.MouseOptions['radius'])
                self.angle.set(cp.MouseOptions['angle'])
                self.timeout.set(cp.MouseOptions['timeout'])
                # Load easing modes if available
                if hasattr(cp, 'easing_modes'):
                    self.modelist = cp.easing_modes
                # Set preset based on loaded values
                if float(cp.MouseOptions['startmove']) < 1.0:
                    self.set_preset("Fast")
                elif float(cp.MouseOptions['startmove']) > 3.0:
                    self.set_preset("Slow")
                else:
                    self.set_preset("Normal")
            else:
                mb.showwarning("No config file detected", "There is no config file it will be created")
                cp.write_config(self.modelist, self.key, self.movetimeFrom.get(), self.movetimeTo.get(), self.clicktimeFrom.get(), self.clicktimeTo.get(), self.radius.get(), self.angle.get(), self.timeout.get())
                cp.write_easing_modes(self.modelist)
        except Exception as e:
            print(f"Error reading config: {e}")
            mb.showerror("Config Error", f"Failed to read configuration: {e}")

    def render_list(self):
        print("DEBUG: Rendering list")
        self.app_list()
        print(f"DEBUG: Applist: {self.applist}")
        for i, v in enumerate(self.applist):
            button = Button(self.windowList, text=v, width=30, bg='#333333', fg='#ffffff', activebackground='#555555', activeforeground='#ffffff', bd=0, relief='flat', font=('Helvetica', 12), padx=10, pady=5, command=lambda app=v: self.select_app(app))
            button.pack(pady=2)
            self.add_hover_effect(button)
            self.buttonAppList.append(button)

        # Add a manual entry option for Linux users
        if self.applist and "Default Window" in self.applist[0]:
            print("DEBUG: Adding manual entry for Linux")
            try:
                manual_label = Label(self.windowList, text="Or enter window title manually:", bg='#1a1a1a', fg='#ffffff', font=('Helvetica', 12))
                manual_label.pack(pady=(10, 5))
                self.manual_entry = Entry(self.windowList, bg='#333333', fg='#ffffff', insertbackground='#ffffff', bd=0, relief='flat', font=('Helvetica', 12), width=30)
                self.manual_entry.pack(pady=5)
                manual_button = Button(self.windowList, text="Use Manual Entry", bg='#333333', fg='#ffffff', activebackground='#555555', activeforeground='#ffffff', bd=0, relief='flat', font=('Helvetica', 12), padx=10, pady=5, command=self.use_manual_entry)
                manual_button.pack(pady=5)
                self.add_hover_effect(manual_button)
            except Exception as e:
                print(f"DEBUG: Error creating manual entry widgets: {e}")

    def select_app(self, app):
        # Cross-platform window activation - simplified for compatibility
        # Window activation may not work on all platforms
        try:
            # Try to use pygetwindow if available (fallback)
            import pygetwindow as gw
            win = gw.getWindowsWithTitle(app)[0]
            win.activate()
        except (ImportError, IndexError, NotImplementedError):
            # If pygetwindow not available, not supported, or window not found, just proceed
            pass
        self.windowList.destroy()
        self.start()

    def use_manual_entry(self):
        app = self.manual_entry.get().strip()
        if app:
            self.select_app(app)
        else:
            mb.showwarning("No Window Title", "Please enter a window title.")

    def start_playback(self):
        """Start playback of loaded recording"""
        if not self.recording_instance or not self.recording_instance.mousePositions:
            mb.showwarning("No Recording", "No recording loaded to play back.")
            return

        def run_playback():
            try:
                print("DEBUG: Starting playback")
                self.recording_instance.ModeList = self.modelist
                self.recording_instance.key = self.key
                self.recording_instance.angle = self.angle.get()
                self.recording_instance.start = self.movetimeFrom.get()
                self.recording_instance.end = self.movetimeTo.get()
                self.recording_instance.startc = self.clicktimeFrom.get()
                self.recording_instance.endc = self.clicktimeTo.get()
                self.recording_instance.radius = self.radius.get()
                self.recording_instance.parse_config()
                # Enable continuous looping by default
                self.recording_instance.start_clicking(continuous=True)
                print("DEBUG: Playback completed")
            except Exception as e:
                print(f"Error during playback: {e}")
                mb.showerror("Playback Error", f"Failed to play back recording: {e}")

        # Run playback in a separate thread to prevent GUI freezing
        playback_thread = threading.Thread(target=run_playback, daemon=True)
        playback_thread.start()

    def start(self):
        def run_recording():
            try:
                print("DEBUG: Starting recording instance")
                self.recording_instance = Recording.Recording()
                self.recording_instance.ModeList = self.modelist
                self.recording_instance.key = self.key
                self.recording_instance.angle = self.angle.get()
                self.recording_instance.start = self.movetimeFrom.get()
                self.recording_instance.end = self.movetimeTo.get()
                self.recording_instance.startc = self.clicktimeFrom.get()
                self.recording_instance.endc = self.clicktimeTo.get()
                self.recording_instance.radius = self.radius.get()
                self.recording_instance.parse_config()
                print("DEBUG: About to call record()")
                self.recording_instance.record()
                print("DEBUG: Record() completed")
                # Enable save button after recording stops
                self.root.after(0, lambda: self.buttonSave.configure(state=NORMAL))
                # Enable playback button after recording
                self.root.after(0, lambda: self.buttonPlayback.configure(state=NORMAL))
            except Exception as e:
                print(f"Error starting recording: {e}")
                mb.showerror("Recording Error", f"Failed to start recording: {e}")

        # Run recording in a separate thread to prevent GUI freezing
        recording_thread = threading.Thread(target=run_recording, daemon=True)
        recording_thread.start()

    def validate_float(self, value):
        if value == "":
            return True
        try:
            float(value)
            return True
        except ValueError:
            return False

    def validate_int(self, value):
        if value == "":
            return True
        try:
            int(value)
            return True
        except ValueError:
            return False

    def save_recording(self):
        if not self.recording_instance or not self.recording_instance.mousePositions:
            mb.showwarning("No Recording", "No recording to save.")
            return
        filename = simpledialog.askstring("Save Recording", "Enter filename:")
        if filename:
            success = self.recording_instance.save_recording(filename)
            if success:
                mb.showinfo("Save Successful", f"Recording saved as {filename}.json")
            else:
                mb.showerror("Save Failed", "Failed to save recording.")

    def load_recording(self):
        filename = simpledialog.askstring("Load Recording", "Enter filename:")
        if filename:
            if not self.recording_instance:
                self.recording_instance = Recording.Recording()
            success = self.recording_instance.load_recording(filename)
            if success:
                mb.showinfo("Load Successful", f"Recording loaded from {filename}.json")
                self.buttonSave.configure(state=NORMAL)
                self.buttonPlayback.configure(state=NORMAL)
            else:
                mb.showerror("Load Failed", f"Failed to load recording {filename}.json")

    def app_list(self):
        os_name = platform.system().lower()

        if os_name == "windows":
            self._get_windows_windows()
        elif os_name == "linux":
            self._get_linux_windows()
        else:
            # Fallback for other OS
            self.applist = ["Default Window - Window selection not supported on this platform"]

        # Ensure we have at least one option
        if not self.applist:
            self.applist = ["Default Window - No windows found"]

    def _get_windows_windows(self):
        try:
            # Try to use pygetwindow for window listing
            import pygetwindow as gw
            titles = gw.getAllTitles()
            if titles:
                for window in titles:
                    if window and window.strip():
                        self.applist.append(window.strip())
            else:
                # If getAllTitles returns empty, try alternative method
                try:
                    windows = gw.getAllWindows()
                    for window in windows:
                        title = window.title
                        if title and title.strip():
                            self.applist.append(title.strip())
                except Exception as e2:
                    print(f"Error with getAllWindows fallback: {e2}")
                    self.applist = ["Default Window - Window enumeration failed"]
        except (ImportError, NotImplementedError):
            self.applist = ["Default Window - pygetwindow not available"]
        except Exception as e:
            self.applist = ["Default Window"]
            print(f"Error getting Windows window list: {e}")

    def _get_linux_windows(self):
        # Try wmctrl first, then xdotool as fallback
        if self._try_wmctrl():
            return
        if self._try_xdotool():
            return
        # If both fail, provide manual entry option
        self.applist = ["Default Window - Window selection not available on this platform"]

    def _try_wmctrl(self):
        try:
            result = subprocess.run(['wmctrl', '-l'], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                for line in lines:
                    if line.strip():
                        # wmctrl output format: <window_id> <desktop> <client_machine> <window_title>
                        parts = line.split(None, 3)  # Split on whitespace, max 4 parts
                        if len(parts) >= 4:
                            title = parts[3].strip()
                            if title:
                                self.applist.append(title)
                return True
        except (subprocess.TimeoutExpired, subprocess.CalledProcessError, FileNotFoundError):
            return False
        return False

    def _try_xdotool(self):
        try:
            result = subprocess.run(['xdotool', 'search', '--name', '.*'], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                window_ids = result.stdout.strip().split('\n')
                for wid in window_ids:
                    if wid.strip():
                        # Get window name for each ID
                        name_result = subprocess.run(['xdotool', 'getwindowname', wid], capture_output=True, text=True, timeout=2)
                        if name_result.returncode == 0:
                            title = name_result.stdout.strip()
                            if title:
                                self.applist.append(title)
                return True
        except (subprocess.TimeoutExpired, subprocess.CalledProcessError, FileNotFoundError):
            return False
        return False