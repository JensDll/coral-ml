import aiohttp
from aiohttp.client_reqrep import ClientResponse
import zipfile
from .base import RepositoryBase
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


class RecordRepository(RepositoryBase):
    def __init__(self, base_uri: str, client: aiohttp.ClientSession) -> None:
        super().__init__(base_uri, client)

    async def get_by_id(self, id: int) -> str:
        print(f"Loading model with id ({id})")
        async with self.client.get(f"{self.base_uri}/record/{id}") as resp:
            if resp.ok:
                json = await resp.json()
                print(json)
                return json["recordType"]

    async def download(self, id: int):
        async with self.client.get(f"{self.base_uri}/record/download/{id}") as resp:
            if resp.ok:
                file_path = pathlib.Path("record.zip")
                await save_zip(resp, file_path)
                return extract_zip(file_path)
            raise aiohttp.ClientError()

    async def set_loaded(self, id: int):
        async with self.client.put(f"{self.base_uri}/record/loaded/{id}") as resp:
            await resp.text()
