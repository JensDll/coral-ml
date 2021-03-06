# python main.py --loglevel quiet
import argparse
import asyncio
import logging
import threading
import os

import zmq.asyncio
import aiohttp

if os.environ.get("MODE") != "PROD":
    import dotenv

    dotenv.load_dotenv()

from modules import core, servers


def load_model(pipe: zmq.asyncio.Socket):
    def impl(json: core.types.LoadModelResult):
        pipe.send_json(json)
        return pipe.recv_json()

    return impl


async def main():
    core.logging.setup_logging()

    parser = argparse.ArgumentParser()
    parser.add_argument("--loglevel", default="info", type=str)
    args = parser.parse_args()

    core.Config.Http.SESSION = aiohttp.ClientSession()
    core.Config.Zmq.CONTEXT = zmq.asyncio.Context()
    core.Config.FFmpeg.LOGLEVEL = args.loglevel

    load_model_handlers: core.types.LoadModelHandlers = {}

    # Register pipes for inner thread communication with the image server
    img_reset_pipe, img_reset_peer = core.zutils.pipe()
    img_load_model_pipe, img_load_model_peer = core.zutils.pipe()
    load_model_handlers["Image Classification"] = load_model(img_load_model_pipe)

    # Start the image server thread
    image_server = servers.ImageServer(img_reset_peer, img_load_model_peer)
    image_server_thread = threading.Thread(
        target=asyncio.run,
        args=[image_server.start()],
        daemon=True,
    )
    image_server_thread.start()

    # Register pipes for inner thread communication with the video server
    video_reset_pipe, video_reset_peer = core.zutils.pipe()
    video_load_model_pipe, video_load_model_peer = core.zutils.pipe()
    load_model_handlers["Object Detection"] = load_model(video_load_model_pipe)

    # Start the video server thread
    video_server = servers.VideoServer(video_reset_peer, video_load_model_peer)
    video_server_thread = threading.Thread(
        target=asyncio.run,
        args=[video_server.start()],
        daemon=True,
    )
    video_server_thread.start()

    reset_pipes = [img_reset_pipe, video_reset_pipe]

    # Wait for the ready signal from the servers
    await asyncio.gather(img_load_model_pipe.recv(), video_load_model_pipe.recv())

    logging.info("All servers ready")
    logging.info("Starting model manager")

    # Start model manager server in main thread
    model_manager_server = servers.ModelManagerServer(reset_pipes)
    await model_manager_server.start(load_model_handlers)

    await core.Config.Http.SESSION.close()


if __name__ == "__main__":
    asyncio.run(main())
