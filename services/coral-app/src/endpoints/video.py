from typing_extensions import TypedDict
import cv2
import argparse
import zmq
from zmq.asyncio import Context, Poller
import tflite_runtime.interpreter as tflite
import logging

import src.detection.detect as detect
import src.common as common
import src.zutils as zutils
import src.annotation as annotation
import scripts.stream


class Message(TypedDict):
    topK: int
    threshold: int


async def start(ctx: Context, video_peer: zmq.Socket, args: argparse.Namespace):
    # reset signal
    reset = ctx.socket(zmq.SUB)
    reset.connect("tcp://localhost:7777")
    reset.setsockopt(zmq.SUBSCRIBE, b"")

    reply_addr = f"tcp://*:{args.video_port}"
    reply = ctx.socket(zmq.REP)
    reply.bind(reply_addr)
    logging.info(f"[VIDEO] (REP) Bind to '{reply_addr}'")

    poller = Poller()
    poller.register(reset, zmq.POLLIN)
    poller.register(video_peer, zmq.POLLIN)
    poller.register(reply, zmq.POLLIN)

    cap = cv2.VideoCapture(0)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    process = scripts.stream.start_stream(
        frame_width=frame_width,
        frame_height=frame_height,
        pix_fmt="rgb24",
        fps=fps,
        publish_uri=args.publish_uri,
    )

    fps_iter = annotation.fps_iter()
    interpreter: tflite.Interpreter = None
    labels: dict = None
    msg: Message = {"topK": 1, "threshold": 0.1}

    await video_peer.send(b"")

    while True:
        try:
            items = dict(await poller.poll(0))
        except:
            break

        if reset in items:
            await reset.recv()
            interpreter = None
            logging.info("[VIDEO] Reset")

        if video_peer in items:
            interpreter, labels = await zutils.recv_interpreter(video_peer)
            logging.info("[VIDEO] Received Interpreter - Sending response ...")
            video_peer.send(b"")

        if reply in items:
            msg: Message = await reply.recv_json()
            reply.send(b"")

        has_frame, frame = cap.read()

        if not has_frame:
            break

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        if interpreter is not None:
            input_size = common.get_input_size(interpreter)
            resized = cv2.resize(frame, input_size, interpolation=cv2.INTER_AREA)
            common.invoke_interpreter(interpreter, resized)
            detections = detect.get_detections(
                interpreter, score_threshold=msg["threshold"]
            )[: msg["topK"]]
            frame = detect.append_detection_to_img(
                img=frame, input_size=input_size, detections=detections, labels=labels
            )

        annotation.print_fps(frame, fps_iter)

        process.stdin.write(frame.tobytes())
