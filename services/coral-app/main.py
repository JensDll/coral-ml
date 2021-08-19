# For development:
# python .\main.py --publish-uri http://localhost:5060 --api-uri http://localhost:5000/api --loglevel quiet

import asyncio
import argparse
import threading
import signal
import logging
import src.zutils as zutils
import time
import os

from zmq.asyncio import Context, Socket
from src import model_manager_server
from src.inference.classification import classification_server
from src.inference.video import video_server

parser = argparse.ArgumentParser()

parser.add_argument("--loglevel", default="info", type=str)
parser.add_argument("--publish-uri", default="http://node-video:8080", type=str)
parser.add_argument("--api-uri", default="http://proxy/record-api", type=str)

args = parser.parse_args()

args.manager_server_port = 7000

args.update_video_settings_port = 7100

args.classify_server_port = 7200
args.update_clssify_settings_port = 7201

log_id = time.strftime("%Y_%m_%d_%H_%M_%S")

if not os.path.isdir("logs"):
    os.mkdir("logs")

fileHanlder = logging.FileHandler(filename=f"logs/{log_id}.log")
fileHanlder.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler()
streamHandler.setLevel(logging.INFO)

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)-8s %(message)s",
    datefmt="%d/%m/%Y %H:%M:%S",
    handlers=[fileHanlder, streamHandler],
)


def load_model(pipe: Socket):
    def impl(**kwargs):
        pipe.send_json(kwargs)
        return pipe.recv_json()

    return impl


async def main():
    load_model_handlers = {}
    ctx = Context()

    # Register pipes for inner thread communication with the classifcation server
    img_pipe, img_peer = zutils.pipe(ctx)
    img_reset_pipe, img_reset_peer = zutils.pipe(ctx)
    load_model_handlers["Image Classification"] = load_model(img_pipe)

    # Register pipes for inner thread communication with the video server
    video_pipe, video_peer = zutils.pipe(ctx)
    video_reset_pipe, video_reset_peer = zutils.pipe(ctx)
    load_model_handlers["Object Detection"] = load_model(video_pipe)

    reset_pipes = [img_reset_pipe, video_reset_pipe]

    # Start the video server
    video_thread = threading.Thread(
        target=asyncio.run,
        args=[
            video_server.start(
                ctx,
                load_model_peer=video_peer,
                reset_peer=video_reset_peer,
                config=args,
            )
        ],
        daemon=True,
    )
    video_thread.start()

    # Start the classifcation server
    classification_thread = threading.Thread(
        target=asyncio.run,
        args=[
            classification_server.start(
                ctx,
                load_model_peer=img_peer,
                reset_peer=img_reset_peer,
                config=args,
            )
        ],
        daemon=True,
    )
    classification_thread.start()

    signal.signal(signal.SIGINT, signal.SIG_DFL)

    # Wait for the ready signal from the servers
    await asyncio.gather(img_pipe.recv(), video_pipe.recv())

    logging.info("[MAIN] All Servers Ready")
    logging.info("[MAIN] Starting Model Manager")

    # Start the model manager server
    await model_manager_server.start(
        ctx=ctx,
        load_model_handlers=load_model_handlers,
        reset_pipes=reset_pipes,
        config=args,
    )


if __name__ == "__main__":
    asyncio.run(main())
