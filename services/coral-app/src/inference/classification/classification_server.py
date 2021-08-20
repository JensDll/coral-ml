import argparse
import zmq
import logging
import functools

from zmq.asyncio import Context, Poller, Socket
from src import common, zutils
from src.inference.classification import classification_models
from typing import TypedDict


class Settings(TypedDict):
    topK: int
    threshold: int


async def load_model(peer: Socket, args: classification_models.ModelArgs):
    json = await peer.recv_json()
    logging.info("[CLASSIFICATION] Received Interpreter")
    args["labels"] = common.load_labels(json["label_path"])
    interpreter = common.load_interpreter(json["model_path"])
    args["model_name"] = json["model_name"]
    logging.info("[CLASSIFICATION] Sending Response ...")
    zutils.send_normalized_json(peer)
    return functools.partial(
        getattr(classification_models, "generic_model"),
        interpreter=interpreter,
    )


def run_classfication(socket: Socket, args, run_inference):
    if run_inference == None:
        zutils.send_normalized_json(socket, errors=["No model is loaded for this task"])
    else:
        try:
            results = run_inference(args=args)
            zutils.send_normalized_json(socket, data=results)
        except Exception as e:
            zutils.send_normalized_json(socket, errors=[str(e)])


async def start(
    ctx: Context,
    load_model_peer: Socket,
    reset_peer: Socket,
    config: argparse.Namespace,
):
    main_addr = f"tcp://*:{config.classify_server_port}"
    main_socket: Socket = ctx.socket(zmq.REP)
    main_socket.bind(main_addr)
    logging.info(f"[CLASSIFICATION] (Main) Bind to '{main_addr}'")

    update_settings_addrs = f"tcp://*:{config.update_clssify_settings_port}"
    update_settings_socket: Socket = ctx.socket(zmq.REP)
    update_settings_socket.bind(update_settings_addrs)
    logging.info(
        f"[CLASSIFICATION] (Update Settings) Bind to '{update_settings_addrs}'"
    )

    poller = Poller()
    poller.register(reset_peer, zmq.POLLIN)
    poller.register(load_model_peer, zmq.POLLIN)
    poller.register(main_socket, zmq.POLLIN)
    poller.register(update_settings_socket, zmq.POLLIN)

    run_inference = None
    args: classification_models.ModelArgs = {"top_k": 1, "score_threshold": 0.1}

    # Signal classification server ready
    load_model_peer.send(b"")

    while True:
        try:
            items = dict(await poller.poll())
        except:
            break

        # Reset signal received
        if reset_peer in items:
            await reset_peer.recv()
            run_inference = None
            logging.info("[CLASSIFICATION] Reset")
            await reset_peer.send(b"")

        # Load model signal received
        if load_model_peer in items:
            run_inference = await load_model(load_model_peer, args=args)

        # Update settings request received
        if update_settings_socket in items:
            settings: Settings = await update_settings_socket.recv_json()
            args["top_k"] = settings["topK"]
            args["score_threshold"] = settings["threshold"]
            run_classfication(
                update_settings_socket, args=args, run_inference=run_inference
            )

        # Classification request received
        if main_socket in items:
            img_buffer, format = await main_socket.recv_multipart()
            args["img_buffer"] = img_buffer
            args["format"] = format.decode()
            args["resized"] = None
            run_classfication(main_socket, args=args, run_inference=run_inference)
