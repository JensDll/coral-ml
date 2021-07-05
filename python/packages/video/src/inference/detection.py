import pathlib
from pycoral.utils import dataset, edgetpu
from pycoral.adapters import common, detect
import cv2
import numpy as np
import os

models_dir = pathlib.Path(os.path.dirname(__file__)) \
    .joinpath("models").joinpath("detection")
model_file = models_dir.joinpath(
    "mobilenet_ssd_v2_coco_quant_postprocess_edgetpu.tflite")
label_file = models_dir.joinpath("coco_labels.txt")

labels = dataset.read_label_file(str(label_file.resolve()))
interpreter = edgetpu.make_interpreter(str(model_file.resolve()), device="usb")
interpreter.allocate_tensors()
input_size = common.input_size(interpreter)


def append_objs_to_img(img, input_size, objs, labels: dict):
    h_img, w_img = img.shape[:2]
    h_in, w_in = input_size

    scale_x = w_img / w_in
    scale_y = h_img / h_in

    for obj in objs:
        bbox: detect.BBox = obj.bbox
        bbox = bbox.scale(scale_x, scale_y)

        x0, y0 = int(bbox.xmin), int(bbox.ymin)
        x1, y1 = int(bbox.xmax), int(bbox.ymax)

        percent = int(100 * obj.score)
        label = f"{percent}% {labels[obj.id]}"

        img = cv2.rectangle(img, (x0, y0), (x1, y1), (0, 255, 0), 2)
        img = cv2.putText(img, label, (x0, y0 + 30),
                          cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 0), 2)
    return img


def run_inference(frame: np.ndarray):
    frame_rgb = cv2.resize(frame, input_size)
    frame_rgb = cv2.cvtColor(frame_rgb, cv2.COLOR_BGR2RGB)
    edgetpu.run_inference(interpreter, frame_rgb.tobytes())
    objs = detect.get_objects(interpreter, score_threshold=0.1)[:5]
    result = append_objs_to_img(frame, input_size, objs, labels)
    return result
