import tflite_runtime.interpreter as tflite
import cv2
import numpy as np

from src import common
from typing_extensions import TypedDict
from src.inference.video.bbox import BBox
from src.inference.video.common import append_detections_to_frame, Detection


def invoke_interpreter(interpreter: tflite.Interpreter, data):
    input_index = common.get_input_index(interpreter, 0)
    data = np.expand_dims(data, axis=0)
    interpreter.set_tensor(input_index, data)
    interpreter.invoke()


class ModelArgs(TypedDict):
    labels: dict
    top_k: int
    score_threshold: int


def make_detection(scale, class_id, score, box) -> Detection:
    ymin, xmin, ymax, xmax = box
    bbox = BBox(ymin, xmin, ymax, xmax)
    bbox = bbox.scale(*scale).map(int)
    return {"id": int(class_id), "score": score, "bbox": bbox}


def ssd_mobilenet_v1_coco_quant_postprocess_edgetpu(
    interpreter: tflite.Interpreter, args: ModelArgs, frame: np.ndarray
):
    input_size = common.get_input_size(interpreter, 0)
    resized = cv2.resize(frame, input_size, interpolation=cv2.INTER_AREA)

    invoke_interpreter(interpreter, resized)

    boxes = common.get_output_tensor(interpreter, 0)[0]
    class_ids = common.get_output_tensor(interpreter, 1)[0]
    scores = common.get_output_tensor(interpreter, 2)[0]
    count = int(common.get_output_tensor(interpreter, 3)[0])

    detections = [
        make_detection(
            scale=input_size, class_id=class_ids[i], score=scores[i], box=boxes[i]
        )
        for i in range(count)
        if scores[i] >= args["score_threshold"]
    ][: args["top_k"]]

    append_detections_to_frame(
        frame=frame,
        input_size=input_size,
        detections=detections,
        labels=args["labels"],
    )


def ssd_mobilenet_v2_coco_quant_postprocess_edgetpu(
    interpreter: tflite.Interpreter, args: ModelArgs, frame: np.ndarray
):
    ssd_mobilenet_v1_coco_quant_postprocess_edgetpu(interpreter, args, frame)


def tf2_ssd_mobilenet_v1_fpn_640x640_coco17_ptq_edgetpu(
    interpreter: tflite.Interpreter, args: ModelArgs, frame: np.ndarray
):
    input_size = common.get_input_size(interpreter, 0)
    resized = cv2.resize(frame, input_size, interpolation=cv2.INTER_AREA)

    invoke_interpreter(interpreter, resized)

    scores = common.get_output_tensor(interpreter, 0)[0]
    boxes = common.get_output_tensor(interpreter, 1)[0]
    count = int(common.get_output_tensor(interpreter, 2)[0])
    class_ids = common.get_output_tensor(interpreter, 3)[0]

    detections = [
        make_detection(
            scale=input_size, class_id=class_ids[i], score=scores[i], box=boxes[i]
        )
        for i in range(count)
        if scores[i] >= args["score_threshold"]
    ][: args["top_k"]]

    append_detections_to_frame(
        frame=frame,
        input_size=input_size,
        detections=detections,
        labels=args["labels"],
    )


def ssd_mobilenet_v2_face_quant_postprocess_edgetpu(
    interpreter: tflite.Interpreter, args: ModelArgs, frame: np.ndarray
):
    input_size = common.get_input_size(interpreter, 0)
    resized = cv2.resize(frame, input_size, interpolation=cv2.INTER_AREA)

    invoke_interpreter(interpreter, resized)

    boxes = common.get_output_tensor(interpreter, 0)[0]
    class_ids = common.get_output_tensor(interpreter, 1)[0]
    scores = common.get_output_tensor(interpreter, 2)[0]
    count = int(common.get_output_tensor(interpreter, 3)[0])

    detections = [
        make_detection(
            scale=input_size, class_id=class_ids[i], score=scores[i], box=boxes[i]
        )
        for i in range(count)
        if scores[i] >= args["score_threshold"]
    ]

    append_detections_to_frame(
        frame=frame, input_size=input_size, detections=detections
    )
