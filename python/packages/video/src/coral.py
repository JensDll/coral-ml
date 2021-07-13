import asyncio
from os import path
import pathlib
from typing import List, Tuple
import time
import tflite_runtime.interpreter as tflite
import platform
import cv2
import numpy as np
import src.repositories as repos
import simplejpeg
import imageio
import re

EDGETUP_LIB = {
    'Linux': 'libedgetpu.so.1',
    'Darwin': 'libedgetpu.1.dylib',
    'Windows': 'edgetpu.dll'
}[platform.system()]


def get_input_details(interpreter: tflite.Interpreter):
    input_details = interpreter.get_input_details()[0]
    # print("Input Details")
    # print(input_details)
    input_shape = input_details["shape"][1:]
    input_dtype = input_details["dtype"]
    input_index = input_details["index"]
    return input_index, input_shape, input_dtype


def get_output_details(interpreter: tflite.Interpreter):
    output_details = interpreter.get_output_details()[0]
    # print("Output Details")
    # print(output_details)
    output_index = output_details["index"]
    output_shape = output_details["shape"]
    output_dtype = output_details["dtype"]
    return output_index, output_shape, output_dtype


def load_labels(label_path: pathlib.Path):
    with label_path.open("r", encoding="utf-8") as f:
        lines = f.readlines()
    labels = {}
    for row_number, content in enumerate(lines):
        pair = re.split(r'[:\s]+', content.strip(), maxsplit=1)
        if len(pair) == 2 and pair[0].strip().isdigit():
            labels[int(pair[0])] = pair[1].strip()
        else:
            labels[row_number] = pair[0].strip()
    return labels


def get_interpreter(model_path: pathlib.Path, label_path: pathlib.Path):
    delegate = tflite.load_delegate(EDGETUP_LIB)
    interpreter = tflite.Interpreter(
        model_path=str(model_path),
        experimental_delegates=[delegate]
    )
    interpreter.allocate_tensors()
    labels = load_labels(label_path)
    return interpreter, labels


async def load_model(record_repo: repos.RecordRepository, id):
    print(f"Loading model with id ({id})")
    paths, record_type, _ = await asyncio.gather(
        record_repo.download(id),
        record_repo.get_by_id(id),
        record_repo.set_loaded(id)
    )
    return paths, record_type


def evaluate(y_scores: np.ndarray, labels: dict, top_k: int) -> Tuple[list, list]:
    # indices of top k highest scores (unsorted)
    ind: np.ndarray = np.argpartition(y_scores, -top_k, axis=1)[:, -top_k:]
    # top k highest probalities (unsorted)
    probs: np.ndarray = np.take_along_axis(y_scores, ind, axis=1)
    # indices of top k highest scores (sorted)
    ind: np.ndarray = np.take_along_axis(
        ind, np.argsort(probs, axis=1), axis=1)
    # top k highest probalities (sorted)
    probs: np.ndarray = np.take_along_axis(y_scores, ind, axis=1) * (100/255)
    # class names of top k highest probalities
    classes = [labels[i] for i in ind[0]]
    # flatten probs and reverse order (highest first)
    probs = probs.flatten()[::-1]
    classes = classes[::-1]
    return probs.tolist(), classes


def interpreter_invoke(interpreter: tflite.Interpreter):
    start = time.perf_counter()
    interpreter.invoke()
    return (time.perf_counter() - start) * 1000


def classification(interpreter: tflite.Interpreter, labels: List[str], img_buffer: bytes, format: str):
    img = simplejpeg.decode_jpeg(img_buffer, fastdct=True) \
        if simplejpeg.is_jpeg(img_buffer) \
        else imageio.imread(img_buffer, format=format)
    input_index, input_shape, input_dtype = get_input_details(interpreter)
    output_index, output_shape, output_dtype = get_output_details(interpreter)
    img = cv2.resize(img, input_shape[:2], interpolation=cv2.INTER_AREA)
    img = np.expand_dims(img, axis=0)
    interpreter.set_tensor(input_index, img)
    inference_time = interpreter_invoke(interpreter)
    output_data = interpreter.get_tensor(output_index)
    probs, classes = evaluate(output_data, labels, 4)
    return {
        "probabilities": probs,
        "classes": classes,
        "inferenceTime": inference_time
    }
