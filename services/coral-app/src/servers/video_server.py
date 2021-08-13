import cv2
import argparse
import zmq
import logging
import time
import traceback
import scripts.stream
import numpy as np

from typing_extensions import TypedDict
from functools import partial
from src import common, zutils
from src.inference.video import models
from src.inference.video.models import VideoModelArgs
from zmq.asyncio import Context, Poller, Socket


class Settings(TypedDict):
    topK: int
    threshold: int


class CapProps(TypedDict):
    frame_width: int
    frame_height: int
    fps: int


def new_fps_iter():
    prev = time.time()
    yield 0.0  # First fps value
    while True:
        curr = time.time()
        diff = curr - prev
        fps = 1 / diff
        prev = curr
        yield fps


def print_fps(img: np.ndarray, fps_iter):
    fps = next(fps_iter)

    cv2.putText(
        img,
        "FPS: {:.2f}".format(fps),
        (30, 30),
        fontFace=1,
        fontScale=cv2.FONT_HERSHEY_PLAIN,
        color=(0, 245, 0),
        thickness=1,
        lineType=cv2.LINE_AA,
    )


def start_stream(cap_props: CapProps, args):
    return scripts.stream.start_stream(
        frame_width=cap_props["frame_width"],
        frame_height=cap_props["frame_height"],
        pix_fmt="rgb24",
        fps=cap_props["fps"],
        args=args,
    )


def restart_stream(cap_props: CapProps, args, intervall=4):
    logging.error("FFMPEG Error")
    logging.error(traceback.format_exc())
    while True:
        time.sleep(intervall)
        logging.info("Restarting Stream")
        try:
            yield start_stream(cap_props, args)
            break
        except:
            pass


async def receive_model(peer: Socket, model_args):
    logging.info("[VIDEO] Received Interpreter")
    json = await peer.recv_json()
    model_args["labels"] = common.load_labels(json["label_path"])
    interpreter = common.load_interpreter(json["model_path"])
    model_name = json["model_file_name"]
    logging.info("[VIDEO] Sending Response ...")
    if hasattr(models, model_name):
        zutils.send_normalized_json(peer)
        return partial(getattr(models, model_name), interpreter)
    else:
        zutils.send_normalized_json(peer, errors=["This model is not supported"])
    return None


async def update_args(reply: Socket, model_args):
    settings: Settings = await reply.recv_json()
    model_args["top_k"] = settings["topK"]
    model_args["score_threshold"] = settings["threshold"]
    await reply.send(b"")


async def start(
    ctx: Context,
    load_model_peer: Socket,
    reset_peer: Socket,
    args: argparse.Namespace,
):
    video_server_addr = f"tcp://*:{args.video_server_port}"
    video_server = ctx.socket(zmq.REP)
    video_server.bind(video_server_addr)
    logging.info(f"[VIDEO] (REP) Bind to '{video_server_addr}'")

    poller = Poller()
    poller.register(reset_peer, zmq.POLLIN)
    poller.register(load_model_peer, zmq.POLLIN)
    poller.register(video_server, zmq.POLLIN)

    cap = cv2.VideoCapture(0)
    cap_props: CapProps = {
        "frame_width": int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
        "frame_height": int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
        "fps": int(cap.get(cv2.CAP_PROP_FPS)),
    }

    process = start_stream(cap_props, args)

    fps_iter = new_fps_iter()
    run_inference = None
    model_args: VideoModelArgs = {
        "top_k": 1,
        "score_threshold": 0.1,
        "labels": None,
    }

    load_model_peer.send(b"")

    while True:
        try:
            items = dict(await poller.poll(0))
        except:
            break

        if reset_peer in items:
            await reset_peer.recv()
            run_inference = None
            logging.info("[VIDEO] Reset")
            reset_peer.send(b"")

        if load_model_peer in items:
            run_inference = await receive_model(load_model_peer, model_args)

        if video_server in items:
            await update_args(video_server, model_args)

        frame: np.ndarray = cap.read()[1]
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        if run_inference is not None:
            run_inference(model_args, frame=frame)

        print_fps(frame, fps_iter)

        try:
            process.stdin.write(frame.tobytes())
        except:
            process = next(restart_stream(cap_props, args))
