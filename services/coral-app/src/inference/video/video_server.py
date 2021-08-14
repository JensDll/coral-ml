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
from src.inference.video import video_models
from src.inference.video.common import new_fps_iter, print_fps
from zmq.asyncio import Context, Poller, Socket


class Settings(TypedDict):
    topK: int
    threshold: int


class CapProps(TypedDict):
    frame_width: int
    frame_height: int
    fps: int


def start_stream(cap_props: CapProps, config):
    return scripts.stream.start_stream(
        frame_width=cap_props["frame_width"],
        frame_height=cap_props["frame_height"],
        pix_fmt="rgb24",
        fps=cap_props["fps"],
        config=config,
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
    if hasattr(video_models, model_name):
        zutils.send_normalized_json(peer)
        return partial(getattr(video_models, model_name), interpreter)
    else:
        zutils.send_normalized_json(peer, errors=["This model is not supported"])
    return None


async def update_settings(socket: Socket, args: video_models.ModelArgs):
    settings: Settings = await socket.recv_json()
    args["top_k"] = settings["topK"]
    args["score_threshold"] = settings["threshold"]
    await socket.send(b"")


async def start(
    ctx: Context,
    load_model_peer: Socket,
    reset_peer: Socket,
    config: argparse.Namespace,
):
    update_settings_addr = f"tcp://*:{config.update_video_settings_port}"
    update_settings_socket: Socket = ctx.socket(zmq.REP)
    update_settings_socket.bind(update_settings_addr)
    logging.info(f"[VIDEO] (Update Settings) Bind to '{update_settings_addr}'")

    poller = Poller()
    poller.register(reset_peer, zmq.POLLIN)
    poller.register(load_model_peer, zmq.POLLIN)
    poller.register(update_settings_socket, zmq.POLLIN)

    cap = cv2.VideoCapture(0)
    cap_props: CapProps = {
        "frame_width": int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
        "frame_height": int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
        "fps": int(cap.get(cv2.CAP_PROP_FPS)),
    }

    process = start_stream(cap_props, config)

    fps_iter = new_fps_iter()
    run_inference = None
    args: video_models.ModelArgs = {"top_k": 1, "score_threshold": 0.1}

    # Signal video server ready
    await load_model_peer.send(b"")

    while True:
        try:
            items = dict(await poller.poll(0))
        except:
            break

        # Received reset signal
        if reset_peer in items:
            await reset_peer.recv()
            run_inference = None
            logging.info("[VIDEO] Reset")
            await reset_peer.send(b"")

        # Received load model signla
        if load_model_peer in items:
            run_inference = await receive_model(load_model_peer, args)

        # Received updare settings request
        if update_settings_socket in items:
            await update_settings(update_settings_socket, args)

        frame: np.ndarray = cap.read()[1]
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        if run_inference is not None:
            run_inference(args, frame=frame)

        print_fps(frame, fps_iter)

        try:
            process.stdin.write(frame.tobytes())
        except:
            process = next(restart_stream(cap_props, args))
