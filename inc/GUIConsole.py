from tkinter import *
from tkinter import ttk
from tkinter import filedialog


class GUIConsole(Toplevel):
    key = None
    ConsoleTable = None
    x = []
    y = []
    c_interval = []
    m_interval = []
    mousePositions = []
    angle = 360
    radius = 5
    start = 0
    startc = 0
    end = 0
    endc = 0
    ModeList = 'easeInQuad easeOutQuad easeInOutQuad easeOutQuart easeInOutQuart easeInQuad easeInBack'

    def __init__(self, *args, **kwargs):
        Toplevel.__init__(self, *args, **kwargs)
        self.wm_title("Autoclicker")
        self.geometry("620x480")
        # self.icon = ImageTk.PhotoImage(file="H:/code/rs3Autoclicker/icon.ico")
        # self.wm_iconphoto(False, self.icon)
        self.s = ttk.Style()
        self.renderTreeView()
        self.ButtonDump = Button(self, text="Dump!", command=lambda: self.dump_data(self.ConsoleTable))
        self.attributes('-topmost', True)
        self.ConsoleTable.pack(fill=BOTH, expand=True, side='right')
        self.ButtonDump.pack()
        self.scroll = ttk.Scrollbar(self, orient='vertical', command=self.ConsoleTable.yview)
        self.scroll.pack(side="right", fill="x")
        self.ConsoleTable.configure(xscrollcommand=self.scroll.set)
        self.protocol("WM_DELETE_WINDOW", print("ja"))

    def renderTreeView(self):
        self.s.configure('Treeview', rowheight=40, colwidth=40)
        self.ConsoleTable = ttk.Treeview(self)
        self.ConsoleTable['columns'] = ('x', 'y', 'm_interval', 'c_interval')
        self.ConsoleTable.column('#0', width=0, stretch=0)
        self.ConsoleTable.column('x', anchor=CENTER, width=80)
        self.ConsoleTable.column('y', anchor=CENTER, width=80)
        self.ConsoleTable.column('m_interval', anchor=CENTER, width=80)
        self.ConsoleTable.column('c_interval', anchor=CENTER, width=80)
        self.ConsoleTable.heading('#0', text='#0', anchor=CENTER)
        self.ConsoleTable.heading('x', text='X:', anchor=CENTER)
        self.ConsoleTable.heading('y', text='Y:', anchor=CENTER)
        self.ConsoleTable.heading('m_interval', text='Move interval:', anchor=CENTER)
        self.ConsoleTable.heading('c_interval', text='Click interval:', anchor=CENTER)

    def insert_column(self, x, y, c_interval, m_interval):
        self.x.append(x)
        self.y.append(y)
        self.c_interval.append(c_interval)
        self.m_interval.append(m_interval)
        self.ConsoleTable.insert(parent='', index='end', text='', values=(x, y, c_interval, m_interval))

    def dump_data(self, treeview):
        data = "x,     y,     ci,  mi\n"
        for id in treeview.get_children():
            row = treeview.item(id)['values']
            data += " ".join(row) + "\n"

        print(data)
        fdlg = filedialog.asksaveasfile()
        fdlg.write(data)


# verwijder dit waneer het ui ontworpen is
if __name__ == '__main__':
    g = GUIConsole()
    g.mainloop()
