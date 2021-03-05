import asyncio
import sys
from typing import Tuple
import aiohttp
from aiohttp import ClientSession

sys.path.append("src")
from util.async_timer import async_timed


async def fetch_status(
    session: ClientSession, url: str, delay: int = 0
) -> Tuple[int, int]:
    await asyncio.sleep(delay)
    async with session.get(url) as result:
        return result.status, delay


@async_timed()
async def main():
    async with aiohttp.ClientSession() as session:
        fetchers = [
            fetch_status(session, "http://www.example.com", 10),
            fetch_status(session, "http://www.example.com", 1),
            fetch_status(session, "http://www.example.com", 5),
        ]

        for finished_task in asyncio.as_completed(fetchers):
            print(await finished_task)


asyncio.run(main())
