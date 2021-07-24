import time
import cv2
import numpy as np


def fps_iter():
    prev = time.time()
    yield 0.0  # First fps value
    while True:
        curr = time.time()
        diff = curr - prev
        fps = 1 / diff
        prev = curr
        yield fps


def print_fps(img: np.ndarray, fps_iter):
    fps = next(fps_iter)

    cv2.putText(
        img,
        "FPS: {:.2f}".format(fps),
        (30, 30),
        fontFace=1,
        fontScale=cv2.FONT_HERSHEY_PLAIN,
        color=(0, 245, 0),
        thickness=1,
        lineType=cv2.LINE_AA,
    )
