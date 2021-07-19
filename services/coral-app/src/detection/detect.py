from typing_extensions import TypedDict
from typing import List
import cv2
import tflite_runtime.interpreter as tflite
import src.common as common
from src.detection.bbox import BBox


class Detection(TypedDict):
    id: int
    score: float
    bbox: BBox


def append_detection_to_img(img, input_size, detections: List[Detection], labels: dict):
    h_img, w_img = img.shape[:2]
    h_in, w_in = input_size

    scale_x = w_img / w_in
    scale_y = h_img / h_in

    for detection in detections:
        bbox = detection["bbox"]
        bbox = bbox.scale(scale_x, scale_y)

        x0, y0 = int(bbox.xmin), int(bbox.ymin)
        x1, y1 = int(bbox.xmax), int(bbox.ymax)

        percent = int(100 * detection["score"])
        label = f"{percent}% {labels[detection['id']]}"

        img = cv2.rectangle(img, (x0, y0), (x1, y1), (0, 255, 0), 2)
        img = cv2.putText(
            img, label, (x0, y0 + 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 0), 2
        )

    return img


def get_detections(interpreter: tflite.Interpreter, score_threshold=0.1):
    boxes = common.get_output_tensor(interpreter, 0)[0]
    class_ids = common.get_output_tensor(interpreter, 1)[0]
    scores = common.get_output_tensor(interpreter, 2)[0]
    count = int(common.get_output_tensor(interpreter, 3)[0])

    width, height = common.get_input_size(interpreter)
    image_scale_x, image_scale_y = 1.0, 1.0
    sx, sy = width / image_scale_x, height / image_scale_y

    def make(i) -> Detection:
        ymin, xmin, ymax, xmax = boxes[i]
        bbox = BBox(ymin, xmin, ymax, xmax)
        bbox = bbox.scale(sx, sy).map(int)
        return {"id": int(class_ids[i]), "score": scores[i], "bbox": bbox}

    return [make(i) for i in range(count) if scores[i] >= score_threshold]
