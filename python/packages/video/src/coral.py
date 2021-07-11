import pathlib
import aiohttp
import tflite_runtime.interpreter as tflite
import platform

import src.repositories.tflite_record_repo as record_repo
from src.repositories.api_routes import ApiRoutes

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


def set_base_uri(base_uri: str):
    print(base_uri)
    ApiRoutes.base_uri = base_uri


async def load_model(session: aiohttp.ClientSession, id):
    print(id)
    try:
        model_path, label_path = await record_repo.get_by_id(session, id)
        labels = load_labels(label_path)
        delegate = tflite.load_delegate(EDGETUP_LIB)
        interpreter = tflite.Interpreter(
            model_path=str(model_path),
            experimental_delegates=[delegate]
        )
        interpreter.allocate_tensors()

        input_shape, input_dtype = read_input_details(interpreter)
        print(input_shape)
        print(input_dtype)
    except Exception as e:
        print(e)
