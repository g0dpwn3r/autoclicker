from tkinter import *
from tkinter import messagebox as mb
from pynput import keyboard
import pygetwindow as gw

from inc import Recording
from inc import ConfigParse


class GUI:

    root = Tk()
    key = StringVar()
    strkey = StringVar()
    movetimeFrom = StringVar(root, "2.0")
    movetimeTo = StringVar(root, "5.0")
    clicktimeFrom = StringVar(root, "0.0")
    clicktimeTo = StringVar(root, "5.0")
    radius = StringVar(root, "5")
    angle = StringVar(root, "360")
    timeout = StringVar(root, "2.0")
    applist = []
    buttonAppList = []
    checkboxes = []
    labelCheckboxes = []
    checkboxesBool = [IntVar(root, 1), IntVar(root, 1), IntVar(root, 1), IntVar(root, 1), IntVar(root, 1), IntVar(root, 1), IntVar(root, 1)]
    applistText = []
    modelist = ['easeInQuad', 'easeOutQuad', 'easeInOutQuad', 'easeOutQuart', 'easeInOutQuart', 'easeInQuad', 'easeInBack']
    modeString = ""
    configModeList = []

    def __init__(self):
        self.root.title("Autoclicker")
        self.icon = PhotoImage(file="icon.ico")
        self.root.iconphoto(True, self.icon)

        self.labelMain = Label(self.root, text="Auto Clicker", height=0)
        self.labelMoveTime = Label(self.root, text="Move time:")
        self.labelClickTime = Label(self.root, text="Click time:")
        self.labelTo1 = Label(self.root, text="To:")
        self.labelTo2 = Label(self.root, text="To:")
        self.labelFrom1 = Label(self.root, text="From:")
        self.labelFrom2 = Label(self.root, text="From:")
        self.labelRadius = Label(self.root, text="Radius")
        self.labelAngle = Label(self.root, text="Angle:")
        self.labelTimeout = Label(self.root, text="Timeout:")

        self.entryMoveTimeFrom = Entry(self.root, textvariable=self.movetimeFrom)
        self.entryMoveTimeTo = Entry(self.root, textvariable=self.movetimeTo)
        self.entryClickTimeFrom = Entry(self.root, textvariable=self.clicktimeFrom)
        self.entryClickTimeTo = Entry(self.root, textvariable=self.clicktimeTo)
        self.entryRadius = Entry(self.root, textvariable=self.radius)
        self.entryAngle = Entry(self.root, textvariable=self.angle)

        self.entryKey = Entry(self.root, textvariable=self.key, width=30, state=DISABLED)
        self.entryTimeout = Entry(self.root, textvariable=self.timeout)

        self.buttonKey = Button(self.root, text="Select key:", command=self.set_key, width=80)
        self.buttonStart = Button(self.root, text="Start Recording", command=self.create_window, width=80, state=DISABLED)

        self.set_grid()
        self.render_checkbox()

        self.read_config_values()

        self.root.mainloop()

    def set_grid(self):
        self.labelMain.grid(row=0, column=1, columnspan=5)
        self.labelMoveTime.grid(row=1, column=1, columnspan=3)
        self.labelFrom1.grid(row=2, column=0)
        self.entryMoveTimeFrom.grid(row=2, column=1)
        self.labelTo1.grid(row=2, column=2)
        self.entryMoveTimeTo.grid(row=2, column=3)
        self.labelRadius.grid(row=2, column=4)
        self.entryRadius.grid(row=2, column=5)
        self.labelClickTime.grid(row=3, column=1, columnspan=3)
        self.labelFrom2.grid(row=4, column=0)
        self.entryClickTimeFrom.grid(row=4, column=1)
        self.labelTo2.grid(row=4, column=2)
        self.entryClickTimeTo.grid(row=4, column=3)
        self.labelAngle.grid(row=4, column=4)
        self.entryAngle.grid(row=4, column=5)
        self.entryKey.grid(row=5, column=2, columnspan=3)
        self.buttonKey.grid(row=6, column=1, columnspan=5)
        self.labelTimeout.grid(row=6, column=7)
        self.buttonStart.grid(row=7, column=1, columnspan=5, rowspan=2)
        self.entryTimeout.grid(row=7, column=7, padx=30, pady=10)

    def render_checkbox(self):
        i = 0
        for c in self.modelist:
            self.labelCheckboxes.append(Label(self.root, text=c, padx=30).grid(row=i, column=7))
            self.checkboxes.append(Checkbutton(self.root, variable=self.checkboxesBool[i], offvalue=0, onvalue=1, padx=5).grid(row=i, column=8))
            i += 1

    def set_key(self):
        self.entryKey.configure(state=NORMAL)
        with keyboard.Listener(on_press=self.on_press) as guik:
            guik.join()

        guik.stop()
        self.entryKey.delete(0, END)
        self.entryKey.insert(0, self.strkey)
        self.entryKey.configure(state=DISABLED)
        self.buttonStart.configure(state=NORMAL)

    def parse_quad(self):
        for i, v in enumerate(self.checkboxesBool):
            if not v.get():
                self.checkboxesBool.pop(i)
                self.modelist.pop(i)

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
        self.parse_quad()
        self.applist = []
        self.windowList = Toplevel()
        self.windowList.title = "Select program"
        self.render_list()


    def read_config_values(self):
        cp = ConfigParse()
        if cp.check_config():
            cp.read_config()
            self.configModeList = cp.ModeListString.split()
            self.movetimeFrom = cp.MouseOptions['startmove']
            self.movetimeTo = cp.MouseOptions['endmove']
            self.clicktimeFrom = cp.MouseOptions['startclick']
            self.clicktimeTo = cp.MouseOptions['endclick']
            self.radius = cp.MouseOptions['radius']
            self.angle = cp.MouseOptions['angle']
            self.timeout = cp.MouseOptions['timeout']
            self.get_checkboxe()
        else:
            mb.showwarning("No config file detected", "There is no config file it will be created")
            self.convert_mode()
            cp.write_config(self.modeString, self.key, self.movetimeFrom.get(), self.movetimeTo.get(), self.clicktimeFrom.get(), self.clicktimeTo.get(), self.radius.get(), self.angle.get(), self.timeout.get())

    def convert_mode(self):
        for m in self.modelist:
            self.modeString += " " + m

        print(self.modeString)

    def get_checkboxe(self):
        for i, v in enumerate(self.modelist):
            if v not in self.configModeList:
                self.checkboxesBool[i] = 0

    def render_list(self):
        self.app_list()
        for i, v in enumerate(self.applist):
            self.buttonAppList.append(Button(self.windowList, text=v, width=30, command=lambda: self.select_app(v)).pack())

    def select_app(self, app):
        win = gw.getWindowsWithTitle(app)[0]
        win.activate()
        self.windowList.destroy()
        self.start()

    def start(self):
        r = Recording.Recording()
        r.ModeList = ' '.join(self.modelist)
        r.key = self.key
        r.angle = self.angle
        r.start = self.movetimeFrom
        r.end = self.movetimeTo
        r.startc = self.clicktimeFrom
        r.endc = self.clicktimeTo
        r.radius = self.radius
        r.parse_config()
        r.record()

    def app_list(self):
        for window in gw.getAllTitles():
            if window != "":
                self.applist.append(window)