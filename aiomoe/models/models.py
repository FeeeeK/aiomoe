from typing import List, Union, Optional

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

    error: str = None


class User(Error):
    """User object

    id - IP address (guest) or email address (user)
    priority - Your priority in search queue
    concurency - Number of parallel search requests you can make
    quota - Search quota you have for this month
    quota_used - Search quota you have used this month
    """

    id: str = None
    priority: int = None
    concurrency: int = None
    quota: int = None
    quota_used: int = None


class AnilistTitle(BaseModel):
    native: Optional[str] = None
    romaji: Optional[str] = None
    english: Optional[str] = None


class Anilist(BaseModel):
    id: int = None
    id_mal: int = None
    is_adult: bool = None
    synonyms: List[str] = None
    title: AnilistTitle = None


class Result(BaseModel):
    """Result obbject

    anilist - The matching Anilist ID or Anilist info
    filename - The filename of file where the match is found
    episode - The extracted episode number from filename
    _from - Starting time of the matching scene (seconds)
    to - Ending time of the matching scene (seconds)
    similarity - Similarity compared to the search image
    video - URL to the preview video of the matching scene
    image - URL to the preview image of the matching scene
    """

    anilist: Union[int, Anilist] = None
    filename: str = None
    episode: Union[float, str, List[Union[float, str]]] = None
    _from: float = None
    to: float = None
    similarity: float = None
    video: str = None
    image: str = None


class SearchResult(Error):
    """SearchResult object

    frame_count - Frames compared for image search
    result - Search results
    """

    frame_count: int = None
    result: List[Result] = None


Error.update_forward_refs()
SearchResult.update_forward_refs()
Result.update_forward_refs()
Anilist.update_forward_refs()
