import cv2 as cv
import numpy as np

from modules import core
from . import common


def ssd_mobilenet_v1_coco_quant_postprocess_edgetpu(
    interpreter: core.Interpreter,
    labels: core.types.Labels,
    img: np.ndarray,
    *,
    top_k: int = 5,
    score_threshold: float = 0.1,
):
    input_size = interpreter.get_input_size(0)
    input_index = interpreter.get_input_index(0)

    resized = cv.resize(img, input_size, interpolation=cv.INTER_AREA)
    resized = np.expand_dims(resized, axis=0)

    interpreter.set_tensor(input_index, resized)
    interpreter.invoke()

    boxes = interpreter.get_output_tensor(0)[0]
    class_ids = interpreter.get_output_tensor(1)[0]
    scores = interpreter.get_output_tensor(2)[0]
    count = int(interpreter.get_output_tensor(3)[0])

    detections = [
        common.make_detection(
            scale=input_size, class_id=class_ids[i], score=scores[i], box=boxes[i]
        )
        for i in range(count)
        if scores[i] >= score_threshold
    ][:top_k]

    common.append_detections_to_img(
        img=img,
        input_size=input_size,
        detections=detections,
        labels=labels,
    )


def ssd_mobilenet_v2_coco_quant_postprocess_edgetpu(
    interpreter: core.Interpreter,
    labels: core.types.Labels,
    img: np.ndarray,
    *,
    top_k: int = 5,
    score_threshold: float = 0.1,
):
    ssd_mobilenet_v1_coco_quant_postprocess_edgetpu(
        interpreter, labels, img, top_k=top_k, score_threshold=score_threshold
    )


def tf2_ssd_mobilenet_v1_fpn_640x640_coco17_ptq_edgetpu(
    interpreter: core.Interpreter,
    labels: core.types.Labels,
    img: np.ndarray,
    *,
    top_k: int = 5,
    score_threshold: float = 0.1,
):
    input_size = interpreter.get_input_size(0)
    input_index = interpreter.get_input_index(0)

    resized = cv.resize(img, input_size, interpolation=cv.INTER_AREA)
    resized = np.expand_dims(resized, axis=0)

    interpreter.set_tensor(input_index, resized)
    interpreter.invoke()

    boxes = interpreter.get_output_tensor(0)[0]
    class_ids = interpreter.get_output_tensor(1)[0]
    scores = interpreter.get_output_tensor(2)[0]
    count = int(interpreter.get_output_tensor(3)[0])

    detections = [
        common.make_detection(
            scale=input_size, class_id=class_ids[i], score=scores[i], box=boxes[i]
        )
        for i in range(count)
        if scores[i] >= score_threshold
    ][:top_k]

    common.append_detections_to_img(
        img=img,
        input_size=input_size,
        detections=detections,
        labels=labels,
    )


def ssd_mobilenet_v2_face_quant_postprocess_edgetpu(
    interpreter: core.Interpreter,
    labels: core.types.Labels,
    img: np.ndarray,
    *,
    top_k: int = 5,
    score_threshold: float = 0.1,
):
    input_size = interpreter.get_input_size(0)
    input_index = interpreter.get_input_index(0)

    resized = cv.resize(img, input_size, interpolation=cv.INTER_AREA)
    resized = np.expand_dims(resized, axis=0)

    interpreter.set_tensor(input_index, resized)
    interpreter.invoke()

    boxes = interpreter.get_output_tensor(0)[0]
    class_ids = interpreter.get_output_tensor(1)[0]
    scores = interpreter.get_output_tensor(2)[0]
    count = int(interpreter.get_output_tensor(3)[0])

    detections = [
        common.make_detection(
            scale=input_size, class_id=class_ids[i], score=scores[i], box=boxes[i]
        )
        for i in range(count)
        if scores[i] >= score_threshold
    ][:top_k]

    common.append_detections_to_img(
        img=img,
        input_size=input_size,
        detections=detections,
        labels={},
    )
