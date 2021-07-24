import zmq
from zmq.asyncio import Context
import asyncio
import argparse
import threading
import aiohttp
import signal
import logging
import src.common as common
import src.zutils as zutils
import src.endpoints as endpoints
import time
import os

parser = argparse.ArgumentParser()
parser.add_argument("--manager_port", default=7000, type=int)
parser.add_argument("--classify_port", default=7100, type=int)
parser.add_argument("--video_port", default=7200, type=int)

parser.add_argument("--publish_uri", default="http://localhost:5060", type=str)
parser.add_argument("--api_uri", default="http://localhost:5000/api", type=str)

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


async def model_manager(ctx: Context, video_pipe: zmq.Socket, img_pipe: zmq.Socket):
    reply_addr = f"tcp://*:{args.manager_port}"
    reply = ctx.socket(zmq.REP)
    reply.bind(reply_addr)
    logging.info(f"[MODEL MANAGER] (REP) Bind to '{reply_addr}'")

    reset_addr = "tcp://*:7777"
    reset = ctx.socket(zmq.PUB)
    reset.bind(reset_addr)
    logging.info(f"[MODEL MANAGER] (PUB) Bind to '{reset_addr}'")

    client = aiohttp.ClientSession()
    record_repo = common.repos.RecordRepository(base_uri=args.api_uri, client=client)

    await asyncio.gather(img_pipe.recv(), video_pipe.recv())

    logging.info("[MODEL MANAGER] All Ready")

    while True:
        id = await reply.recv_string()
        result = await common.load_model(record_repo, id)
        if result["success"]:
            reset.send(b"")
            model_path = str(result["model_path"]).encode()
            label_path = str(result["label_path"]).encode()
            if result["record_type"] == "Object Detection":
                await video_pipe.send_multipart([model_path, label_path])
                await video_pipe.recv()
            else:
                await img_pipe.send_multipart([model_path, label_path])
                await img_pipe.recv()
        await reply.send(zutils.encode_bool(result["success"]))


async def main():
    ctx = Context()

    img_pipe, img_peer = zutils.pipe(ctx)
    video_pipe, video_peer = zutils.pipe(ctx)

    video_thread = threading.Thread(
        target=asyncio.run,
        args=[endpoints.video.start(ctx, video_peer, args)],
        daemon=True,
    )
    video_thread.start()

    classification_thread = threading.Thread(
        target=asyncio.run,
        args=[endpoints.classification.start(ctx, img_peer, args)],
        daemon=True,
    )
    classification_thread.start()

    signal.signal(signal.SIGINT, signal.SIG_DFL)

    await model_manager(
        ctx,
        video_pipe=video_pipe,
        img_pipe=img_pipe,
    )


if __name__ == "__main__":
    asyncio.run(main())
