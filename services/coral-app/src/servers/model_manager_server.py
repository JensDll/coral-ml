import zmq
import logging
import aiohttp
import argparse
import asyncio

from typing import List
from zmq.asyncio import Context, Socket
from typing_extensions import TypedDict
from src import common, zutils
from src.repositories.record_repository import RecordRepository


class LoadModelResult(TypedDict):
    success: bool
    error: str


async def start(
    ctx: Context,
    handlers,
    reset_pipes: List[Socket],
    args: argparse.Namespace,
):
    model_server_addr = f"tcp://*:{args.manager_server_port}"
    model_server = ctx.socket(zmq.REP)
    model_server.bind(model_server_addr)
    logging.info(f"[MODEL MANAGER] (REP) Bind to '{model_server_addr}'")

    client = aiohttp.ClientSession()
    record_repo = RecordRepository(base_uri=args.api_uri, client=client)

    async def reset_endpoints():
        for reset_pipe in reset_pipes:
            reset_pipe.send(b"")
        await asyncio.gather(*[reset_pipe.recv() for reset_pipe in reset_pipes])

    while True:
        id = await model_server.recv_string()
        result = await common.load_model(record_repo, id)
        if result["success"]:
            await reset_endpoints()
            logging.info("[MODEL MANAGER] Sending model and label path")
            normalized_json: zutils.NormalizedJson = await handlers[
                result["record_type"]
            ](
                model_path=result["model_path"],
                label_path=result["label_path"],
                model_file_name=result["model_file_name"],
            )
            if normalized_json["success"]:
                await record_repo.set_loaded(id)
            else:
                await record_repo.unload()
            model_server.send_json(normalized_json)
        else:
            zutils.send_normalized_json(
                model_server, errors=["An unknown error occurred"]
            )
