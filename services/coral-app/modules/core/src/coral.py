import pathlib
import asyncio
import re
import logging
import platform
import tflite_runtime.interpreter as tflite
from typing import Union
from modules import core, repositories


EDGETUP_LIB = {
    "Linux": "libedgetpu.so.1",
    "Darwin": "libedgetpu.1.dylib",
    "Windows": "edgetpu.dll",
}[platform.system()]


def load_labels(path: Union[str, pathlib.Path]):
    label_path = pathlib.Path(str(path))
    labels: core.typedef.Labels = {}

    if not label_path.is_file():
        return labels

    def remove_quotes(s: str):
        return re.sub(r"\A\"|\"$", "", s).strip()

    with label_path.open("r", encoding="utf-8") as file:
        lines = file.readlines()

    for row, line in enumerate(lines):
        line = line.strip()
        pair = re.split(r"[:\s,]+", line, maxsplit=1)
        if len(pair) == 2:
            if pair[0].isdigit():
                labels[int(pair[0])] = remove_quotes(pair[1])
            else:
                labels[row] = remove_quotes(line)
        else:
            labels[row] = remove_quotes(pair[0])

    return labels


async def load_model(id: core.typedef.Id):
    result: core.typedef.LoadModelResult = {
        "success": True,
        "modelPath": "",
        "labelPath": "",
        "record": {
            "id": -1,
            "modelFileName": "",
            "recordTypeId": -1,
            "recordType": "Image Classification",
        },
    }

    try:
        (model_path, label_path), record = await asyncio.gather(
            repositories.Record.download(id),
            repositories.Record.get_by_id(id),
        )
        result["modelPath"] = str(model_path)
        result["labelPath"] = str(label_path)
        result["record"] = record
    except Exception:
        logging.error("Error loading model")
        result["success"] = False

    return result


def load_interpreter(model_path: Union[pathlib.Path, str]):
    model_path = str(model_path)
    delegate = tflite.load_delegate(EDGETUP_LIB)
    interpreter = core.Interpreter(
        model_path=model_path, experimental_delegates=[delegate]
    )
    interpreter.allocate_tensors()
    core.logging.log_details(interpreter)
    return interpreter
