import random
import string
import zmq
import pathlib
from zmq.asyncio import Context, Socket
import src.common as common


def id_generator(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def pipe(ctx: Context):
    a = ctx.socket(zmq.PAIR)
    b = ctx.socket(zmq.PAIR)
    a.linger = b.linger = 0
    a.hwm = b.hwm = 1
    inproc = f"inproc://{id_generator(16)}"
    a.bind(inproc)
    b.connect(inproc)
    return a, b


def encode_bool(bool: bool):
    return bool.to_bytes(1, "big")


async def recv_interpreter(pipe: Socket):
    model_path: bytes
    label_path: bytes
    model_path, label_path = await pipe.recv_multipart()
    model_path = pathlib.Path(model_path.decode())
    label_path = pathlib.Path(label_path.decode())
    return common.interpreter_load(model_path, label_path)
