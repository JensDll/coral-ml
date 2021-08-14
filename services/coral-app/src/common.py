import asyncio
from os import path
import pathlib
import platform
import re
import tflite_runtime.interpreter as tflite
import numpy as np
import src.repositories as repos
import logging
import traceback

from typing_extensions import TypedDict
from typing import Tuple

EDGETUP_LIB = {
    "Linux": "libedgetpu.so.1",
    "Darwin": "libedgetpu.1.dylib",
    "Windows": "edgetpu.dll",
}[platform.system()]


def _get_output_detail(interpreter: tflite.Interpreter, i: int, key: str):
    return interpreter.get_output_details()[i][key]


def get_output_shape(interpreter: tflite.Interpreter, i: int):
    return _get_output_detail(interpreter, i, "shape")


def get_output_dtype(interpreter: tflite.Interpreter, i: int):
    return _get_output_detail(interpreter, i, "dtype")


def get_output_tensor(interpreter: tflite.Interpreter, i: int) -> np.ndarray:
    output_index = interpreter.get_output_details()[i]["index"]
    return interpreter.tensor(output_index)()


def get_output_quant(interpreter: tflite.Interpreter, i: int):
    return _get_output_detail(interpreter, i, "quantization")


def get_num_outputs(interpreter: tflite.Interpreter):
    return len(interpreter.get_output_details())


def _get_input_detail(interpreter: tflite.Interpreter, i: int, key: str):
    return interpreter.get_input_details()[i][key]


def get_input_size(interpreter: tflite.Interpreter, i: int):
    _, height, width, _ = _get_input_detail(interpreter, i, "shape")
    return width, height


def get_input_index(interpreter: tflite.Interpreter, i: int):
    return _get_input_detail(interpreter, i, "index")


def get_input_dtype(interpreter: tflite.Interpreter, i: int):
    return _get_input_detail(interpreter, i, "dtype")


def get_input_quant(interpreter: tflite.Interpreter, i) -> Tuple[float, float]:
    return _get_input_detail(interpreter, i, "quantization")


def load_labels(label_path):
    label_path = pathlib.Path(str(label_path))
    labels = {}

    if not label_path.is_file():
        return labels

    sub_regex = re.compile(r"\A\"|\"$")
    split_regex = re.compile(r"[:\s,]+")

    def remove_leading_trailing_quotes(s: str):
        return re.sub(sub_regex, "", s).strip()

    with label_path.open("r", encoding="utf-8") as f:
        lines = f.readlines()

    for row_number, content in enumerate(lines):
        pair = re.split(split_regex, content.strip(), maxsplit=1)
        if len(pair) == 2:
            pair[0] = pair[0].strip()
            pair[1] = pair[1].strip()
            if pair[0].isdigit():
                labels[int(pair[0])] = remove_leading_trailing_quotes(pair[1])
            else:
                labels[row_number] = remove_leading_trailing_quotes(
                    f"{pair[0]} {pair[1]}"
                )
        else:
            pair[0] = pair[0].strip()
            labels[row_number] = remove_leading_trailing_quotes(pair[0])

    return labels


def log_details(interpreter: tflite.Interpreter):
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    logging.info("INPUT DETAILS ...")
    logging.info(input_details)
    logging.info("OUTPUT DETAILS ...")
    logging.info(output_details)


def load_interpreter(model_path):
    model_path = pathlib.Path(str(model_path))
    delegate = tflite.load_delegate(EDGETUP_LIB)
    interpreter = tflite.Interpreter(
        model_path=str(model_path), experimental_delegates=[delegate]
    )
    interpreter.allocate_tensors()
    log_details(interpreter)
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
        result["model_path"] = str(model_path)
        result["label_path"] = str(label_path)
        result["record_type"] = record_type
        result["model_file_name"] = model_file_name
    except Exception:
        logging.error("Error loading model")
        logging.error(traceback.format_exc())
        result["success"] = False

    return result


# 1. normalization: f = (input - mean) / std
# 2. quantization: q = f / scale + zero_point
# The following code combines the two steps as such:
# q = (input - mean) / (std * scale) + zero_point
# However, if std * scale equals 1, and mean - zero_point equals 0, the input
# does not need any preprocessing (but in practice, even if the results are
# very close to 1 and 0, it is probably okay to skip preprocessing for better
# efficiency; we use 1e-5 below instead of absolute zero).
def invoke_interpreter(interpreter: tflite.Interpreter, *data: np.ndarray):
    mean, std = 127.5, 127.5

    for i, input_data in enumerate(data):
        input_scale, input_zero_point = get_input_quant(interpreter, i)

        if (
            not abs(input_scale * std - 1) < 1e-5
            and not abs(mean - input_zero_point) < 1e-5
        ):
            # Input data requires preprocessing
            print(input_scale, input_zero_point)
            input_data = (input_data - mean) / (std * input_scale) + input_zero_point
            input_data = (input_data / input_scale) + input_zero_point
            np.clip(input_data, 0, 255, out=input_data)
            input_data = input_data.astype(np.uint8)

        interpreter.set_tensor(get_input_index(interpreter, i), input_data)

    # Invoke interpreter
    interpreter.invoke()
    output = {}

    # Set output tensors
    for i, _ in enumerate(data):
        output_data = get_output_tensor(interpreter, i)
        # r = S(q - Z)
        output_scale, output_zero_point = get_output_quant(interpreter, i)
        output_data = output_scale * (output_data.astype(np.int64) - output_zero_point)
        output[i] = output_data

    return output
