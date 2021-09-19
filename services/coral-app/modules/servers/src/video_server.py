import logging
import functools
from typing import Union

import cv2 as cv
import numpy as np
import zmq
from zmq.asyncio import Socket, Poller

from modules import core, inference


class VideoServer:
    reset_peer: Socket
    load_model_peer: Socket
    update_settings_socket: Socket
    poller: Poller

    def __init__(self, reset_peer: Socket, load_model_peer: Socket):
        self.reset_peer = reset_peer
        self.load_model_peer = load_model_peer

        address = f"tcp://*:{core.Config.Ports.VIDEO_UPDATE_SETTINGS}"
        self.update_settings_socket: Socket = core.Config.Zmq.CONTEXT.socket(zmq.REP)
        self.update_settings_socket.bind(address)
        logging.info(f"Bind to ({address})")

        self.poller = Poller()
        self.poller.register(self.reset_peer, zmq.POLLIN)
        self.poller.register(self.load_model_peer, zmq.POLLIN)
        self.poller.register(self.update_settings_socket, zmq.POLLIN)

    def signal_ready(self):
        return self.load_model_peer.send(b"")

    async def start(self):
        cap = cv.VideoCapture(0)
        cap_props: core.types.CapProps = {
            "frameWidth": int(cap.get(cv.CAP_PROP_FRAME_WIDTH)),
            "frameHeight": int(cap.get(cv.CAP_PROP_FRAME_HEIGHT)),
            "fps": int(cap.get(cv.CAP_PROP_FPS)),
        }

        stream = core.stream.start_stream(cap_props)
        fps_counter = core.FpsCounter()

        model = inference.DetectionModel()
        top_k = 5
        score_threshold = 0.1

        await self.signal_ready()

        while True:
            try:
                items = dict(await self.poller.poll(0))
            except:
                break

            if self.reset_peer in items:
                await self.reset_peer.recv()
                logging.info("Reset video server")
                model.reset()
                await self.reset_peer.send(b"")

            if self.load_model_peer in items:
                await model.load_model(self.load_model_peer)

            if self.update_settings_socket in items:
                settings: core.types.ModelSettings = (
                    await self.update_settings_socket.recv_json()
                )
                top_k = settings["topK"]
                score_threshold = settings["scoreThreshold"]
                await self.update_settings_socket.send(b"")

            img: core.types.Image = cap.read()[1]
            cv.cvtColor(img, cv.COLOR_BGR2RGB, img)

            if model.loaded:
                model.predict(img, top_k, score_threshold)

            fps_counter.put_fps(img)

            try:
                stream.stdin.write(img.tobytes())  # type: ignore
            except Exception:
                stream = next(core.stream.restart_stream(cap_props))
