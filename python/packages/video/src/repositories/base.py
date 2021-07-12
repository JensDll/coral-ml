import aiohttp


class RepositoryBase:
    base_uri: str
    client: aiohttp.ClientSession

    def __init__(self, base_uri: str, client: aiohttp.ClientSession) -> None:
        self.base_uri = base_uri
        self.client = client
