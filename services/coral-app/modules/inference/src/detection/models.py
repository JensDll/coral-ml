import cv2
import numpy as np
from .bbox import BBox
from typing import TypedDict
from modules import core


class Detection(TypedDict):
    id: int
    score: float
    bbox: BBox


class ModelArgs(TypedDict):
    labels: dict
    topK: int
    scoreThreshold: float


def append_detections_to_image(
    image: np.ndarray,
    input_size: core.typedef.InputSize,
    detections: list[Detection],
    labels: core.typedef.Labels = {},
):
    h_image, w_image = image.shape[:2]
    h_in, w_in = input_size

    scale_x = w_image / w_in
    scale_y = h_image / h_in

    for detection in detections:
        bbox = detection["bbox"]
        bbox = bbox.scale(scale_x, scale_y)

        x0, y0 = int(bbox.xmin), int(bbox.ymin)
        x1, y1 = int(bbox.xmax), int(bbox.ymax)

        image = cv2.rectangle(image, (x0, y0), (x1, y1), (0, 255, 0), 2)

        if labels:
            percent = int(100 * detection["score"])
            label = f"{percent}% {labels[detection['id']]}"
            image = cv2.putText(
                image,
                label,
                (x0 + 10, y0 + 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 0, 0),
                2,
            )

    return image


def make_detection(scale, class_id, score, box) -> Detection:
    ymin, xmin, ymax, xmax = box
    bbox = BBox(ymin, xmin, ymax, xmax)
    bbox = bbox.scale(*scale).map(int)
    return {"id": int(class_id), "score": score, "bbox": bbox}


def invoke_interpreter(interpreter: core.Interpreter, data):
    input_index = interpreter.get_input_index(0)
    data = np.expand_dims(data, axis=0)
    interpreter.set_tensor(input_index, data)
    interpreter.invoke()


def ssd_mobilenet_v1_coco_quant_postprocess_edgetpu(
    interpreter: core.Interpreter, args: ModelArgs, image: np.ndarray
):
    input_size = interpreter.get_input_size(0)
    resized = cv2.resize(image, input_size, interpolation=cv2.INTER_AREA)

    invoke_interpreter(interpreter, resized)

    boxes = interpreter.get_output_tensor(0)[0]
    class_ids = interpreter.get_output_tensor(1)[0]
    scores = interpreter.get_output_tensor(2)[0]
    count = int(interpreter.get_output_tensor(3)[0])

    detections = [
        make_detection(
            scale=input_size, class_id=class_ids[i], score=scores[i], box=boxes[i]
        )
        for i in range(count)
        if scores[i] >= args["scoreThreshold"]
    ][: args["topK"]]

    append_detections_to_image(
        image=image,
        input_size=input_size,
        detections=detections,
        labels=args["labels"],
    )


def ssd_mobilenet_v2_coco_quant_postprocess_edgetpu(
    interpreter: core.Interpreter, args: ModelArgs, image: np.ndarray
):
    ssd_mobilenet_v1_coco_quant_postprocess_edgetpu(interpreter, args, image)


def tf2_ssd_mobilenet_v1_fpn_640x640_coco17_ptq_edgetpu(
    interpreter: core.Interpreter, args: ModelArgs, image: np.ndarray
):
    input_size = interpreter.get_input_size(0)
    resized = cv2.resize(image, input_size, interpolation=cv2.INTER_AREA)

    invoke_interpreter(interpreter, resized)

    scores = interpreter.get_output_tensor(0)[0]
    boxes = interpreter.get_output_tensor(1)[0]
    count = int(interpreter.get_output_tensor(2)[0])
    class_ids = interpreter.get_output_tensor(3)[0]

    detections = [
        make_detection(
            scale=input_size, class_id=class_ids[i], score=scores[i], box=boxes[i]
        )
        for i in range(count)
        if scores[i] >= args["scoreThreshold"]
    ][: args["topK"]]

    append_detections_to_image(
        image=image,
        input_size=input_size,
        detections=detections,
        labels=args["labels"],
    )


def ssd_mobilenet_v2_face_quant_postprocess_edgetpu(
    interpreter: core.Interpreter, args: ModelArgs, image: np.ndarray
):
    input_size = interpreter.get_input_size(0)
    resized = cv2.resize(image, input_size, interpolation=cv2.INTER_AREA)

    invoke_interpreter(interpreter, resized)

    boxes = interpreter.get_output_tensor(0)[0]
    class_ids = interpreter.get_output_tensor(1)[0]
    scores = interpreter.get_output_tensor(2)[0]
    count = int(interpreter.get_output_tensor(3)[0])

    detections = [
        make_detection(
            scale=input_size, class_id=class_ids[i], score=scores[i], box=boxes[i]
        )
        for i in range(count)
        if scores[i] >= args["scoreThreshold"]
    ]

    append_detections_to_image(
        image=image, input_size=input_size, detections=detections
    )
