from typing import TypedDict

import cv2 as cv
import numpy as np

from .bbox import BBox
from modules import core


class Detection(TypedDict):
    id: int
    score: float
    bbox: BBox


def append_detections_to_img(
    img: np.ndarray,
    input_size: core.types.InputSize,
    detections: list[Detection],
    labels: core.types.Labels = {},
):
    h_img, w_img = img.shape[:2]
    h_in, w_in = input_size

    scale_x = w_img / w_in
    scale_y = h_img / h_in

    for detection in detections:
        bbox = detection["bbox"]
        bbox = bbox.scale(scale_x, scale_y)

        x0, y0 = int(bbox.xmin), int(bbox.ymin)
        x1, y1 = int(bbox.xmax), int(bbox.ymax)

        img = cv.rectangle(img, (x0, y0), (x1, y1), (0, 255, 0), 2)

        if labels:
            percent = int(100 * detection["score"])
            label = f"{percent}% {labels[detection['id']]}"
            img = cv.putText(
                img,
                label,
                (x0 + 10, y0 + 30),
                fontFace=cv.FONT_HERSHEY_SIMPLEX,
                fontScale=0.6,
                thickness=2,
                color=(255, 0, 0),
            )

    return img


def make_detection(scale, class_id, score, box) -> Detection:
    ymin, xmin, ymax, xmax = box
    bbox = BBox(ymin, xmin, ymax, xmax)
    bbox = bbox.scale(*scale).map(int)
    return {"id": int(class_id), "score": score, "bbox": bbox}
