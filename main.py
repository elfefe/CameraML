import tkinter as tk

import threading

from src.gesture import Gesture
from src.input_controller import pause_play, mouse_position, mouse_press, mouse_release
from src.utils import timestamp

is_paused = False
last_time = timestamp()

detect_hand = False
is_hand_mouse = True
is_released = True
thumb_sensitivity = 1

HAND = {
    'WRIST': 0,
    'MIDDLE_FINGER_DIP': 11,
    'THUMB_CMC': 1, 'THUMB_MCP': 2,
    'MIDDLE_FINGER_TIP': 12,
    'THUMB_IP': 3,
    'RING_FINGER_MCP': 13,
    'THUMB_TIP': 4,
    'RING_FINGER_PIP': 14,
    'INDEX_FINGER_MCP': 5,
    'RING_FINGER_DIP': 15,
    'INDEX_FINGER_PIP': 6,
    'RING_FINGER_TIP': 16,
    'INDEX_FINGER_DIP': 7,
    'PINKY_MCP': 17,
    'INDEX_FINGER_TIP': 8,
    'PINKY_PIP': 18,
    'MIDDLE_FINGER_MCP': 9,
    'PINKY_DIP': 19,
    'MIDDLE_FINGER_PIP': 10,
    'PINKY_TIP': 20
}


