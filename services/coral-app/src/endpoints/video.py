from typing_extensions import TypedDict
import cv2
import argparse
import zmq
from zmq.asyncio import Context, Poller
import tflite_runtime.interpreter as tflite
import logging
import time
import traceback

import src.detection.detect as detect
import src.common as common
import src.zutils as zutils
import src.annotation as annotation
import scripts.stream


class Settings(TypedDict):
    topK: int
    threshold: int


def start_stream(frame_width, frame_height, fps, publish_uri):
    return scripts.stream.start_stream(
        frame_width=frame_width,
        frame_height=frame_height,
        pix_fmt="rgb24",
        fps=fps,
        publish_uri=publish_uri,
    )


async def start(
    ctx: Context,
    video_peer: zmq.Socket,
    reset_peer: zmq.Socket,
    args: argparse.Namespace,
):
    reply_addr = f"tcp://*:{args.video_port}"
    reply = ctx.socket(zmq.REP)
    reply.bind(reply_addr)
    logging.info(f"[VIDEO] (REP) Bind to '{reply_addr}'")

    poller = Poller()
    poller.register(reset_peer, zmq.POLLIN)
    poller.register(video_peer, zmq.POLLIN)
    poller.register(reply, zmq.POLLIN)

    cap = cv2.VideoCapture(0)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    process = start_stream(
        frame_width=frame_width,
        frame_height=frame_height,
        fps=fps,
        publish_uri=args.publish_uri,
    )

    fps_iter = annotation.fps_iter()
    interpreter: tflite.Interpreter = None
    labels: dict = None
    settings: Settings = {"topK": 1, "threshold": 0.1}

    await video_peer.send(b"")

    while True:
        try:
            items = dict(await poller.poll(0))
        except:
            break

        if reset_peer in items:
            await reset_peer.recv()
            interpreter = None
            logging.info("[VIDEO] Reset")
            reset_peer.send(b"")

        if video_peer in items:
            interpreter, labels = await zutils.recv_interpreter(video_peer)
            logging.info("[VIDEO] Received Interpreter - Sending response ...")
            video_peer.send(b"")

        if reply in items:
            settings: Settings = await reply.recv_json()
            reply.send(b"")

        frame = cap.read()[1]
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        if interpreter is not None:
            input_size = common.get_input_size(interpreter)
            resized = cv2.resize(frame, input_size, interpolation=cv2.INTER_AREA)
            common.invoke_interpreter(interpreter, resized)
            detections = detect.get_detections(
                interpreter, score_threshold=settings["threshold"]
            )[: settings["topK"]]
            frame = detect.append_detection_to_img(
                img=frame, input_size=input_size, detections=detections, labels=labels
            )

        annotation.print_fps(frame, fps_iter)

        try:
            process.stdin.write(frame.tobytes())
        except:
            logging.error("FFMPEG Error")
            logging.error(traceback.format_exc())
            while True:
                time.sleep(4)
                logging.info("Restarting Stream")
                try:
                    process = start_stream(
                        frame_width=frame_width,
                        frame_height=frame_height,
                        fps=fps,
                        publish_uri=args.publish_uri,
                    )
                    break
                except:
                    pass
