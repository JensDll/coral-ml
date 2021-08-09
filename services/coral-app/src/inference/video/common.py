from typing_extensions import TypedDict
import cv2

from typing_extensions import TypedDict
from src.inference.video.bbox import BBox
from typing import List


class Detection(TypedDict):
    id: int
    score: float
    bbox: BBox


def append_detections_to_frame(
    frame, input_size, detections: List[Detection], labels: dict = None
):
    h_frame, w_frame = frame.shape[:2]
    h_in, w_in = input_size

    scale_x = w_frame / w_in
    scale_y = h_frame / h_in

    for detection in detections:
        bbox = detection["bbox"]
        bbox = bbox.scale(scale_x, scale_y)

        x0, y0 = int(bbox.xmin), int(bbox.ymin)
        x1, y1 = int(bbox.xmax), int(bbox.ymax)

        frame = cv2.rectangle(frame, (x0, y0), (x1, y1), (0, 255, 0), 2)

        if labels:
            percent = int(100 * detection["score"])
            label = f"{percent}% {labels[detection['id']]}"
            frame = cv2.putText(
                frame,
                label,
                (x0 + 10, y0 + 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 0, 0),
                2,
            )

    return frame