def create_window():
    # Create main window
    root = tk.Tk()
    root.geometry('2500x1000+30+40')  # You can change the size of the window if needed
    # Hide the root window drag bar and close button
    root.overrideredirect(True)
    # Make the root window always on top
    root.wm_attributes("-topmost", True)
    root.wm_attributes("-alpha", 0.5)
    # Set the root window background color to a transparent color
    root.configure(bg='')

    # Create a canvas to draw the square
    canvas = tk.Canvas(root, bd=0, highlightthickness=0)
    canvas.pack(fill=tk.BOTH, expand=True)

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


    def draw_hand(hand, canvas):
        try:
            canvas.create_line(hand[HAND["WRIST"]].x, hand[HAND["WRIST"]].y, hand[HAND["THUMB_CMC"]].x,
                               hand[HAND["THUMB_CMC"]].y, fill="green")
            canvas.create_line(hand[HAND["THUMB_CMC"]].x, hand[HAND["THUMB_CMC"]].y, hand[HAND["THUMB_MCP"]].x,
                               hand[HAND["THUMB_MCP"]].y, fill="green")
            canvas.create_line(hand[HAND["THUMB_MCP"]].x, hand[HAND["THUMB_MCP"]].y, hand[HAND["THUMB_IP"]].x,
                               hand[HAND["THUMB_IP"]].y, fill="green")
            canvas.create_line(hand[HAND["THUMB_IP"]].x, hand[HAND["THUMB_IP"]].y, hand[HAND["THUMB_TIP"]].x,
                               hand[HAND["THUMB_TIP"]].y, fill="green")
            # canvas.create_line(hand[HAND["WRIST"]].x, hand[HAND["WRIST"]].y, hand[HAND["INDEX_FINGER_MCP"]].x,
            #                    hand[HAND["INDEX_FINGER_MCP"]].y, fill="green")
            # canvas.create_line(hand[HAND["INDEX_FINGER_MCP"]].x, hand[HAND["INDEX_FINGER_MCP"]].y,
            #                    hand[HAND["INDEX_FINGER_DIP"]].x, hand[HAND["INDEX_FINGER_DIP"]].y, fill="green")
            # canvas.create_line(hand[HAND["INDEX_FINGER_DIP"]].x, hand[HAND["INDEX_FINGER_DIP"]].y,
            #                    hand[HAND["INDEX_FINGER_TIP"]].x, hand[HAND["INDEX_FINGER_TIP"]].y, fill="green")
            # canvas.create_line(hand[HAND["WRIST"]].x, hand[HAND["WRIST"]].y, hand[HAND["MIDDLE_FINGER_MCP"]].x,
            #                    hand[HAND["MIDDLE_FINGER_MCP"]].y, fill="green")
            # canvas.create_line(hand[HAND["MIDDLE_FINGER_MCP"]].x, hand[HAND["MIDDLE_FINGER_MCP"]].y,
            #                    hand[HAND["MIDDLE_FINGER_DIP"]].x, hand[HAND["MIDDLE_FINGER_DIP"]].y, fill="green")
            # canvas.create_line(hand[HAND["MIDDLE_FINGER_DIP"]].x, hand[HAND["MIDDLE_FINGER_DIP"]].y,
            #                    hand[HAND["MIDDLE_FINGER_TIP"]].x, hand[HAND["MIDDLE_FINGER_TIP"]].y, fill="green")
            # canvas.create_line(hand[HAND["WRIST"]].x, hand[HAND["WRIST"]].y, hand[HAND["RING_FINGER_MCP"]].x,
            #                    hand[HAND["RING_FINGER_MCP"]].y, fill="green")
            # canvas.create_line(hand[HAND["RING_FINGER_MCP"]].x, hand[HAND["RING_FINGER_MCP"]].y,
            #                    hand[HAND["RING_FINGER_DIP"]].x, hand[HAND["RING_FINGER_DIP"]].y, fill="green")
            # canvas.create_line(hand[HAND["RING_FINGER_DIP"]].x, hand[HAND["RING_FINGER_DIP"]].y,
            #                    hand[HAND["RING_FINGER_TIP"]].x, hand[HAND["RING_FINGER_TIP"]].y, fill="green")
            # canvas.create_line(hand[HAND["WRIST"]].x, hand[HAND["WRIST"]].y, hand[HAND["PINKY_MCP"]].x,
            #                    hand[HAND["PINKY_MCP"]].y, fill="green")
            # canvas.create_line(hand[HAND["PINKY_MCP"]].x, hand[HAND["PINKY_MCP"]].y, hand[HAND["PINKY_DIP"]].x,
            #                    hand[HAND["PINKY_DIP"]].y, fill="green")
            # canvas.create_line(hand[HAND["PINKY_DIP"]].x, hand[HAND["PINKY_DIP"]].y, hand[HAND["PINKY_TIP"]].x,
            #                    hand[HAND["PINKY_TIP"]].y, fill="green")
        except Exception as e:
            print(e)
        return canvas


    def set_square_color(color):
        canvas.itemconfig(square, fill=color, outline=color)


    def do_on_gesture(result):
        global is_paused, last_time, is_hand_mouse, is_released
        canvas.delete("all")

        set_square_color("green")

        gesture = result.gestures[0][0].category_name
        hand = result.hand_landmarks[0]
        # thumb = hand[HAND["THUMB_TIP"]]
        # index = hand[HAND["INDEX_FINGER_TIP"]]

        screen_hand = {}
        for key, value in HAND.items():
            screen_hand[key] = (1 - hand[value].x) * 2560, hand[value].y * 1080

        # print(screen_hand)

        # if abs(thumb.x - index.x) < 0.007 and abs(thumb.y - index.y) < 0.05:
        #     is_released = False
        #     mouse_press()
        #     print("Pressed")
        # elif not is_released:
        #     is_released = True
        #     mouse_release()
        #     print("Released")

        draw_hand(screen_hand, canvas)
        # hand_x = (1 - thumb.x) * 2560 * thumb_sensitivity
        # hand_y = thumb.y * 1080 * thumb_sensitivity
        # if is_hand_mouse:
        #     mouse_position(hand_x, hand_y)

        # for part, (x, y) in screen_hand.items():
        #     canvas.create_line(x, y, x + 3, y + 3, fill="green")

        current_time = timestamp()
        # print(f"Gesture: {gesture} | Time: {current_time - last_time}")
        if gesture in ["Closed_Fist"] and current_time - last_time >= 1000:
            pause_play()
            last_time = current_time
        # if gesture in ["Closed_Fist"] and current_time - last_time >= 1000:
        #     is_hand_mouse = not is_hand_mouse
        #     last_time = current_time


    def do_on_nothing():
        set_square_color("red")


    gesture = Gesture(
        "resources/gesture_recognizer.task ",
        do_on_gesture,
        do_on_nothing
    )
    threading.Thread(target=gesture.recognition).start()

    root.mainloop()
