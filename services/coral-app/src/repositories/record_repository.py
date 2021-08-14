import traceback
from typing_extensions import Literal
import aiohttp
from aiohttp.client_reqrep import ClientResponse
import zipfile
from .base import RepositoryBase
import pathlib
import logging
import platform
import subprocess

RecordType = Literal["Image Classification", "Object Detection"]


def extract_zip(file_path: pathlib.Path):
    stem = file_path.stem
    name = file_path.name
    if platform.system() == "Windows":
        logging.info(f"[RECORD REPO] Extracting zip ({name}) under {platform.system()}")
        with zipfile.ZipFile(file_path, "r") as zip:
            zip.extractall(stem)
    else:
        logging.info(f"[RECORD REPO] Extracting zip ({name}) under {platform.system()}")
        subprocess.run(["unzip", "-o", "-d", stem, name])
    logging.info(f"[RECORD REPO] Extracted zip content to ({stem})")
    model_path = pathlib.Path(stem) / "model.tflite"
    model_path_abs = model_path.resolve()
    logging.info(f"[RECORD REPO] Model Path ({model_path_abs})")
    label_path = pathlib.Path(stem) / "label"
    label_path_abs = label_path.resolve()
    logging.info(f"[RECORD REPO] Label Path ({label_path_abs})")

    return model_path_abs, label_path_abs


async def save_zip(resp: ClientResponse, file_path: pathlib.Path, chunk_size=512):
    logging.info(f"[RECORD REPO] Saving zip")
    with file_path.open("wb") as f:
        while True:
            chunk = await resp.content.read(chunk_size)
            if not chunk:
                break
            f.write(chunk)


class RecordRepository(RepositoryBase):
    def __init__(self, base_uri: str, client: aiohttp.ClientSession) -> None:
        super().__init__(base_uri, client)

    async def get_record_info(self, id: int):
        logging.info(f"[RECORD REPO] Loading model with id ({id})")
        async with self.client.get(f"{self.base_uri}/record/{id}") as resp:
            if resp.ok:
                json = await resp.json()
                record_type: RecordType = json["recordType"]
                model_file_name: str = json["modelFileName"]
                model_file_name = model_file_name.replace(".tflite", "")
                logging.info(
                    f"[RECORD REPO] Received record info - type ({record_type})"
                )
                logging.info(
                    f"[RECORD REPO] Received record info - filename ({model_file_name})"
                )
                return record_type, model_file_name

    async def download(self, id: int):
        logging.info(f"[RECORD REPO] Downloading model with id ({id})")
        async with self.client.get(f"{self.base_uri}/record/download/{id}") as resp:
            try:
                file_path = pathlib.Path("record.zip")
                if resp.ok:
                    await save_zip(resp, file_path)
                    return extract_zip(file_path)
                raise aiohttp.ClientError()
            except Exception as e:
                logging.error(f"[RECORD REPO] Error downloading model with id ({id})")
                logging.error(traceback.format_exc())
                raise e
            finally:
                if file_path.is_file():
                    logging.info(f"[RECORD REPO] Removing zip ({id})")
                    file_path.unlink()

    async def set_loaded(self, id: int):
        logging.info(f"[RECORD REPO] Setting model loaded with id ({id})")
        async with self.client.put(f"{self.base_uri}/record/loaded/{id}"):
            return

    async def unload(self):
        logging.info(f"[RECORD REPO] Unloading model")
        async with self.client.put(f"{self.base_uri}/record/unload"):
            return
