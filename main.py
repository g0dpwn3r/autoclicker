import os
import sys

from inc.GUI import GUI

def main():
    try:
        g = GUI()
        g.root.protocol("WM_DELETE_WINDOW", on_close)
        g.root.mainloop()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

def on_close():
    print("Application closing...")
    sys.exit(0)

if __name__ == '__main__':
    main()
    