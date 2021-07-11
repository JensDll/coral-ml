import aiohttp
from aiohttp.client_reqrep import ClientResponse
import zipfile
from .api_routes import ApiRoutes
import pathlib


def extract_zip(file_path: pathlib.Path):
    stem = file_path.stem
    with zipfile.ZipFile(file_path, 'r') as zip:
        zip.extractall(stem)
    file_path.unlink()
    model_path = pathlib.Path(stem) / "model.tflite"
    label_path = pathlib.Path(stem) / "label.txt"
    return model_path.resolve(), label_path.resolve()


async def save_zip(resp: ClientResponse, file_path: pathlib.Path, chunk_size=512):
    with file_path.open("wb") as f:
        while True:
            chunk = await resp.content.read(chunk_size)
            if not chunk:
                break
            f.write(chunk)


async def get_by_id(session: aiohttp.ClientSession, id: int):
    async with session.get(ApiRoutes.TFLiteRecord.get_by_id(id)) as resp:
        if resp.ok:
            file_path = pathlib.Path("model.zip")
            await save_zip(resp, file_path)
            return extract_zip(file_path)
        raise aiohttp.ClientError()
