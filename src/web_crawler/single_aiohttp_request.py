import asyncio
import aiohttp
import sys

sys.path.append("src")
from web_crawler import fetch_status
from util.async_timer import async_timed


@async_timed()
async def main():
    async with aiohttp.ClientSession() as session:
        url = "http://www.example.com"
        status = await fetch_status(session, url)
        print(f"Status for {url} was {status}")


asyncio.run(main())
