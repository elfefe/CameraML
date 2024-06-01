import time


def timestamp():
    return int(time.time() * 1000)


def ease_in_quad(t):
    """
  Easing function with quadratic ease-in effect.

  Args:
      t: Progress value between 0 (start) and 1 (end).

  Returns:
      Eased progress value.
  """
    return t * t


def ease_out_quad(t):
    """
  Easing function with quadratic ease-out effect.

  Args:
      t: Progress value between 0 (start) and 1 (end).

  Returns:
      Eased progress value.
  """
    return -t * (t - 2)


def ease_in_out_quad(t):
    """
  Easing function with quadratic ease-in and ease-out effect.

  Args:
      t: Progress value between 0 (start) and 1 (end).

  Returns:
      Eased progress value.
  """
    if t < 0.5:
        return 2 * t * t
    else:
        return -1 + (4 - 2 * t) * t


def move_point(start_pos, end_pos, duration, progress, ease_func):
    """
  Calculates the position of a point at a given progress with easing.

  Args:
      start_pos: Starting position of the point.
      end_pos: Ending position of the point.
      duration: Total duration of the movement.
      progress: Progress value between 0 (start) and 1 (end).
      ease_func: Easing function to apply.

  Returns:
      The current position of the point.
  """
    t = progress / duration
    ease = ease_func(t)
    x = start_pos.x + (end_pos.x - start_pos.x) * ease
    y = start_pos.y + (end_pos.y - start_pos.y) * ease
    return (x, y)


def draw_hand(hand, canvas):
    try:
        color = "green"
        width = 4
        canvas.create_line(hand["WRIST"].x, hand["WRIST"].y, hand["THUMB_CMC"].x, hand["THUMB_CMC"].y,
                           fill=color, width=width)
        canvas.create_line(hand["THUMB_CMC"].x, hand["THUMB_CMC"].y, hand["THUMB_MCP"].x, hand["THUMB_MCP"].y,
                           fill=color, width=width)
        canvas.create_line(hand["THUMB_MCP"].x, hand["THUMB_MCP"].y, hand["THUMB_IP"].x, hand["THUMB_IP"].y,
                           fill=color, width=width)
        canvas.create_line(hand["THUMB_IP"].x, hand["THUMB_IP"].y, hand["THUMB_TIP"].x, hand["THUMB_TIP"].y,
                           fill=color, width=width)
        canvas.create_line(hand["WRIST"].x, hand["WRIST"].y, hand["INDEX_FINGER_MCP"].x, hand["INDEX_FINGER_MCP"].y,
                           fill=color, width=width)
        canvas.create_line(hand["INDEX_FINGER_MCP"].x, hand["INDEX_FINGER_MCP"].y, hand["INDEX_FINGER_PIP"].x,
                           hand["INDEX_FINGER_PIP"].y,
                           fill=color, width=width)
        canvas.create_line(hand["INDEX_FINGER_PIP"].x, hand["INDEX_FINGER_PIP"].y, hand["INDEX_FINGER_DIP"].x,
                           hand["INDEX_FINGER_DIP"].y,
                           fill=color, width=width)
        canvas.create_line(hand["INDEX_FINGER_DIP"].x, hand["INDEX_FINGER_DIP"].y, hand["INDEX_FINGER_TIP"].x,
                           hand["INDEX_FINGER_TIP"].y,
                           fill=color, width=width)
        canvas.create_line(hand["WRIST"].x, hand["WRIST"].y, hand["MIDDLE_FINGER_MCP"].x,
                           hand["MIDDLE_FINGER_MCP"].y,
                           fill=color, width=width)
        canvas.create_line(hand["MIDDLE_FINGER_MCP"].x, hand["MIDDLE_FINGER_MCP"].y, hand["MIDDLE_FINGER_PIP"].x,
                           hand["MIDDLE_FINGER_PIP"].y,
                           fill=color, width=width)
        canvas.create_line(hand["MIDDLE_FINGER_PIP"].x, hand["MIDDLE_FINGER_PIP"].y, hand["MIDDLE_FINGER_DIP"].x,
                           hand["MIDDLE_FINGER_DIP"].y,
                           fill=color, width=width)
        canvas.create_line(hand["MIDDLE_FINGER_DIP"].x, hand["MIDDLE_FINGER_DIP"].y, hand["MIDDLE_FINGER_TIP"].x,
                           hand["MIDDLE_FINGER_TIP"].y,
                           fill=color, width=width)
        canvas.create_line(hand["WRIST"].x, hand["WRIST"].y, hand["RING_FINGER_MCP"].x, hand["RING_FINGER_MCP"].y,
                           fill=color, width=width)
        canvas.create_line(hand["RING_FINGER_MCP"].x, hand["RING_FINGER_MCP"].y, hand["RING_FINGER_PIP"].x,
                           hand["RING_FINGER_PIP"].y,
                           fill=color, width=width)
        canvas.create_line(hand["RING_FINGER_PIP"].x, hand["RING_FINGER_PIP"].y, hand["RING_FINGER_DIP"].x,
                           hand["RING_FINGER_DIP"].y,
                           fill=color, width=width)
        canvas.create_line(hand["RING_FINGER_DIP"].x, hand["RING_FINGER_DIP"].y, hand["RING_FINGER_TIP"].x,
                           hand["RING_FINGER_TIP"].y,
                           fill=color, width=width)
        canvas.create_line(hand["WRIST"].x, hand["WRIST"].y, hand["PINKY_MCP"].x, hand["PINKY_MCP"].y,
                           fill=color, width=width)
        canvas.create_line(hand["PINKY_MCP"].x, hand["PINKY_MCP"].y, hand["PINKY_PIP"].x, hand["PINKY_PIP"].y,
                           fill=color, width=width)
        canvas.create_line(hand["PINKY_PIP"].x, hand["PINKY_PIP"].y, hand["PINKY_DIP"].x, hand["PINKY_DIP"].y,
                           fill=color, width=width)
        canvas.create_line(hand["PINKY_DIP"].x, hand["PINKY_DIP"].y, hand["PINKY_TIP"].x, hand["PINKY_TIP"].y,
                           fill=color, width=width)

    except Exception as e:
        print(e)
    return canvas
