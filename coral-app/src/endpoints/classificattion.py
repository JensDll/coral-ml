import argparse
from typing_extensions import TypedDict
from typing import List
import zmq
from zmq.asyncio import Context, Poller
import tflite_runtime.interpreter as tflite
import src.zutils as zutils
import src.classification.classify as classify
import logging


class Message(TypedDict):
    success: bool
    errors: List[str]
    data: any


async def start(ctx: Context, img_peer: zmq.Socket, args: argparse.Namespace):
    reply_addr = f"tcp://*:{args.classification_port}"
    reply = ctx.socket(zmq.REP)
    reply.bind(reply_addr)
    logging.info(f"[CLASSIFICATION] (REP) Bind to '{reply_addr}'")

    reset = ctx.socket(zmq.SUB)
    reset.connect("tcp://localhost:6666")
    reset.setsockopt(zmq.SUBSCRIBE, b"")

    poller = Poller()
    poller.register(reset, zmq.POLLIN)
    poller.register(reply, zmq.POLLIN)
    poller.register(img_peer, zmq.POLLIN)

    interpreter: tflite.Interpreter = None
    labels: dict = None

    await img_peer.send(b"")

    while True:
        try:
            items = dict(await poller.poll())
        except:
            break

        if reset in items:
            await reset.recv()
            interpreter = None
            logging.info("[CLASSIFICATION] Reset")

        if img_peer in items:
            interpreter, labels = await zutils.recv_interpreter(img_peer)
            logging.info("[CLASSIFICATION] Received Interpreter - Sending response ...")
            img_peer.send(b"")

        if reply in items:
            img_buffer: bytes
            format: bytes
            img_buffer, format = await reply.recv_multipart()

            msg: Message = {"success": True, "errors": [], "data": None}

            if interpreter == None:
                msg["success"] = False
                msg["errors"].append("No model is loaded for this task")
                await reply.send_json(msg)
            else:
                format = format.decode()

                results = classify.classify(
                    interpreter=interpreter,
                    labels=labels,
                    img_buffer=img_buffer,
                    format=format,
                )

                msg["success"] = True
                msg["data"] = results

                await reply.send_json(msg)
