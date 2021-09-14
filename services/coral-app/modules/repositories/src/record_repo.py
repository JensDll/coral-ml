import aiohttp
import logging
import pathlib
import traceback
import platform
import zipfile
import subprocess
from aiohttp.client_reqrep import ClientResponse
from modules import core


def extract_zip(file_path: pathlib.Path):
    stem = file_path.stem
    name = file_path.name
    logging.info(f"Extracting record zip ({name}) to ({stem}) ...")
    if platform.system() == "Windows":
        with zipfile.ZipFile(file_path, "r") as zip:
            zip.extractall(stem)
    else:
        subprocess.run(["unzip", "-o", "-d", stem, name])
    model_path = pathlib.Path(stem) / "model.tflite"
    label_path = pathlib.Path(stem) / "label"
    model_path_abs = model_path.resolve().absolute()
    label_path_abs = label_path.resolve().absolute()
    logging.info(f"Model path ({model_path_abs})")
    logging.info(f"Label path ({label_path_abs})")
    return model_path_abs, label_path_abs


async def save_zip(resp: ClientResponse, file_path: pathlib.Path, chunk_size=512):
    logging.info(f"Saving record zip ...")
    with file_path.open("wb") as file:
        while True:
            chunk = await resp.content.read(chunk_size)
            if not chunk:
                break
            file.write(chunk)


class RecordRepository:
    @staticmethod
    async def get_by_id(id: core.types.Id):
        uri = f"{core.Config.Uri.RECORD_API}/record/{id}"
        logging.info(uri)
        async with core.Config.Http.SESSION.get(uri) as resp:
            if resp.ok:
                record: core.types.Record = await resp.json()
                record["modelFileName"] = record["modelFileName"].replace(".tflite", "")
                return record
            raise aiohttp.ClientError()

    @staticmethod
    async def download(id: core.types.Id):
        uri = f"{core.Config.Uri.RECORD_API}/record/download/{id}"
        logging.info(uri)
        async with core.Config.Http.SESSION.get(uri) as resp:
            zip_path = pathlib.Path("record.zip")
            try:
                if resp.ok:
                    await save_zip(resp, zip_path)
                    return extract_zip(zip_path)
                raise aiohttp.ClientError()
            except Exception as e:
                logging.error(f"Error downloading record with id ({id})")
                logging.error(traceback.format_exc())
                raise e
            finally:
                logging.info(f"Removing record zip ...")
                zip_path.unlink(missing_ok=True)

    @staticmethod
    async def set_loaded(id: core.types.Id):
        uri = f"{core.Config.Uri.RECORD_API}/record/loaded/{id}"
        logging.info(uri)
        async with core.Config.Http.SESSION.put(uri):
            pass

    @staticmethod
    async def unload():
        uri = f"{core.Config.Uri.RECORD_API}/record/unload"
        logging.info(uri)
        async with core.Config.Http.SESSION.put(uri):
            pass
