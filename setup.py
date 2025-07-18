from distutils.core import setup
import py2exe

import pynput.mouse
import sys
from inc import Clicker
from pynput import mouse
from pynput import keyboard
from pynput.keyboard import Key
import pyautogui
import random
from inc import Recording

setup(console=['main.py'])