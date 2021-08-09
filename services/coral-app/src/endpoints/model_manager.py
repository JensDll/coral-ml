import typing
import zmq
from typing import List
from zmq.asyncio import Context, Socket
import logging
import aiohttp
import argparse
import asyncio

import src.common as common
import src.zutils as zutils


async def start(
    ctx: Context,
    handlers,
    reset_pipes: List[Socket],
    args: argparse.Namespace,
):
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

    async def reset_endpoints():
        for reset_pipe in reset_pipes:
            reset_pipe.send(b"")
        await asyncio.gather(*[reset_pipe.recv() for reset_pipe in reset_pipes])

    while True:
        id = await reply.recv_string()
        result = await common.load_model(record_repo, id)
        if result["success"]:
            await reset_endpoints()
            logging.info("[MODEL MANAGER] Sending model and label path")
            await handlers[result["record_type"]](
                model_path=result["model_path"],
                label_path=result["label_path"],
                model_file_name=result["model_file_name"],
            )
        reply.send(zutils.encode_bool(result["success"]))
