import asyncio
from asyncio.windows_events import WindowsSelectorEventLoopPolicy
import pathlib
from typing import List, TypedDict
import zmq
from zmq.asyncio import Context, Poller
import cv2
import simplejpeg
import argparse
import threading
import random
import string
import aiohttp
import signal
import tflite_runtime.interpreter as tflite
import platform

import src.coral as coral
import src.zutils as zutils

parser = argparse.ArgumentParser()
parser.add_argument("--pub_port", default=5500, type=int)
parser.add_argument("--manager_port", default=5600, type=int)
parser.add_argument("--classification_port", default=5700, type=int)
parser.add_argument("--api", default="http://localhost:5000/api", type=str)
args = parser.parse_args()


class Message(TypedDict):
    success: bool
    errors: List[str]
    data: any


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
            video_peer.send(b"")

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

    interpreter: tflite.Interpreter = None
    labels: List[str] = None

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
            model_path: bytes
            label_path: bytes
            model_path, label_path = await img_peer.recv_multipart()
            model_path = pathlib.Path(model_path.decode())
            label_path = pathlib.Path(label_path.decode())
            interpreter, labels = coral.get_interpreter(model_path, label_path)
            img_peer.send(b"")

        if reply in items:
            img_buffer: bytes
            format: bytes
            img_buffer, format = await reply.recv_multipart()

            msg: Message = {
                "success": True,
                "errors": [],
                "data": None
            }

            if interpreter == None:
                msg["success"] = False
                msg["errors"].append("No model is loaded for this task")
                await reply.send_json(msg)
            else:
                format = format.decode()

                results = coral.classification(
                    interpreter=interpreter,
                    labels=labels,
                    img_buffer=img_buffer,
                    format=format
                )

                msg["success"] = True
                msg["data"] = results

                await reply.send_json(msg)


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
            (model_path, label_path), record_type = await coral.load_model(record_repo, id)
            print(record_type)
            await reset.send(b"")
            model_path = str(model_path).encode()
            label_path = str(label_path).encode()

            model_type = True  # TODO get model type here

            if model_type:
                await img_pipe.send_multipart([model_path, label_path])
                await img_pipe.recv()
            else:
                await video_pipe.send_multipart([model_path, label_path])
                await video_pipe.recv()
        except Exception as e:
            print("Error loading model")
            print(e)
            success = False
        await reply.send(zutils.encode_bool(success))


async def main():
    ctx = Context()

    img_pipe, img_peer = zutils.pipe(ctx)
    video_pipe, video_peer = zutils.pipe(ctx)

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
