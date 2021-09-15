# python main.py --publish-uri http://localhost:5060 --api-uri http://localhost:5000/api --loglevel quiet
import argparse
import asyncio
import logging
import threading

import zmq.asyncio
import aiohttp

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
    parser.add_argument("--publish-uri", default="http://node-video:8080", type=str)
    parser.add_argument("--api-uri", default="http://proxy/record-api", type=str)

    args = parser.parse_args()

    core.Config.Http.SESSION = aiohttp.ClientSession()
    core.Config.Zmq.CONTEXT = zmq.asyncio.Context()
    core.Config.Uri.RECORD_API = args.api_uri
    core.Config.Uri.PUBLISH_VIDEO = args.publish_uri
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
