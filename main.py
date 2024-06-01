import tkinter as tk

import threading
from collections import namedtuple

from src.gesture import Gesture
from src.input_controller import pause_play, mouse_position, mouse_press, mouse_release, mouse_left_click
from src.utils import timestamp, ease_in_out_quad, move_point, draw_hand

import win32gui
import win32con

is_paused = False
last_time = timestamp()

detect_hand = False
is_hand_mouse = True
is_cliqued = False
thumb_sensitivity = 1

HAND = {
    'WRIST': 0,
    'THUMB_CMC': 1,
    'THUMB_MCP': 2,
    'THUMB_IP': 3,
    'THUMB_TIP': 4,
    'INDEX_FINGER_MCP': 5,
    'INDEX_FINGER_PIP': 6,
    'INDEX_FINGER_DIP': 7,
    'INDEX_FINGER_TIP': 8,
    'MIDDLE_FINGER_MCP': 9,
    'MIDDLE_FINGER_PIP': 10,
    'MIDDLE_FINGER_DIP': 11,
    'MIDDLE_FINGER_TIP': 12,
    'RING_FINGER_MCP': 13,
    'RING_FINGER_PIP': 14,
    'RING_FINGER_DIP': 15,
    'RING_FINGER_TIP': 16,
    'PINKY_MCP': 17,
    'PINKY_PIP': 18,
    'PINKY_DIP': 19,
    'PINKY_TIP': 20
}


def setClickthrough(hwnd):
    print("setting window properties")
    try:
        styles = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
        styles = win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT
        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, styles)
        win32gui.SetLayeredWindowAttributes(hwnd, 0, 255, win32con.LWA_ALPHA)
    except Exception as e:
        print(e)


def create_window():
    # Create main window
    root = tk.Tk()
    root.geometry('2560x1080+0+0')  # You can change the size of the window if needed
    # Hide the root window drag bar and close button
    root.overrideredirect(True)
    # Make the root window always on top
    root.wm_attributes("-topmost", True)
    alpha = 0.3
    root.attributes("-alpha", alpha)
    root.wm_attributes("-alpha", alpha)
    root.wm_attributes("-transparentcolor", "black")
    # Set the root window background color to a transparent color

    root.configure(bg='')

    # Create a canvas to draw the square
    canvas = tk.Canvas(root, bd=0, highlightthickness=0)
    canvas.pack(fill=tk.BOTH, expand=True)

    setClickthrough(canvas.winfo_id())

    # Calculate coordinates for square in the center
    side_length = 30  # Change this to desired side length of your square
    x1 = (root.winfo_width() - side_length) / 2
    y1 = (root.winfo_height() - side_length) / 2
    x2, y2 = x1 + side_length, y1 + side_length

    # Draw the red square on canvas
    square = canvas.create_rectangle(x1, y1, x2, y2, fill='red', outline='red')

    return root, canvas, square


if __name__ == '__main__':
    root, canvas, square = create_window()
    Point = namedtuple('Point', ['x', 'y'])
    screen_hand = {}
    duration = 12
    move_space_width = 2000
    move_space_height = 900


    def set_square_color(color):
        canvas.itemconfig(square, fill=color, outline=color)


    def do_on_gesture(result):
        try:
            global is_paused, last_time, is_hand_mouse, is_cliqued, screen_hand
            canvas.delete("all")
            velocity = timestamp() - last_time
            last_time = timestamp()

            set_square_color("green")

            gesture = result.gestures[0][0].category_name
            print(gesture)

            hand = result.hand_landmarks[0]
            # thumb = hand[HAND["THUMB_TIP"]]
            # index = hand[HAND["INDEX_FINGER_TIP"]]

            avg_x = 0
            avg_y = 0
            for key, value in HAND.items():
                new_point = Point(
                    (1 - hand[value].x - 0.2) * (2560 / (0.8 - 0.2)),
                    (hand[value].y - 0.2) * (1080 / (0.8 - 0.2))
                )
                try:
                    point = move_point(
                        screen_hand[key],
                        new_point,
                        duration,
                        velocity / duration,
                        ease_in_out_quad
                    )
                    screen_hand[key] = Point(point[0], point[1])
                except Exception as e:
                    screen_hand[key] = new_point
                avg_x += new_point.x
                avg_y += new_point.y
            avg_x /= len(HAND)
            avg_y /= len(HAND)

            # Draw a square at the center of the hand
            # canvas.create_rectangle(avg_x - 5, avg_y - 5, avg_x + 5, avg_y + 5, fill="red")

            draw_hand(screen_hand, canvas)
            mouse_position(screen_hand["WRIST"].x, screen_hand["WRIST"].y - 400)

            if gesture == "Closed_Fist" and not is_cliqued:
                is_cliqued = True
                mouse_left_click()
            elif gesture != "Closed_Fist":
                is_cliqued = False
            # print(screen_hand[0].x)

            # if abs(thumb.x - index.x) < 0.007 and abs(thumb.y - index.y) < 0.05:
            #     is_released = False
            #     mouse_press()
            #     print("Pressed")
            # elif not is_released:
            #     is_released = True
            #     mouse_release()
            #     print("Released")
            # hand_x = (1 - thumb.x) * 2560 * thumb_sensitivity
            # hand_y = thumb.y * 1080 * thumb_sensitivity
            # if is_hand_mouse:
            #     mouse_position(hand_x, hand_y)

            # for part, (x, y) in screen_hand.items():
            #     canvas.create_line(x, y, x + 3, y + 3, fill="green")

            # current_time = timestamp()
            # print(f"Gesture: {gesture} | Time: {current_time - last_time}")
            # if gesture in ["Closed_Fist"] and current_time - last_time >= 1000:
            #     pause_play()
            #     last_time = current_time
            # if gesture in ["Closed_Fist"] and current_time - last_time >= 1000:
            #     is_hand_mouse = not is_hand_mouse
            #     last_time = current_time
        except Exception as e:
            print(e)


    def do_on_nothing():
        set_square_color("red")


    gesture = Gesture(
        "resources/gesture_recognizer.task ",
        do_on_gesture,
        do_on_nothing
    )
    threading.Thread(target=gesture.recognition).start()

    root.mainloop()
