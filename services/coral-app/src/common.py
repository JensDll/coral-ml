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
from zmq.asyncio import Socket

EDGETUP_LIB = {
    "Linux": "libedgetpu.so.1",
    "Darwin": "libedgetpu.1.dylib",
    "Windows": "edgetpu.dll",
}[platform.system()]


def get_output_detail(interpreter: tflite.Interpreter, i: int, key: str):
    return interpreter.get_output_details()[i][key]


def get_output_shape(interpreter: tflite.Interpreter, i: int):
    return get_output_detail(interpreter, i, "shape")


def get_output_dtype(interpreter: tflite.Interpreter, i: int):
    return get_output_detail(interpreter, i, "dtype")


def get_output_tensor(interpreter: tflite.Interpreter, i):
    output_index = interpreter.get_output_details()[i]["index"]
    return interpreter.tensor(output_index)()


def get_num_outputs(interpreter: tflite.Interpreter):
    return len(interpreter.get_output_details())


def get_input_detail(interpreter: tflite.Interpreter, key):
    return interpreter.get_input_details()[0][key]


def get_input_size(interpreter: tflite.Interpreter):
    _, height, width, _ = get_input_detail(interpreter, "shape")
    return width, height


def get_input_index(interpreter: tflite.Interpreter):
    return get_input_detail(interpreter, "index")


def load_labels(label_path):
    label_path = pathlib.Path(str(label_path))
    labels = {}
    if not label_path.is_file():
        return labels
    with label_path.open("r", encoding="utf-8") as f:
        lines = f.readlines()
    for row_number, content in enumerate(lines):
        pair = re.split(r"[:\s]+", content.strip(), maxsplit=1)
        if len(pair) == 2 and pair[0].strip().isdigit():
            labels[int(pair[0])] = pair[1].strip()
        else:
            labels[row_number] = pair[0].strip()
    return labels


def load_interpreter(model_path):
    model_path = pathlib.Path(str(model_path))
    delegate = tflite.load_delegate(EDGETUP_LIB)
    interpreter = tflite.Interpreter(
        model_path=str(model_path), experimental_delegates=[delegate]
    )
    interpreter.allocate_tensors()
    return interpreter


class LoadModelResult(TypedDict):
    success: str
    model_path: bytes
    label_path: bytes
    record_type: str
    model_file_name: str


async def load_model(record_repo: repos.RecordRepository, id):
    result: LoadModelResult = {
        "success": True,
        "model_path": None,
        "label_path": None,
        "record_type": None,
        "model_file_name": None,
    }

    try:
        (model_path, label_path), (record_type, model_file_name) = await asyncio.gather(
            record_repo.download(id), record_repo.get_record_info(id)
        )
        await record_repo.set_loaded(id)

        result["model_path"] = str(model_path)
        result["label_path"] = str(label_path)
        result["record_type"] = record_type
        result["model_file_name"] = model_file_name
    except Exception:
        logging.error("Error loading model")
        logging.error(traceback.format_exc())
        result["success"] = False

    return result


def invoke_interpreter(interpreter: tflite.Interpreter, data):
    input_index = get_input_index(interpreter)
    img = np.expand_dims(data, axis=0)
    interpreter.set_tensor(input_index, img)
    interpreter.invoke()
