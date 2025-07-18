# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import os

from inc import GUI
from inc import Clicker

def main():
    g = GUI()
    g.mainloop()
    g.protocol("WM_DELETE_WINDOW", os._exit(0))

def on_close():
    Clicker.recording = False
    os._exit(0)

if __name__ == '__main__':
    main()



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
