import time

import cv2
import numpy as np


class FpsCounter:
    def __init__(self) -> None:
        self.fps_iter = FpsCounter.__fps_iter()

    def put_fps(self, img: np.ndarray):
        cv2.putText(
            img,
            f"{next(self.fps_iter):.2f}",
            (15, 25),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=0.5,
            thickness=1,
            color=(255, 255, 255),
            lineType=cv2.LINE_4,
        )

    @staticmethod
    def __fps_iter():
        prevTime = time.time()
        yield 0.0
        while True:
            currTime = time.time()
            diff = currTime - prevTime
            fps = 1 / diff
            prevTime = currTime
            yield fps
