from typing import List, Optional, Union

from pydantic import BaseModel


def to_calmel_case(string: str) -> str:
    words = string.split("_")
    return words[0] + "".join(word.capitalize() for word in words[1:])


BaseModel.Config.alias_generator = to_calmel_case
BaseModel.Config.allow_population_by_field_name = True


class Error(BaseModel):
    """Error object

    error - Error message
    """

    error: str


class User(Error):
    """User object

    id - IP address (guest) or email address (user)
    priority - Your priority in search queue
    concurency - Number of parallel search requests you can make
    quota - Search quota you have for this month
    quota_used - Search quota you have used this month
    """

    id: str
    priority: int
    concurrency: int
    quota: int
    quota_used: int


class AnilistTitle(BaseModel):
    native: Optional[str]
    romaji: Optional[str]
    english: Optional[str]


class Anilist(BaseModel):
    id: int
    id_mal: int
    is_adult: bool
    synonyms: List[str]
    title: AnilistTitle


class Result(BaseModel):
    """Result object

    anilist - The matching Anilist ID or Anilist info
    filename - The filename of file where the match is found
    episode - The extracted episode number from filename
    _from - Starting time of the matching scene (seconds)
    to - Ending time of the matching scene (seconds)
    similarity - Similarity compared to the search image
    video - URL to the preview video of the matching scene
    image - URL to the preview image of the matching scene
    """

    anilist: Union[int, Anilist]
    filename: str
    episode: Optional[Union[int, float, str, List[Union[int, float, str]]]]
    _from: float
    to: float
    similarity: float
    video: str
    image: str


class SearchResult(Error):
    """SearchResult object

    frame_count - Frames compared for image search
    result - Search results
    """

    frame_count: int
    result: List[Result]


Error.update_forward_refs()
SearchResult.update_forward_refs()
Result.update_forward_refs()
Anilist.update_forward_refs()
