import logging

import asyncio
import zmq
import zmq.asyncio

from modules import core, repositories


async def start(
    reset_pipes: list[zmq.asyncio.Socket],
    load_model_handlers: core.types.LoadModelHandlers,
):
    main_addr = f"tcp://*:{core.Config.Ports.MODEL_MANAGER}"
    main_socket: zmq.asyncio.Socket = core.Config.Zmq.CONTEXT.socket(zmq.REP)
    main_socket.bind(main_addr)
    logging.info(f"[MODEL MANAGER] (Main) Bind to ({main_addr})")

    def send_reset_signals():
        for pipe in reset_pipes:
            pipe.send(b"")
        return asyncio.gather(*[pipe.recv() for pipe in reset_pipes])

    while True:
        id: str = await main_socket.recv_string()
        result = await core.coral.load_model(id)
        if result["success"]:
            await send_reset_signals()
            logging.info("[MODEL MANAGER] Sending model and label path")
            json = await load_model_handlers[result["record"]["recordType"]](result)
            if json["success"]:
                await repositories.Record.set_loaded(id)
            else:
                await repositories.Record.unload()
            main_socket.send_json(json)
        else:
            core.zutils.send_normalized_json(
                main_socket, errors=["An unknown error occurred"]
            )
