import uuid
from typing import Any

import zmq
from zmq.asyncio import Socket

from modules import core


def pipe():
    a: Socket = core.Config.Zmq.CONTEXT.socket(zmq.PAIR)
    b: Socket = core.Config.Zmq.CONTEXT.socket(zmq.PAIR)
    a.linger = b.linger = 0
    a.hwm = b.hwm = 1
    inproc = f"inproc://{uuid.uuid4()}"
    a.bind(inproc)
    b.connect(inproc)
    return a, b


def encode_bool(bool: bool):
    return bool.to_bytes(1, "big")


def send_message_envelope(
    socket: Socket,
    data: Any = [],
    errors: list[str] = [],
):
    json: core.types.MessageEnvelope = {
        "success": False,
        "data": data,
        "errors": errors,
    }
    json["success"] = len(json["errors"]) == 0
    return socket.send_json(json)
