from typing_extensions import TypedDict
from typing import List
import cv2
import tflite_runtime.interpreter as tflite
import src.common as common
from src.inference.detection.bbox import BBox


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
            img, label, (x0, y0 + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2
        )

    return img


def get_detections(interpreter: tflite.Interpreter, score_threshold=0.1):
    print(interpreter.get_output_details())
    for i in range(common.get_num_outputs(interpreter)):
        shape_len = len(common.get_output_shape(interpreter, i))
        output = common.get_output_tensor(interpreter, i)[0]
        if shape_len == 3:
            boxes = output
        elif shape_len == 1:
            count = int(output)
        elif int(output[0]) == 0 or int(output[1]) == 0:
            scores = output
        else:
            class_ids = output

    sx, sy = common.get_input_size(interpreter)

    def make_detection(class_ids, scores) -> Detection:
        ymin, xmin, ymax, xmax = boxes[i]
        bbox = BBox(ymin, xmin, ymax, xmax)
        bbox = bbox.scale(sx, sy).map(int)
        return {"id": int(class_ids), "score": scores, "bbox": bbox}

    return [
        make_detection(class_ids[i], scores[i])
        for i in range(count)
        if scores[i] >= score_threshold
    ]
