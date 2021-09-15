import logging

import zmq
from zmq.asyncio import Socket, Poller

from modules import core, inference


class ImageServer:
    poller: Poller
    main_socket: Socket
    update_settings_socket: Socket
    reset_peer: Socket
    load_model_peer: Socket

    def __init__(self, reset_peer: Socket, load_model_peer: Socket):
        self.reset_peer = reset_peer
        self.load_model_peer = load_model_peer

        address = f"tcp://*:{core.Config.Ports.IMAGE_CLASSIFICATION}"
        self.main_socket: Socket = core.Config.Zmq.CONTEXT.socket(zmq.REP)
        self.main_socket.bind(address)
        logging.info(f"Bind to ({address})")

        address = f"tcp://*:{core.Config.Ports.IMAGE_UPDATE_SETTINGS}"
        self.update_settings_socket: Socket = core.Config.Zmq.CONTEXT.socket(zmq.REP)
        self.update_settings_socket.bind(address)
        logging.info(f"Bind to ({address})")

        self.poller = Poller()
        self.poller.register(self.reset_peer, zmq.POLLIN)
        self.poller.register(self.load_model_peer, zmq.POLLIN)
        self.poller.register(self.main_socket, zmq.POLLIN)
        self.poller.register(self.update_settings_socket, zmq.POLLIN)

    def signal_ready(self):
        return self.load_model_peer.send(b"")

    async def start(self):
        await self.signal_ready()

        model = inference.ImageClassificationModel()
        top_k = 5
        score_threshold = 0.1

        while True:
            try:
                items = dict(await self.poller.poll())
            except Exception:
                break

            if self.reset_peer in items:
                await self.reset_peer.recv()
                logging.info("Reset image server")
                model.reset()
                await self.reset_peer.send(b"")

            if self.load_model_peer in items:
                await model.load_model(self.load_model_peer)

            if self.main_socket in items:
                img_buffer: bytes
                img_format: bytes
                img_buffer, img_format = await self.main_socket.recv_multipart()
                if model.loaded:
                    result = model.predict(
                        (img_buffer, img_format.decode()), top_k, score_threshold
                    )
                    await core.zutils.send_normalized_json(
                        self.main_socket, data=result
                    )
                else:
                    await core.zutils.send_normalized_json(
                        self.main_socket, errors=["No model is loaded for this task"]
                    )

            if self.update_settings_socket in items:
                settings: core.types.ModelSettings = (
                    await self.update_settings_socket.recv_json()
                )
                top_k = settings["topK"]
                score_threshold = settings["threshold"]
                if model.has_cache:
                    result = model.predict(
                        top_k=top_k,
                        score_threshold=score_threshold,
                    )
                    await core.zutils.send_normalized_json(
                        self.update_settings_socket, data=result
                    )
                else:
                    await core.zutils.send_normalized_json(
                        self.update_settings_socket,
                        errors=["No model is loaded for this task"],
                    )
