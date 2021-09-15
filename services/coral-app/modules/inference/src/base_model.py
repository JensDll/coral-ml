import logging

import zmq.asyncio

from modules import core


class BaseModel:
    labels: core.types.Labels
    interpreter: core.Interpreter
    loaded: bool = False

    async def load_model(self, peer: zmq.asyncio.Socket):
        json: core.types.LoadModelResult = await peer.recv_json()
        logging.info("Received Interpreter")
        self.labels = core.coral.load_labels(json["labelPath"])
        self.interpreter = core.coral.load_interpreter(json["modelPath"])
        self.interpreter.name = json["record"]["modelFileName"]
        self.loaded = True
        logging.info("Sending Response ...")
        await core.zutils.send_normalized_json(peer)

    def predict(self):
        pass

    def reset(self):
        self.loaded = False
