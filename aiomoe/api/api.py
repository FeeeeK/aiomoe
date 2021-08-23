from io import BytesIO
from typing import BinaryIO, Dict, Optional, Union

from aiohttp import ClientSession
from loguru import logger

from ..models import SearchResult, User
from ..utils import check_response


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
        file_source: Union[BinaryIO, bytes, str],
        anilist_info: Optional[bool] = False,
        cut_borders: Optional[bool] = False,
        anilist_id: Optional[int] = None,
    ) -> SearchResult:
        """/search

        file_source - Image url or a file-like object
        anilist_info - Return an `Anilist` object instead of anilist id
        cut_borders - Cut out black borders from screenshots
        anilist_id - Filter results by anilist id
        """
        url = self.API_URL + "/search"
        query: Dict[str, Union[str, int]] = {}
        file: Optional[BinaryIO] = None
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
        elif isinstance(file_source, bytes):
            file = BytesIO(file_source)
        else:
            file = file_source
        status, response = await self.request(url, query, file)
        logger.debug(f"Got response from {self.API_URL}/search: {response}")
        return await check_response(status, response, SearchResult)

    async def request(self, url: str, query: dict, data: Optional[BinaryIO] = None):
        files = None
        if data:
            files = {"image": data}
        async with ClientSession(**self.session_kwargs) as session, session.request(
            "POST" if data else "GET", url, params=query, data=files
        ) as response:
            logger.debug(f"Request sent to '{url}', status: {response.status}")
            return response.status, await response.json()
