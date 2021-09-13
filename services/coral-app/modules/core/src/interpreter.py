import tflite_runtime.interpreter as tflite
import numpy as np
from typing import Tuple
from . import typedef


class Interpreter(tflite.Interpreter):
    def get_output_shape(self, i: int):
        return self.get_output_details()[i]["shape"]

    def get_output_dtype(self, i: int):
        return self.get_output_details()[i]["dtype"]

    def get_output_tensor(self, i: int) -> np.ndarray:
        output_index = self.get_output_details()[i]["index"]
        return self.tensor(output_index)()

    def get_output_quant(self, i: int) -> Tuple[float, float]:
        return self.get_output_details()[i]["quantization"]

    def get_num_outputs(self):
        return len(self.get_output_details())

    def get_input_size(self, i: int) -> typedef.InputSize:
        _, height, width, _ = self.get_input_details()[i]["shape"]
        return width, height

    def get_input_index(self, i: int):
        return self.get_input_details()[i]["index"]

    def get_input_dtype(self, i: int):
        return self.get_input_details()[i]["dtype"]

    def get_input_quant(self, i) -> Tuple[float, float]:
        return self.get_input_details()[i]["quantization"]
