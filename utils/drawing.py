import math
import cv2


def draw_arrow(img, p1, p2, color=(0,0,255), thickness=4):
    # draw base line
    cv2.line(img, p1, p2, color, thickness)

    # direction
    angle = math.atan2(p1[1] - p2[1], p1[0] - p2[0])

    # fixed arrow size
    arrow_length = 20   # 🔥 constant size
    arrow_angle = math.pi / 6  # 30 degrees

    # arrow points
    x1 = int(p2[0] + arrow_length * math.cos(angle + arrow_angle))
    y1 = int(p2[1] + arrow_length * math.sin(angle + arrow_angle))

    x2 = int(p2[0] + arrow_length * math.cos(angle - arrow_angle))
    y2 = int(p2[1] + arrow_length * math.sin(angle - arrow_angle))

    # draw arrow head
    cv2.line(img, p2, (x1, y1), color, thickness)
    cv2.line(img, p2, (x2, y2), color, thickness)
