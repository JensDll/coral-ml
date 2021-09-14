import uuid
from typing import Any

import zmq
import zmq.asyncio

from modules import core


def pipe():
    a: zmq.asyncio.Socket = core.Config.Zmq.CONTEXT.socket(zmq.PAIR)
    b: zmq.asyncio.Socket = core.Config.Zmq.CONTEXT.socket(zmq.PAIR)
    a.linger = b.linger = 0
    a.hwm = b.hwm = 1
    inproc = f"inproc://{uuid.uuid4()}"
    a.bind(inproc)
    b.connect(inproc)
    return a, b


def encode_bool(bool: bool):
    return bool.to_bytes(1, "big")


def send_normalized_json(
    socket: zmq.asyncio.Socket,
    data: Any = [],
    errors: list[str] = [],
):
    json: core.typedef.NormalizedJson = {
        "success": False,
        "data": data,
        "errors": errors,
    }
    json["success"] = len(json["errors"]) == 0
    socket.send_json(json)
