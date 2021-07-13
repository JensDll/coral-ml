import random
import string
import zmq
from zmq.asyncio import Context


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
