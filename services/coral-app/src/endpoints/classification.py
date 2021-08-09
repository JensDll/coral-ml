import argparse
from typing_extensions import TypedDict
from typing import List
import zmq
from zmq.asyncio import Context, Poller
import tflite_runtime.interpreter as tflite
import logging

from src.inference.classification.classify import classify
from src import common


class Message(TypedDict):
    success: bool
    errors: List[str]
    data: any


async def start(
    ctx: Context, img_peer: zmq.Socket, reset_peer: zmq.Socket, args: argparse.Namespace
):
    reply_addr = f"tcp://*:{args.classify_port}"
    reply = ctx.socket(zmq.REP)
    reply.bind(reply_addr)
    logging.info(f"[CLASSIFICATION] (REP) Bind to '{reply_addr}'")

    poller = Poller()
    poller.register(reset_peer, zmq.POLLIN)
    poller.register(reply, zmq.POLLIN)
    poller.register(img_peer, zmq.POLLIN)

    labels: dict = None
    interpreter: tflite.Interpreter = None

    img_peer.send(b"")

    while True:
        try:
            items = dict(await poller.poll())
        except:
            break

        if reset_peer in items:
            await reset_peer.recv()
            interpreter = None
            logging.info("[CLASSIFICATION] Reset")
            reset_peer.send(b"")

        if img_peer in items:
            json = await img_peer.recv_json()
            labels = common.load_labels(json["label_path"])
            interpreter = common.load_interpreter(json["model_path"])
            logging.info("[CLASSIFICATION] Received Interpreter - Sending response ...")
            img_peer.send(b"")

        if reply in items:
            img_buffer: bytes
            format: bytes
            img_buffer, format = await reply.recv_multipart()

            msg: Message = {"success": False, "errors": [], "data": None}

            if interpreter == None:
                msg["errors"].append("No model is loaded for this task")
                await reply.send_json(msg)
            else:
                format = format.decode()

                try:
                    results = classify(
                        interpreter=interpreter,
                        labels=labels,
                        img_buffer=img_buffer,
                        format=format,
                    )
                    msg["data"] = results
                    msg["success"] = True
                except Exception as e:
                    msg["errors"].append(str(e))

                await reply.send_json(msg)
