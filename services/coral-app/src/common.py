import asyncio
import pathlib
import platform
import re
from typing_extensions import TypedDict
import tflite_runtime.interpreter as tflite
import numpy as np
import src.repositories as repos
import logging
import traceback

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


def load_interpreter(model_path: pathlib.Path, label_path: pathlib.Path):
    delegate = tflite.load_delegate(EDGETUP_LIB)
    interpreter = tflite.Interpreter(
        model_path=str(model_path), experimental_delegates=[delegate]
    )
    interpreter.allocate_tensors()
    labels = load_labels(label_path)
    return interpreter, labels


def invoke_interpreter(interpreter: tflite.Interpreter, data):
    input_index = get_input_index(interpreter)
    img = np.expand_dims(data, axis=0)
    interpreter.set_tensor(input_index, img)
    interpreter.invoke()


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
    except Exception:
        logging.error("Error loading model")
        logging.error(traceback.format_exc())
        result["success"] = False

    return result
