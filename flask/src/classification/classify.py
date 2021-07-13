from typing_extensions import Tuple
import numpy as np
import tflite_runtime.interpreter as tflite
import simplejpeg
import imageio
import src.common as common
import cv2


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


def classify(interpreter: tflite.Interpreter, labels: dict, img_buffer: bytes, format: str):
    img = simplejpeg.decode_jpeg(img_buffer, fastdct=True) \
        if simplejpeg.is_jpeg(img_buffer) \
        else imageio.imread(img_buffer, format=format)
    input_size = common.get_input_size(interpreter)
    resized = cv2.resize(img, input_size, interpolation=cv2.INTER_AREA)
    inference_time = common.interpreter_invoke(interpreter, resized)
    output_data = common.get_output_tensor(interpreter, 0)
    probs, classes = evaluate(output_data, labels, 4)
    return {
        "probabilities": probs,
        "classes": classes,
        "inferenceTime": inference_time
    }
