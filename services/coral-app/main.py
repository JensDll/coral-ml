from zmq.asyncio import Context, Socket
import asyncio
import argparse
import threading
import signal
import logging
import src.zutils as zutils
import src.endpoints as endpoints
import time
import os

parser = argparse.ArgumentParser()
parser.add_argument("--manager-port", default=7000, type=int)
parser.add_argument("--classify-port", default=7100, type=int)
parser.add_argument("--video-port", default=7200, type=int)
parser.add_argument("--loglevel", default="quiet", type=str)

parser.add_argument("--publish-uri", default="http://localhost:5060", type=str)
parser.add_argument("--api-uri", default="http://localhost:5000/api", type=str)

args = parser.parse_args()

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
    async def impl(**kwargs):
        pipe.send_json(kwargs)
        return await pipe.recv_json()

    return impl


async def main():
    handlers = {}
    ctx = Context()

    img_pipe, img_peer = zutils.pipe(ctx)
    img_reset_pipe, img_reset_peer = zutils.pipe(ctx)
    handlers["Image Classification"] = load_model(img_pipe)

    video_pipe, video_peer = zutils.pipe(ctx)
    video_reset_pipe, video_reset_peer = zutils.pipe(ctx)
    handlers["Object Detection"] = load_model(video_pipe)

    reset_pipes = [img_reset_pipe, video_reset_pipe]

    video_thread = threading.Thread(
        target=asyncio.run,
        args=[
            endpoints.video.start(
                ctx,
                load_model_peer=video_peer,
                reset_peer=video_reset_peer,
                args=args,
            )
        ],
        daemon=True,
    )
    video_thread.start()

    classification_thread = threading.Thread(
        target=asyncio.run,
        args=[
            endpoints.classification.start(
                ctx, load_model_peer=img_peer, reset_peer=img_reset_peer, args=args
            )
        ],
        daemon=True,
    )
    classification_thread.start()

    signal.signal(signal.SIGINT, signal.SIG_DFL)

    await asyncio.gather(img_pipe.recv(), video_pipe.recv())
    logging.info("[MAIN] All Endpoints Ready")
    logging.info("[MAIN] Starting Model Manager")
    await endpoints.model_manager.start(
        ctx=ctx, handlers=handlers, reset_pipes=reset_pipes, args=args
    )


if __name__ == "__main__":
    asyncio.run(main())
