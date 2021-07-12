from os import path
import pathlib
from typing import List, Literal, Tuple
import aiohttp
import tflite_runtime.interpreter as tflite
import platform
import cv2
import numpy as np
import src.repositories as repos
import simplejpeg
import imageio

EDGETUP_LIB = {
    'Linux': 'libedgetpu.so.1',
    'Darwin': 'libedgetpu.1.dylib',
    'Windows': 'edgetpu.dll'
}[platform.system()]


def read_input_details(interpreter: tflite.Interpreter):
    input_details = interpreter.get_input_details()[0]
    input_shape = input_details["shape"][1:]
    input_dtype = input_details["dtype"]
    return input_shape, input_dtype


def load_labels(label_path: pathlib.Path):
    with label_path.open("r") as f:
        return [line.strip() for line in f.readlines()]


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
    return await record_repo.get_by_id(id)


async def classification(interpreter: tflite.Interpreter, labels: List[str], img_buffer: bytes, format: str):
    img = simplejpeg.decode_jpeg(img_buffer, fastdct=True) \
        if simplejpeg.is_jpeg(img_buffer) \
        else imageio.imread(img_buffer, format=format)
    input_shape, input_dtype = read_input_details(interpreter)
    print(input_shape)
    print(input_dtype)
