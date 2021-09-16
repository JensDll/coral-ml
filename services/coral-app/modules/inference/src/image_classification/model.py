from typing import Union, Tuple

import cv2 as cv
import numpy as np
import imageio
from zmq.asyncio import Socket

from modules import inference, core
from . import common

ImgBuffer = bytes
ImgFormat = str


class ImageClassificationModel(inference.BaseModel):
    cached_img: Union[core.types.Image, None] = None

    async def predict(
        self,
        socket: Socket,
        img_buffer: Union[Tuple[ImgBuffer, ImgFormat], None] = None,
        top_k: int = 5,
        score_threshold: float = 0.1,
    ) -> None:
        if not self.loaded:
            await core.zutils.send_normalized_json(
                socket,
                errors=["No model is loaded for this task"],
            )
            return None

        if img_buffer is not None:
            img = imageio.imread(img_buffer[0], img_buffer[1])
            input_size = self.interpreter.get_input_size(0)
            resized = cv.resize(img, input_size, interpolation=cv.INTER_AREA)
            resized = np.expand_dims(resized, axis=0)
            self.cached_img = resized
        elif self.cached_img is None:
            await core.zutils.send_normalized_json(
                socket,
                errors=["No model is loaded for this task"],
            )
            return None

        output_data, inference_time = common.invoke(self.interpreter, self.cached_img)
        probs, classes = common.evaluate(output_data, self.labels, top_k)

        result = {
            "probabilities": probs,
            "classes": classes,
            "inferenceTime": inference_time,
        }

        await core.zutils.send_normalized_json(socket, data=result)

    def reset(self):
        super().reset()
        self.cached_img = None
