from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import json
import time
import os


class GUIConsole(Toplevel):
    _instance = None
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

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self, *args, **kwargs):
        if GUIConsole._instance is not None:
            print("DEBUG: GUIConsole singleton already exists, returning existing instance")
            return GUIConsole._instance
        print("DEBUG: Creating new GUIConsole instance")
        GUIConsole._instance = self
        Toplevel.__init__(self, *args, **kwargs)
        self.wm_title("Autoclicker")
        self.geometry("620x480")
        # Icon loading removed for cross-platform compatibility

        # Apple-inspired dark theme
        self.configure(bg='#1a1a1a')
        self.s = ttk.Style()
        self.s.configure('Treeview', background='#333333', foreground='#ffffff', fieldbackground='#333333', borderwidth=0, font=('Helvetica', 12))
        self.s.configure('Treeview.Heading', background='#1a1a1a', foreground='#ffffff', font=('Helvetica', 12, 'bold'))
        self.s.map('Treeview', background=[('selected', '#555555')])

        self.renderTreeView()

        # Create button frame
        self.button_frame = Frame(self, bg='#1a1a1a')
        self.button_frame.pack(side='bottom', fill='x', pady=10)

        # Import Recording button
        self.ButtonImport = Button(self.button_frame, text="Import Recording", bg='#333333', fg='#ffffff', activebackground='#555555', activeforeground='#ffffff', bd=0, relief='flat', font=('Helvetica', 12, 'bold'), padx=20, pady=10, command=self.import_recording)
        self.ButtonImport.pack(side='left', padx=10)

        # Export Recording button (renamed from Dump)
        self.ButtonExport = Button(self.button_frame, text="Export Recording", bg='#333333', fg='#ffffff', activebackground='#555555', activeforeground='#ffffff', bd=0, relief='flat', font=('Helvetica', 12, 'bold'), padx=20, pady=10, command=self.export_recording)

        # Add hover effects
        def on_enter_import(e):
            self.ButtonImport.config(bg='#555555')
        def on_leave_import(e):
            self.ButtonImport.config(bg='#333333')
        self.ButtonImport.bind("<Enter>", on_enter_import)
        self.ButtonImport.bind("<Leave>", on_leave_import)

        def on_enter_export(e):
            self.ButtonExport.config(bg='#555555')
        def on_leave_export(e):
            self.ButtonExport.config(bg='#333333')
        self.ButtonExport.bind("<Enter>", on_enter_export)
        self.ButtonExport.bind("<Leave>", on_leave_export)

        self.attributes('-topmost', True)
        self.ConsoleTable.pack(fill=BOTH, expand=True, side='right')
        self.ButtonExport.pack(side='right', padx=10)
        self.scroll = ttk.Scrollbar(self, orient='vertical', command=self.ConsoleTable.yview)
        self.scroll.pack(side="right", fill="y")
        self.ConsoleTable.configure(yscrollcommand=self.scroll.set)
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def renderTreeView(self):
        self.s.configure('Treeview', rowheight=40, colwidth=40)
        self.ConsoleTable = ttk.Treeview(self)
        self.ConsoleTable['columns'] = ('x', 'y', 'm_interval', 'c_interval')
        self.ConsoleTable.column('#0', width=0, stretch=False)
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

    def import_recording(self):
        """Import recording from JSON file and populate the table."""
        try:
            filename = filedialog.askopenfilename(
                title="Select Recording File",
                filetypes=[("JSON files", "*.json")],
                initialdir="recordings"
            )
            if not filename:
                return

            with open(filename, 'r') as f:
                data = json.load(f)

            mouse_positions = data.get('mousePositions', [])
            if not mouse_positions:
                print("No mouse positions found in the file.")
                return

            # Clear existing table data
            for item in self.ConsoleTable.get_children():
                self.ConsoleTable.delete(item)

            # Clear lists
            self.x = []
            self.y = []
            self.c_interval = []
            self.m_interval = []

            # Populate table with mouse positions
            # Assuming mousePositions is list of [x, y] pairs
            for i, pos in enumerate(mouse_positions):
                if len(pos) >= 2:
                    x, y = pos[0], pos[1]
                    # For intervals, we might need to calculate or use defaults
                    # Since the original dump was x,y,ci,mi, and ci was pressed (bool), mi was elapsed_time
                    # For import, we'll use 0 for intervals if not available
                    c_interval = 0  # Default click interval
                    m_interval = 0  # Default move interval

                    self.insert_column(x, y, c_interval, m_interval)

            print(f"Imported {len(mouse_positions)} positions from {filename}")

        except Exception as e:
            print(f"Error importing recording: {e}")

    def export_recording(self):
        """Export table data to JSON recording file."""
        try:
            # Collect data from table
            mouse_positions = []
            for item in self.ConsoleTable.get_children():
                values = self.ConsoleTable.item(item)['values']
                if len(values) >= 2:
                    x, y = values[0], values[1]
                    mouse_positions.append([x, y])

            if not mouse_positions:
                print("No data to export.")
                return

            # Create data structure similar to Recording.save_recording
            data = {
                'mousePositions': mouse_positions,
                'timestamp': time.time(),
                'config': {
                    'modeList': self.ModeList,
                    'angle': self.angle,
                    'start': self.start,
                    'end': self.end,
                    'startc': self.startc,
                    'endc': self.endc,
                    'radius': self.radius,
                    'timeout': 2  # Default timeout
                }
            }

            # Ask for filename
            filename = filedialog.asksaveasfilename(
                title="Save Recording",
                defaultextension=".json",
                filetypes=[("JSON files", "*.json")],
                initialdir="recordings"
            )
            if not filename:
                return

            # Ensure recordings directory exists
            os.makedirs('recordings', exist_ok=True)

            with open(filename, 'w') as f:
                json.dump(data, f, indent=4)

            print(f"Recording exported to {filename}")

        except Exception as e:
            print(f"Error exporting recording: {e}")

    def on_close(self):
        GUIConsole._instance = None
        self.destroy()


if __name__ == '__main__':
    g = GUIConsole()
    g.mainloop()
