from typing import Union, Tuple

import zmq.asyncio
import cv2 as cv
import numpy as np
import imageio
import time

from modules import inference, core
from . import common

ImgBuffer = bytes
ImgFormat = str


class ImageClassificationModel(inference.BaseModel):
    cached_img: Union[np.ndarray, None] = None

    @property
    def has_cache(self):
        return self.cached_img is not None

    def predict(
        self,
        img_buffer: Union[Tuple[ImgBuffer, ImgFormat], None] = None,
        top_k: int = 5,
        score_threshold: float = 0.1,
    ) -> core.types.ClassificationResult:
        if img_buffer is not None:
            img = imageio.imread(img_buffer[0], img_buffer[1])
            input_size = self.interpreter.get_input_size(0)
            resized = cv.resize(img, input_size, interpolation=cv.INTER_AREA)
            resized = np.expand_dims(resized, axis=0)
            self.cached_img = resized

        output_data, inference_time = common.invoke(self.interpreter, self.cached_img)
        probs, classes = common.evaluate(output_data, self.labels, top_k)

        return {
            "probabilities": probs,
            "classes": classes,
            "inferenceTime": inference_time,
        }

    def reset(self):
        super().reset()
        self.cached_img = None
