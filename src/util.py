import os
import sys

from .variables import *

def exit_game():
    show_cursor()
    os.system("stty echo")
    print(message)
    F.close()
    
def reset_canvas():
    for y in range(CANVAS_HEIGHT):
        for x in range(CANVAS_WIDTH):
            CANVAS[y][x] = " "
    
def untrap():
    for y in [6, 24]:
        for x in range(30, 80):
            CANVAS[y][x] = " "
    for x in [30, 80]:
        for y in range(6, 25):
            CANVAS[y][x] = " "

def distance(troop, building):
    dx = 2*building.X - troop.X
    dy = building.Y - troop.Y
    
    d2 = dx**2 + dy**2
    return math.sqrt(d2)

def hide_cursor():
    if os.name == 'nt':
        ci = _CursorInfo()
        handle = ctypes.windll.kernel32.GetStdHandle(-11)
        ctypes.windll.kernel32.GetConsoleCursorInfo(handle, ctypes.byref(ci))
        ci.visible = False
        ctypes.windll.kernel32.SetConsoleCursorInfo(handle, ctypes.byref(ci))
    elif os.name == 'posix':
        sys.stdout.write("\033[?25l")
        sys.stdout.flush()

def show_cursor():
    if os.name == 'nt':
        ci = _CursorInfo()
        handle = ctypes.windll.kernel32.GetStdHandle(-11)
        ctypes.windll.kernel32.GetConsoleCursorInfo(handle, ctypes.byref(ci))
        ci.visible = True
        ctypes.windll.kernel32.SetConsoleCursorInfo(handle, ctypes.byref(ci))
    elif os.name == 'posix':
        sys.stdout.write("\033[?25h")
        sys.stdout.flush()