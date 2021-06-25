import time
import cv2


prev_time = time.time()


def print_fps(image):
    global prev_time

    fontScale = 1.5
    fontFace = cv2.FONT_HERSHEY_PLAIN
    fontColor = (0, 245, 0)
    fontThickness = 2

    cur_time = time.time()
    time_diff = cur_time - prev_time
    fps = 1 / time_diff
    fps = round(fps, 2)
    prev_time = cur_time

    cv2.putText(image, f"FPS: {fps}", (30, 50), fontFace, fontScale,
                fontColor, fontThickness, cv2.LINE_AA)
