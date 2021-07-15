import zmq
from zmq.asyncio import Context
import asyncio
import argparse
import threading
import aiohttp
import signal

import src.common as common
import src.zutils as zutils
import src.endpoints as endpoints

parser = argparse.ArgumentParser()
parser.add_argument("--manager_port", default=7100, type=int)
parser.add_argument("--classification_port", default=7200, type=int)
parser.add_argument("--api", default="http://localhost:5000/api", type=str)
args = parser.parse_args()


async def model_manager(ctx: Context, video_pipe: zmq.Socket, img_pipe: zmq.Socket):
    reply_addr = f"tcp://*:{args.manager_port}"
    reply = ctx.socket(zmq.REP)
    reply.bind(reply_addr)
    print(f"[MODEL MANAGER] (REP) Bind to '{reply_addr}'")

    reset_addr = "tcp://*:6666"
    reset = ctx.socket(zmq.PUB)
    reset.bind(reset_addr)
    print(f"[MODEL MANAGER] (PUB) Bind to '{reset_addr}'")

    client = aiohttp.ClientSession()
    record_repo = common.repos.RecordRepository(
        base_uri=args.api,
        client=client
    )

    await asyncio.gather(img_pipe.recv(), video_pipe.recv())

    print("[MODEL MANAGER] All Ready")

    while True:
        id = await reply.recv_string()
        success = True
        try:
            (model_path, label_path), record_type = await common.load_model(record_repo, id)

            reset.send(b"")

            model_path = str(model_path).encode()
            label_path = str(label_path).encode()

            if record_type == "Video":
                await video_pipe.send_multipart([model_path, label_path])
                await video_pipe.recv()
            else:
                await img_pipe.send_multipart([model_path, label_path])
                await img_pipe.recv()
        except Exception as e:
            print("Error loading model")
            print(e)
            success = False
        await reply.send(zutils.encode_bool(success))


async def main():
    ctx = Context()

    img_pipe, img_peer = zutils.pipe(ctx)
    video_pipe, video_peer = zutils.pipe(ctx)

    streamer_thread = threading.Thread(
        target=asyncio.run,
        args=[endpoints.streamer.start(ctx, video_peer, args)],
        daemon=True
    )
    streamer_thread.start()

    classification_thread = threading.Thread(
        target=asyncio.run,
        args=[endpoints.classificattion.start(ctx, img_peer, args)],
        daemon=True
    )
    classification_thread.start()

    signal.signal(signal.SIGINT, signal.SIG_DFL)

    await model_manager(
        ctx,
        img_pipe=img_pipe,
        video_pipe=video_pipe,
    )


if __name__ == "__main__":
    asyncio.run(main())
