import asyncio
import aiohttp
import sys

sys.path.append("src")
from web_crawler import fetch_status
from util.async_timer import async_timed


@async_timed()
async def main():
    async with aiohttp.ClientSession() as session:
        urls = ["http://www.example.com", "python://www.example.com"]
        requests = [fetch_status(session, url) for url in urls]
        responses = await asyncio.gather(*requests, return_exceptions=True)
        exceptions = [res for res in responses if isinstance(res, Exception)]
        successful_results = [
            res for res in responses if not isinstance(res, Exception)
        ]

        print(f"All results: {responses}")
        print(f"exceptions: {exceptions}")
        print(f"successful_results: {successful_results}")


asyncio.run(main())
