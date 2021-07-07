import aiohttp
import pathlib


class ModelRepository:
    def __init__(self, uri: str, session: aiohttp.ClientSession) -> None:
        self.uri = uri
        self.session = session

    async def get_by_id(self, id: int):
        print(f"{self.uri}/model/{id}")
        async with self.session.get(f"{self.uri}/model/{id}") as resp:
            file = pathlib.Path(__file__).parent.joinpath("model.tflite")
            await self.__save_to_file(str(file), resp)

    async def __save_to_file(self, file: str, resp, chunk_size=512):
        with open(file, "wb") as f:
            while True:
                chunk = await resp.content.read(chunk_size)
                if not chunk:
                    break
                f.write(chunk)
