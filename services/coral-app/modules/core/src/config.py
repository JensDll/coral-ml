import aiohttp
import zmq.asyncio


class CONFIG:
    class PORTS:
        MODEL_MANAGER = 7000
        IMAGE_CLASSIFICATION = 7100
        IMAGE_UPDATE_SETTINGS = 7101
        VIDEO_UPDATE_SETTINGS = 7200

    class URI:
        RECORD_API: str
        PUBLISH_VIDEO: str

    class FFMPEG:
        LOGLEVEL: str

    class HTTP:
        SESSION: aiohttp.ClientSession

    class ZMQ:
        CONTEXT: zmq.asyncio.Context
