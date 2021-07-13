import cv2
import simplejpeg
import argparse
import zmq
from zmq.asyncio import Context, Poller
import tflite_runtime.interpreter as tflite

import src.detection.detect as detect
import src.common as common
import src.zutils as zutils


async def start(ctx: Context, video_peer: zmq.Socket, args: argparse.Namespace):
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
    interpreter: tflite.Interpreter = None
    labels: dict = None

    await video_peer.send(b"")

    fps_iter = common.fps_iter()

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
            interpreter, labels = await zutils.recv_interpreter(video_peer)
            print("[PUBLISHER] Received Interpreter - Sending response ...")
            video_peer.send(b"")

        has_frame, frame = camera_src.read()

        if not has_frame:
            break

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        if interpreter is not None:
            input_size = common.get_input_size(interpreter)
            resized = cv2.resize(
                frame, input_size, interpolation=cv2.INTER_AREA)
            inference_time = common.interpreter_invoke(interpreter, resized)
            detections = detect.get_detections(interpreter)
            frame = detect.append_detection_to_img(
                img=frame,
                input_size=input_size,
                detections=detections,
                labels=labels
            )

        common.print_fps(frame, fps_iter)

        jpg = simplejpeg.encode_jpeg(
            frame, quality=95, colorspace="rgb", fastdct=True)

        publisher.send(jpg, copy=False)

    reset.close()
    video_peer.close()
    publisher.close()
