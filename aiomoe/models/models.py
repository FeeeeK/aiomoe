from typing import List, Optional, Union

from pydantic import BaseModel


def to_calmel_case(string: str) -> str:
    words = string.split("_")
    return words[0] + "".join(word.capitalize() for word in words[1:])


BaseModel.Config.alias_generator = to_calmel_case
BaseModel.Config.allow_population_by_field_name = True


class Error(BaseModel):
    """Error object"""

    error: str
    """Error message"""


class User(Error):
    """User object"""

    id: str
    """IP address (guest) or email address (user)"""
    priority: int
    """Your priority in search queue"""
    concurrency: int
    """Number of parallel search requests you can make"""
    quota: int
    """Search quota you have for this month"""
    quota_used: int
    """Search quota you have used this month"""


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
    """Result object"""

    anilist: Union[int, Anilist]
    """The matching Anilist ID or Anilist info"""
    filename: str
    """The filename of file where the match is found"""
    episode: Optional[Union[int, float, str, List[Union[int, float, str]]]]
    """The extracted episode number from filename"""
    _from: float
    """Starting time of the matching scene (seconds)"""
    to: float
    """Ending time of the matching scene (seconds)"""
    similarity: float
    """Similarity compared to the search image"""
    video: str
    """URL to the preview video of the matching scene"""
    image: str
    """URL to the preview image of the matching scene"""


class SearchResult(Error):
    """SearchResult object"""

    frame_count: int
    """Frames compared for image search"""
    result: List[Result]
    """Search results"""


Error.update_forward_refs()
SearchResult.update_forward_refs()
Result.update_forward_refs()
Anilist.update_forward_refs()
