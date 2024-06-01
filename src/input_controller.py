from pynput.keyboard import Key, Controller
from pynput.mouse import Button, Controller as MouseController

keyboard = Controller()
mouse = MouseController()


def pause_play():
    keyboard.tap(Key.space)


def mouse_position(x, y):
    mouse.position = (x, y)


def mouse_press():
    mouse.press(Button.left)


def mouse_release():
    mouse.release(Button.left)


def mouse_right_click():
    mouse.click(Button.right, 1)


def mouse_left_click():
    mouse.click(Button.left, 1)
