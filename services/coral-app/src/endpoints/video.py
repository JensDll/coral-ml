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
from src import annotation
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


def start_stream(cap_props: CapProps, publish_uri):
    return scripts.stream.start_stream(
        frame_width=cap_props["frame_width"],
        frame_height=cap_props["frame_height"],
        pix_fmt="rgb24",
        fps=cap_props["fps"],
        publish_uri=publish_uri,
    )


def restart_stream(cap_props: CapProps, intervall=4):
    logging.error("FFMPEG Error")
    logging.error(traceback.format_exc())
    while True:
        time.sleep(intervall)
        logging.info("Restarting Stream")
        try:
            yield start_stream(cap_props)
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
    reply.send(b"")


async def start(
    ctx: Context,
    load_model_peer: zmq.Socket,
    reset_peer: zmq.Socket,
    args: argparse.Namespace,
):
    reply_addr = f"tcp://*:{args.video_port}"
    reply = ctx.socket(zmq.REP)
    reply.bind(reply_addr)
    logging.info(f"[VIDEO] (REP) Bind to '{reply_addr}'")

    poller = Poller()
    poller.register(reset_peer, zmq.POLLIN)
    poller.register(load_model_peer, zmq.POLLIN)
    poller.register(reply, zmq.POLLIN)

    cap = cv2.VideoCapture(0)
    cap_props: CapProps = {
        "frame_width": int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
        "frame_height": int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
        "fps": int(cap.get(cv2.CAP_PROP_FPS)),
    }

    process = start_stream(
        cap_props,
        publish_uri=args.publish_uri,
    )

    fps_iter = annotation.fps_iter()
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

        if reply in items:
            await update_args(reply, model_args)

        frame: np.ndarray = cap.read()[1]
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        if run_inference is not None:
            run_inference(model_args, frame=frame)

        annotation.print_fps(frame, fps_iter)

        try:
            process.stdin.write(frame.tobytes())
        except:
            process = next(restart_stream(cap_props))
