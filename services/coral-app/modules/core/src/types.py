from collections.abc import Coroutine
from typing import Tuple, TypedDict, Any, Literal, Union, Callable

import numpy as np

Id = Union[str, int]
RecordType = Literal["Image Classification", "Object Detection"]
Labels = dict[int, str]
InputSize = Tuple[int, int]
Image = np.ndarray


class NormalizedJson(TypedDict):
    success: bool
    errors: list[str]
    data: Any


class Record(TypedDict):
    id: int
    modelFileName: str
    recordTypeId: int
    recordType: RecordType


class LoadModelResult(TypedDict):
    success: bool
    modelPath: str
    labelPath: str
    record: Record


LoadModelHandlers = dict[
    RecordType, Callable[[LoadModelResult], Coroutine[Any, Any, NormalizedJson]]
]


class CapProps(TypedDict):
    frameWidth: int
    frameHeight: int
    fps: int


class ModelSettings(TypedDict):
    topK: int
    threshold: int


class ClassificationResult(TypedDict):
    probabilities: list[float]
    classes: list[str]
    inferenceTime: float
