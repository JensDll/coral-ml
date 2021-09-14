import logging
import functools
from typing import Union

import zmq
import zmq.asyncio
import numpy as np

from modules import core, inference


async def load_model(
    load_model_peer: zmq.asyncio.Socket, args: inference.image.classification.ModelArgs
) -> core.types.RunInference:
    json: core.types.LoadModelResult = await load_model_peer.recv_json()
    logging.info("[CLASSIFICATION] Received Interpreter")
    args["labels"] = core.coral.load_labels(json["labelPath"])
    interpreter = core.coral.load_interpreter(json["modelPath"])
    args["modelFileName"] = json["record"]["modelFileName"]
    logging.info("[CLASSIFICATION] Sending Response ...")
    core.zutils.send_normalized_json(load_model_peer)
    return functools.partial(
        getattr(inference.image.classification, "generic_model"),
        interpreter=interpreter,
        args=args,
    )


def send_inference_results(
    socket: zmq.asyncio.Socket,
    run_inference: Union[
        core.types.RunInference,
        None,
    ],
):
    if run_inference == None:
        core.zutils.send_normalized_json(
            socket, errors=["No model is loaded for this task"]
        )
    else:
        try:
            results = run_inference()
            core.zutils.send_normalized_json(socket, data=results)
        except Exception as e:
            core.zutils.send_normalized_json(socket, errors=[str(e)])


async def start(reset_peer: zmq.asyncio.Socket, load_model_peer: zmq.asyncio.Socket):
    main_addr = f"tcp://*:{core.Config.Ports.IMAGE_CLASSIFICATION}"
    main_socket: zmq.asyncio.Socket = core.Config.Zmq.CONTEXT.socket(zmq.REP)
    main_socket.bind(main_addr)
    logging.info(f"[IMAGE SERVER] (Main) Bind to ({main_addr})")

    update_settings_addrs = f"tcp://*:{core.Config.Ports.IMAGE_UPDATE_SETTINGS}"
    update_settings_socket: zmq.asyncio.Socket = core.Config.Zmq.CONTEXT.socket(zmq.REP)
    update_settings_socket.bind(update_settings_addrs)
    logging.info(f"[IMAGE SERVER] (Update Settings) Bind to ({update_settings_addrs})")

    poller = zmq.asyncio.Poller()
    poller.register(reset_peer, zmq.POLLIN)
    poller.register(load_model_peer, zmq.POLLIN)
    poller.register(main_socket, zmq.POLLIN)
    poller.register(update_settings_socket, zmq.POLLIN)

    args: inference.image.classification.ModelArgs = {
        "imgBuffer": b"",
        "format": "str",
        "modelFileName": "str",
        "labels": dict(),
        "imgResized": None,
        "topK": 5,
        "scoreThreshold": 0.1,
    }
    run_inference: Union[core.types.RunInference, None] = None

    # Signal image server ready
    await load_model_peer.send(b"")

    while True:
        try:
            items = dict(await poller.poll())
        except:
            break

        if reset_peer in items:
            await reset_peer.recv()
            run_inference = None
            logging.info("[IMAGE SERVER] Reset")
            await reset_peer.send(b"")

        if load_model_peer in items:
            run_inference = await load_model(load_model_peer, args=args)

        if main_socket in items:
            img_buffer: bytes
            format: bytes
            img_buffer, format = await main_socket.recv_multipart()
            args["imgBuffer"] = img_buffer
            args["imgResized"] = None
            args["format"] = format.decode()
            send_inference_results(main_socket, run_inference)

        if update_settings_socket in items:
            settings: core.types.ModelSettings = (
                await update_settings_socket.recv_json()
            )
            args["topK"] = settings["topK"]
            args["scoreThreshold"] = settings["threshold"]
            send_inference_results(update_settings_socket, run_inference)
