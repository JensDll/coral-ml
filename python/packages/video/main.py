import asyncio
from asyncio.windows_events import WindowsSelectorEventLoopPolicy
import pathlib
from typing import List
import zmq
from zmq.asyncio import Context, Poller
import cv2
import simplejpeg
import argparse
import traceback
import sys
import threading
import random
import string
import aiohttp
import signal
import tflite_runtime.interpreter as tflite
import platform
import pickle

from zmq.backend import has

import src.coral as coral

parser = argparse.ArgumentParser()
parser.add_argument("--pub_port", default=5500, type=int)
parser.add_argument("--manager_port", default=5600, type=int)
parser.add_argument("--classification_port", default=5700, type=int)
parser.add_argument("--api", default="http://localhost:5000/api", type=str)
args = parser.parse_args()


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


async def publisher(ctx: Context, video_peer: zmq.Socket):
    publisher_addr = f"tcp://*:{args.pub_port}"
    publisher = ctx.socket(zmq.PUB)
    publisher.bind(publisher_addr)
    print(f"[PUBLISHER] (PUB) Bind to '{publisher_addr}'")

    # Subscribe to reset signal
    reset = ctx.socket(zmq.SUB)
    reset.connect("tcp://localhost:6666")
    reset.setsockopt(zmq.SUBSCRIBE, b"")

    poller = Poller()
    poller.register(reset, zmq.POLLIN)
    poller.register(video_peer, zmq.POLLIN)

    camera_src = cv2.VideoCapture(0)
    interpreter: tflite.Interpreter

    await video_peer.send(b"")

    while True:
        try:
            items = dict(await poller.poll(0))
        except:
            break

        if reset in items:
            await reset.recv()
            interpreter = None
            print("[PUBLISHER] Reset")

        if video_peer in items:
            interpreter, label_path = await video_peer.recv_multipart()
            print(label_path)

        has_frame, frame = camera_src.read()

        if not has_frame:
            break

        jpg = simplejpeg.encode_jpeg(
            frame, quality=95, colorspace="bgr", fastdct=True)

        await publisher.send(jpg, copy=False)

    print("Closing")
    reset.close()
    video_peer.close()
    publisher.close()


async def classification(ctx: Context, img_peer: zmq.Socket):
    reply_addr = f"tcp://*:{args.classification_port}"
    reply = ctx.socket(zmq.REP)
    reply.bind(reply_addr)
    print(f"[CLASSIFICATION] (REP) Bind to '{reply_addr}'")

    # Subscribe to reset signal
    reset = ctx.socket(zmq.SUB)
    reset.connect("tcp://localhost:6666")
    reset.setsockopt(zmq.SUBSCRIBE, b"")

    poller = Poller()
    poller.register(reset, zmq.POLLIN)
    poller.register(reply, zmq.POLLIN)
    poller.register(img_peer, zmq.POLLIN)

    interpreter: tflite.Interpreter
    labels: List[str]

    await img_peer.send(b"")

    while True:
        try:
            items = dict(await poller.poll())
        except:
            break

        if reset in items:
            await reset.recv()
            interpreter = None
            print("[CLASSIFICATION] Reset")

        if img_peer in items:
            model_path, label_path = await img_peer.recv_multipart()
            model_path = pathlib.Path(model_path.decode())
            label_path = pathlib.Path(label_path.decode())
            interpreter, labels = coral.get_interpreter(model_path, label_path)
            img_peer.send(b"")

        if reply in items:
            if interpreter == None:
                await reply.send_string("No model is loaded for this task")
            else:
                img_buffer: bytes
                format: bytes
                img_buffer, format = await reply.recv_multipart()
                format = format.decode("utf-8")

                await coral.classification(
                    interpreter=interpreter,
                    labels=labels,
                    img_buffer=img_buffer,
                    format=format
                )

                await reply.send_string("response")


async def model_manager(ctx: Context, video_pipe: zmq.Socket, img_pipe: zmq.Socket):
    reply_addr = f"tcp://*:{args.manager_port}"
    reply = ctx.socket(zmq.REP)
    reply.bind(reply_addr)
    print(f"[MODEL MANAGER] (REP) Bind to '{reply_addr}'")

    reset_addr = "tcp://*:6666"
    reset = ctx.socket(zmq.PUB)
    reset.bind(reset_addr)
    print(f"[MODEL MANAGER] (PUB) Bind to '{reset_addr}'")

    client = aiohttp.ClientSession()
    record_repo = coral.repos.RecordRepository(
        base_uri=args.api,
        client=client
    )

    await asyncio.gather(img_pipe.recv(), video_pipe.recv())

    print("[MODEL MANAGER] All Ready")

    while True:
        id = await reply.recv_string()
        success = True
        try:
            model_path, label_path = await coral.load_model(record_repo, id)
            await reset.send(b"")
            label_path = str(label_path).encode()
            model_path = str(model_path).encode()

            model_type = True  # TODO get model type here

            if model_type:
                await img_pipe.send_multipart([model_path, label_path])
                await img_pipe.recv()
            else:
                await video_pipe.send_multipart([model_path, label_path])
                await img_pipe.recv()
        except Exception as e:
            print("Error loading model")
            print(e)
            success = False
        await reply.send(success.to_bytes(1, "big"))


async def main():
    ctx = Context()

    img_pipe, img_peer = pipe(ctx)
    video_pipe, video_peer = pipe(ctx)

    publisher_thread = threading.Thread(
        target=asyncio.run,
        args=[publisher(ctx, video_peer)],
        daemon=True
    )
    publisher_thread.start()

    classification_thread = threading.Thread(
        target=asyncio.run,
        args=[classification(ctx, img_peer=img_peer)],
        daemon=True
    )
    classification_thread.start()

    signal.signal(signal.SIGINT, signal.SIG_DFL)

    await model_manager(
        ctx,
        img_pipe=img_pipe,
        video_pipe=video_pipe,
    )


if __name__ == "__main__":
    if platform.system() == "Windows":
        asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
