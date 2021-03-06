import asyncio
import sys
from typing import Tuple
import logging
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
        pending = [
            asyncio.create_task(fetch_status(session, "http://www.example.com", 3)),
            asyncio.create_task(fetch_status(session, "http://example.com", 5)),
            asyncio.create_task(fetch_status(session, "http://www.example.com", 0)),
        ]

        while pending:
            done, pending = await asyncio.wait(
                pending, return_when=asyncio.FIRST_COMPLETED
            )

            print(f"Done task count: {len(done)}")
            print(f"Pending task count: {len(pending)}")

            for done_task in done:
                if done_task.exception() is None:
                    print(done_task.result())
                else:
                    logging.error(
                        "request got an exception.", exc_info=done_task.exception()
                    )


asyncio.run(main())
