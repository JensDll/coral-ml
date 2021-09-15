import aiohttp
from zmq.asyncio import Context


class Config:
    class Ports:
        MODEL_MANAGER = 7000
        IMAGE_CLASSIFICATION = 7100
        IMAGE_UPDATE_SETTINGS = 7101
        VIDEO_UPDATE_SETTINGS = 7200

    class Uri:
        RECORD_API: str
        PUBLISH_VIDEO: str

    class FFmpeg:
        LOGLEVEL: str

    class Http:
        SESSION: aiohttp.ClientSession

    class Zmq:
        CONTEXT: Context
