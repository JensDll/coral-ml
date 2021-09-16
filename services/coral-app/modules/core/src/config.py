import os

import aiohttp
from zmq.asyncio import Context


class Config:
    class Ports:
        MODEL_MANAGER = int(os.getenv("CORAL_PORT_MODEL_MANAGER"))  # type: ignore
        IMAGE_CLASSIFICATION = int(os.getenv("CORAL_PORT_IMAGE_CLASSIFICATION"))  # type: ignore
        IMAGE_UPDATE_SETTINGS = int(os.getenv("CORAL_PORT_IMAGE_SETTINGS"))  # type: ignore
        VIDEO_UPDATE_SETTINGS = int(os.getenv("CORAL_PORT_VIDEO_SETTINGS"))  # type: ignore

    class Uri:
        RECORD_API = os.getenv("RECORD_API_URI")  # type: ignore
        PUBLISH_VIDEO = os.getenv("NODE_API_URI")  # type: ignore

    class FFmpeg:
        LOGLEVEL: str

    class Http:
        SESSION: aiohttp.ClientSession

    class Zmq:
        CONTEXT: Context
