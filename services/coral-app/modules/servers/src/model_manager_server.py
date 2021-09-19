import logging

import asyncio
import zmq
from zmq.asyncio import Socket

from modules import core, repositories


class ModelManagerServer:
    reset_pipes: list[Socket]
    main_socket: Socket

    def __init__(
        self,
        reset_pipes: list[Socket],
    ):
        self.reset_pipes = reset_pipes
        address = f"tcp://*:{core.Config.Ports.MODEL_MANAGER}"
        self.main_socket = core.Config.Zmq.CONTEXT.socket(zmq.REP)
        self.main_socket.bind(address)
        logging.info(f"Bind to ({address})")

    def send_reset_signals(self):
        for pipe in self.reset_pipes:
            pipe.send(b"")
        return asyncio.gather(*[pipe.recv() for pipe in self.reset_pipes])

    async def start(self, load_model_handlers: core.types.LoadModelHandlers):
        while True:
            id: str = await self.main_socket.recv_string()
            result = await core.coral.load_model(id)
            if result["success"]:
                await self.send_reset_signals()
                logging.info("Sending model and label path")
                json = await load_model_handlers[result["record"]["recordType"]](result)
                if json["success"]:
                    await repositories.Record.set_loaded(id)
                else:
                    await repositories.Record.unload()
                self.main_socket.send_json(json)
            else:
                await core.zutils.send_message_envelope(
                    self.main_socket, errors=["An unknown error occurred"]
                )
