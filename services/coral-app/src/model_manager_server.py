import zmq
import logging
import aiohttp
import argparse
import asyncio

from typing import List, TypedDict
from zmq.asyncio import Context, Socket
from src import common, zutils
from src.repositories.record_repository import RecordRepository


class LoadModelResult(TypedDict):
    success: bool
    error: str


async def start(
    ctx: Context,
    load_model_handlers,
    reset_pipes: List[Socket],
    config: argparse.Namespace,
):
    main_addr = f"tcp://*:{config.manager_server_port}"
    main_socket: Socket = ctx.socket(zmq.REP)
    main_socket.bind(main_addr)
    logging.info(f"[MODEL MANAGER] (Main) Bind to '{main_addr}'")

    client = aiohttp.ClientSession()
    record_repo = RecordRepository(base_uri=config.api_uri, client=client)

    async def reset_endpoints():
        for reset_pipe in reset_pipes:
            reset_pipe.send(b"")
        await asyncio.gather(*[reset_pipe.recv() for reset_pipe in reset_pipes])

    while True:
        id = await main_socket.recv_string()
        result = await common.load_model(record_repo, id)
        if result["success"]:
            await reset_endpoints()
            logging.info("[MODEL MANAGER] Sending model and label path")
            normalized_json: zutils.NormalizedJson = await load_model_handlers[
                result["record_type"]
            ](
                model_path=result["model_path"],
                label_path=result["label_path"],
                model_name=result["model_file_name"],
            )
            if normalized_json["success"]:
                await record_repo.set_loaded(id)
            else:
                await record_repo.unload()
            main_socket.send_json(normalized_json)
        else:
            zutils.send_normalized_json(
                main_socket, errors=["An unknown error occurred"]
            )
