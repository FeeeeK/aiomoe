# AioMoe

Fully asynchronous trace.moe API wrapper

## Installation

You can install the stable version from PyPI:

    $ pip install aiomoe

Or get it from github:

    $ pip install https://github.com/FeeeeK/aiomoe/archive/refs/heads/master.zip

## Usage

### Get info about your account

```python
import asyncio
from aiomoe import AioMoe

tm = AioMoe() # or AioMoe(token="xxxxxxxx")

async def main():
    me = await tm.me()
    print(me)
    print(f"Used quota: {me.quota_used}/{me.quota}")

asyncio.run(main())
```
The output will be like this:
```
User(error=None, id='your ip', priority=0, concurrency=1, quota=1000, quota_used=0)
Used quota: 0/1000
```

### Search anime
```python
import asyncio
from aiomoe import AioMoe

tm = AioMoe()

async def main():
    image = "https://i.imgur.com/Xrb06w5.png"
    search_results = await tm.search(file_source=image, anilist_info=True)
    print(search_results.result[0].anilist.title.romaji)
    # 'Steins;Gate 0'

asyncio.run(main())
```
You can pass a link to an image, bytes or file-like object (`io.BytesIO`)
```python
    with open("image.png", "rb") as file:
        search_results = await tm.search(file)
```
And use additional parameters such as:
 - anilist_info - Return an `Anilist` object instead of anilist id
 - cut_borders - Cut out black borders from screenshots
 - anilist_id - Filter results by anilist id

## See Also
  - [Response objects](https://github.com/FeeeeK/aiomoe/blob/master/aiomoe/models/models.py)
  - [trace.moe API docs](https://soruly.github.io/trace.moe-api/#/docs)
  - [trace.moe API swagger docs](https://app.swaggerhub.com/apis/soruly/api.trace.moe)

## Contributing

1.  Fork it
2.  Create your feature branch (`git checkout -b my-new-feature`)
3.  Commit your changes (`git commit -am 'Add some feature'`)
4.  Push to the branch (`git push origin my-new-feature`)
5.  Create new Pull Request

## License

Released under the MIT license.

Copyright by [FeeeeK](https://github.com/feeeek).
