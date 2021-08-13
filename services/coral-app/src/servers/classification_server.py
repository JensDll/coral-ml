import argparse
import zmq
import logging
import functools

from zmq.asyncio import Context, Poller, Socket
from src import common, zutils
from src.inference.classification import models


async def load_model(peer: Socket):
    logging.info("[CLASSIFICATION] Received Interpreter")
    json = await peer.recv_json()
    labels = common.load_labels(json["label_path"])
    interpreter = common.load_interpreter(json["model_path"])
    logging.info("[CLASSIFICATION] Sending Response ...")
    zutils.send_normalized_json(peer)
    return functools.partial(
        getattr(models, "generic_model"), interpreter=interpreter, labels=labels
    )


async def start(
    ctx: Context,
    load_model_peer: zmq.Socket,
    reset_peer: zmq.Socket,
    args: argparse.Namespace,
):
    classify_server_addr = f"tcp://*:{args.classify_server_port}"
    classify_server = ctx.socket(zmq.REP)
    classify_server.bind(classify_server_addr)
    logging.info(f"[CLASSIFICATION] (REP) Bind to '{classify_server_addr}'")

    poller = Poller()
    poller.register(reset_peer, zmq.POLLIN)
    poller.register(load_model_peer, zmq.POLLIN)
    poller.register(classify_server, zmq.POLLIN)

    run_inference = None
    load_model_peer.send(b"")

    while True:
        try:
            items = dict(await poller.poll())
        except:
            break

        if reset_peer in items:
            await reset_peer.recv()
            run_inference = None
            logging.info("[CLASSIFICATION] Reset")
            reset_peer.send(b"")

        if load_model_peer in items:
            run_inference = await load_model(load_model_peer)

        if classify_server in items:
            img_buffer, format = await classify_server.recv_multipart()
            if run_inference == None:
                zutils.send_normalized_json(
                    classify_server, errors=["No model is loaded for this task"]
                )
            else:
                format = format.decode()

                try:
                    results = run_inference(
                        img_buffer=img_buffer,
                        format=format,
                    )
                    zutils.send_normalized_json(classify_server, data=results)
                except Exception as e:
                    zutils.send_normalized_json(classify_server, errors=[str(e)])
