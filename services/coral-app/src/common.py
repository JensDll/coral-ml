import asyncio
import pathlib
import platform
import re
from typing_extensions import TypedDict
import tflite_runtime.interpreter as tflite
import numpy as np
import cv2
import time
import src.repositories as repos
import logging

EDGETUP_LIB = {
    "Linux": "libedgetpu.so.1",
    "Darwin": "libedgetpu.1.dylib",
    "Windows": "edgetpu.dll",
}[platform.system()]


def get_output_tensor(interpreter: tflite.Interpreter, i):
    tensor_idx = interpreter.get_output_details()[i]["index"]
    return interpreter.tensor(tensor_idx)()


def get_input_detail(interpreter: tflite.Interpreter, key):
    return interpreter.get_input_details()[0][key]


def get_input_size(interpreter: tflite.Interpreter):
    _, height, width, _ = get_input_detail(interpreter, "shape")
    return width, height


def get_input_index(interpreter: tflite.Interpreter):
    return get_input_detail(interpreter, "index")


def load_labels(label_path: pathlib.Path):
    with label_path.open("r", encoding="utf-8") as f:
        lines = f.readlines()
    labels = {}
    for row_number, content in enumerate(lines):
        pair = re.split(r"[:\s]+", content.strip(), maxsplit=1)
        if len(pair) == 2 and pair[0].strip().isdigit():
            labels[int(pair[0])] = pair[1].strip()
        else:
            labels[row_number] = pair[0].strip()
    return labels


def interpreter_load(model_path: pathlib.Path, label_path: pathlib.Path):
    delegate = tflite.load_delegate(EDGETUP_LIB)
    interpreter = tflite.Interpreter(
        model_path=str(model_path), experimental_delegates=[delegate]
    )
    interpreter.allocate_tensors()
    labels = load_labels(label_path)
    return interpreter, labels


def interpreter_invoke(interpreter: tflite.Interpreter, img: np.ndarray):
    input_index = get_input_index(interpreter)
    img = np.expand_dims(img, axis=0)
    interpreter.set_tensor(input_index, img)
    start = time.perf_counter()
    interpreter.invoke()
    return (time.perf_counter() - start) * 1000


class LoadModelResult(TypedDict):
    success: str
    model_path: str
    label_path: str
    record_type: str


async def load_model(record_repo: repos.RecordRepository, id):
    result: LoadModelResult = {
        "success": True,
        "model_path": None,
        "label_path": None,
        "record_type": None,
    }

    try:
        (model_path, label_path), record_type = await asyncio.gather(
            record_repo.download(id), record_repo.get_record_type(id)
        )
        await record_repo.set_loaded(id)

        result["model_path"] = model_path
        result["label_path"] = label_path
        result["record_type"] = record_type
    except Exception as e:
        logging.error(str(e))
        result["success"] = False

    return result


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

    fontScale = 1
    fontFace = cv2.FONT_HERSHEY_PLAIN
    fontColor = (0, 245, 0)
    fontThickness = 1

    cv2.putText(
        img,
        "FPS: {:.2f}".format(fps),
        (30, 30),
        fontFace,
        fontScale,
        fontColor,
        fontThickness,
        cv2.LINE_AA,
    )
