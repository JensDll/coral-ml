from typing_extensions import Tuple
import numpy as np
import tflite_runtime.interpreter as tflite
import imageio
import src.common as common
import cv2
import time
from typing_extensions import TypedDict


class ModelArgs(TypedDict):
    img_buffer: bytes
    format: str
    model_name: str
    labels: dict
    top_k: int
    score_threshold: int


# EfficientNet family of models require unique input quantization:
# 1. Normalization: f = (r - mean) / std
# 2. Quantization: q = f / S + Z
# 3. q = (r - mean) / (std * S) + Z
# -------
# However, if std * scale equals 1, and mean - zero_point equals 0, the input
# does not need any preprocessing. But in practice, even if the results are
# very close to 1 and 0, it is probably okay to skip preprocessing for better
# efficiency. We use 1e-5 below instead of absolute zero.
def invoke_interpreter(
    interpreter: tflite.Interpreter, model_name: str, img: np.ndarray
):
    mean, std = 128, 128
    input_scale, input_zero_point = common.get_input_quant(interpreter, 0)

    # Apply quantization if necessary
    if (
        not abs(input_scale * std - 1) < 1e-5
        and not abs(mean - input_zero_point) < 1e-5
        and model_name.lower().startswith("efficientnet")
    ):
        # q = (r - mean) / (std * S) + Z
        img = (img - mean) / (std * input_scale) + input_zero_point
        np.clip(img, 0, 255, out=img)
        img = img.astype(common.get_input_dtype(interpreter, 0))

    # Set input tensor
    input_index = common.get_input_index(interpreter, 0)
    interpreter.set_tensor(input_index, img)

    # Invoke interpreter
    start = time.perf_counter()
    interpreter.invoke()
    inference_time = (time.perf_counter() - start) * 1000

    # Get output tensor
    output_data = common.get_output_tensor(interpreter, 0)

    # Dequantization if necessary
    if np.issubdtype(common.get_output_dtype(interpreter, 0), np.integer):
        output_scale, output_zero_point = common.get_output_quant(interpreter, 0)
        # r = S * (q - Z)
        output_data = output_scale * (output_data.astype(np.int64) - output_zero_point)

    return output_data, inference_time


def evaluate(y_scores: np.ndarray, labels: dict, top_k: int) -> Tuple[list, list]:
    if top_k == 0:
        return [], []
    y_scores = y_scores.flatten()
    # indices of top k highest scores (unsorted)
    ind: np.ndarray = np.argpartition(y_scores, -top_k)[-top_k:]
    # top k highest probalities (unsorted)
    probs: np.ndarray = np.take_along_axis(y_scores, ind, axis=0)
    # indices of top k highest scores (sorted)
    ind: np.ndarray = np.take_along_axis(ind, np.argsort(probs), axis=0)
    # top k highest probalities (sorted)
    probs: np.ndarray = np.take_along_axis(y_scores, ind, axis=0) * 100
    # class names of top k highest probalities
    classes = [labels[i] for i in ind]
    # flatten probs and reverse order (highest first)
    probs = probs[::-1]
    classes = classes[::-1]
    return probs.tolist(), classes


def generic_model(interpreter: tflite.Interpreter, args: ModelArgs):
    img = imageio.imread(args["img_buffer"], format=args["format"])
    input_size = common.get_input_size(interpreter, 0)
    resized = cv2.resize(img, input_size, interpolation=cv2.INTER_AREA)
    resized = np.expand_dims(resized, axis=0)
    output_data, inference_time = invoke_interpreter(
        interpreter, args["model_name"], resized
    )
    probs, classes = evaluate(output_data, args["labels"], args["top_k"])
    return {"probabilities": probs, "classes": classes, "inferenceTime": inference_time}
