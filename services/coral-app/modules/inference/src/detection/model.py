import numpy as np

from modules import core, inference
from . import detection_nets


class DetectionModel(inference.BaseModel):
    def predict(
        self, img: core.types.Image, top_k: int = 5, score_threshold: float = 0.1
    ):
        if hasattr(detection_nets, self.interpreter.name):
            invoke = getattr(detection_nets, self.interpreter.name)
            invoke(
                self.interpreter,
                self.labels,
                img,
                top_k=top_k,
                score_threshold=score_threshold,
            )
