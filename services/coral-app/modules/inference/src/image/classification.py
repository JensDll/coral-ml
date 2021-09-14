from typing import TypedDict, Tuple, Union

import numpy as np
import imageio
import cv2
import time

from modules import core


class ModelArgs(TypedDict):
    imgBuffer: bytes
    format: str
    modelFileName: str
    labels: dict
    imgResized: Union[np.ndarray, None]
    topK: int
    scoreThreshold: float


class ClassificationResult(TypedDict):
    probabilities: list[float]
    classes: list[str]
    inferenceTime: float


# EfficientNet family of models require unique input quantization:
# 1. Normalization: f = (r - mean) / std
# 2. Quantization: q = f / S + Z
# 3. q = (r - mean) / (std * S) + Z
# However, if std * scale equals 1, and mean - zero_point equals 0, the input
# does not need any preprocessing. But in practice, even if the results are
# very close to 1 and 0, it is probably okay to skip preprocessing for better
# efficiency. We use 1e-5 below instead of absolute zero.
def invoke_interpreter(interpreter: core.Interpreter, model_name: str, img: np.ndarray):
    mean, std = 128, 128
    input_scale, input_zero_point = interpreter.get_input_quant(0)

    print(model_name.lower().startswith("efficientnet"))
    # Apply quantization if necessary
    if (
        model_name.lower().startswith("efficientnet")
        and not abs(input_scale * std - 1) < 1e-5
        and not abs(mean - input_zero_point) < 1e-5
    ):
        # q = (r - mean) / (std * S) + Z
        img = (img - mean) / (std * input_scale) + input_zero_point
        np.clip(img, 0, 255, out=img)
        img = img.astype(interpreter.get_input_dtype(0))

    # Set input tensor
    input_index = interpreter.get_input_index(0)
    interpreter.set_tensor(input_index, img)

    # Invoke interpreter
    start = time.perf_counter()
    interpreter.invoke()
    inference_time = (time.perf_counter() - start) * 1000

    # Get output tensor
    output_data = interpreter.get_output_tensor(0)

    # Dequantization if necessary
    if np.issubdtype(interpreter.get_output_dtype(0), np.integer):
        output_scale, output_zero_point = interpreter.get_output_quant(0)
        # r = S * (q - Z)
        output_data = output_scale * (output_data.astype(np.int64) - output_zero_point)

    return output_data, inference_time


def evaluate(y_scores: np.ndarray, labels: dict, top_k: int) -> Tuple[list, list]:
    if top_k == 0:
        return [], []
    y_scores = y_scores.flatten()
    # Indices of top k highest scores (unsorted)
    ind: np.ndarray = np.argpartition(y_scores, -top_k)[-top_k:]
    # Top k highest probalities (unsorted)
    probs: np.ndarray = np.take_along_axis(y_scores, ind, axis=0)
    # Indices of top k highest scores (sorted)
    ind: np.ndarray = np.take_along_axis(ind, np.argsort(probs), axis=0)
    # Top k highest probalities (sorted)
    probs: np.ndarray = np.take_along_axis(y_scores, ind, axis=0) * 100
    # Class names of top k highest probalities
    classes = [labels[i] for i in ind]
    # Reverse order (highest first)
    probs = probs[::-1]
    classes = classes[::-1]
    return probs.tolist(), classes


def generic_model(
    interpreter: core.Interpreter, args: ModelArgs
) -> ClassificationResult:
    # Check if an image is already cached
    if args["imgResized"] is None:
        img = imageio.imread(args["imgBuffer"], format=args["format"])
        input_size = interpreter.get_input_size(0)
        resized = cv2.resize(img, input_size, interpolation=cv2.INTER_AREA)
        resized = np.expand_dims(resized, axis=0)
        args["imgResized"] = resized

    output_data, inference_time = invoke_interpreter(
        interpreter,
        model_name=args["modelFileName"],
        img=args["imgResized"],
    )
    probs, classes = evaluate(output_data, args["labels"], args["topK"])

    return {"probabilities": probs, "classes": classes, "inferenceTime": inference_time}
