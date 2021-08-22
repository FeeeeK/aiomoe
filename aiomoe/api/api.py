from io import BytesIO
from typing import IO, Optional, Union

from aiohttp import ClientSession

from ..models import SearchResult, User
from ..utils import check_response
from loguru import logger


class API:
    """Main class for API calls"""

    API_URL = "https://api.trace.moe"

    def __init__(self, token: str = None, session_kwargs: dict = {}):
        self.token = token
        self.session_kwargs = session_kwargs

    async def me(self) -> User:
        url = self.API_URL + "/me"
        query = {}
        if self.token:
            query["key"] = self.token
        status, response = await self.request(url, query)
        logger.debug(f"Got response from {self.API_URL}/me: {response}")
        return await check_response(status, response, User)

    async def search(
        self,
        file_source: Union[IO, bytes, str],
        anilist_info: bool = False,
        cut_borders: bool = False,
        anilist_id: int = None,
    ) -> SearchResult:
        """/search

        file_source - Image url or a file-like object
        anilist_info - Return an `Anilist` object instead of anilist id
        cut_borders - Cut out black borders from screenshots
        anilist_id - Filter results by anilist id
        """
        url = self.API_URL + "/search"
        query = {}
        if self.token:
            query["key"] = self.token
        if anilist_info:
            query["anilistInfo"] = 1
        if cut_borders:
            query["cutBorders"] = 1
        if anilist_id:
            query["anilistID"] = anilist_id
        if isinstance(file_source, str):
            query["url"] = file_source
            file_source = None
        elif isinstance(file_source, bytes):
            file_source = BytesIO(bytes)
        status, response = await self.request(url, query, file_source)
        logger.debug(f"Got response from {self.API_URL}/search: {response}")
        return await check_response(status, response, SearchResult)

    async def request(self, url: str, query: dict, data: Optional[IO] = None):
        async with ClientSession(**self.session_kwargs) as session, session.request(
            "POST" if data else "GET", url, params=query, data=data
        ) as response:
            logger.debug(f"Request sent to '{url}', status: {response.status}")
            return response.status, await response.json()
