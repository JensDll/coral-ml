from collections.abc import Coroutine
from typing import Tuple, TypeVar, TypedDict, Any, Literal, Union, Callable

Id = Union[str, int]
RecordType = Literal["Image Classification", "Object Detection"]
Labels = dict[int, str]
InputSize = Tuple[int, int]

TRunInferenceResult = TypeVar("TRunInferenceResult")
RunInference = Callable[..., None]


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


class ModelSettings(TypedDict):
    topK: int
    threshold: int


class CapProps(TypedDict):
    frameWidth: int
    frameHeight: int
    fps: int


LoadModelHandlers = dict[
    RecordType, Callable[[LoadModelResult], Coroutine[Any, Any, NormalizedJson]]
]
