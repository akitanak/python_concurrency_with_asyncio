import asyncio
import functools
import requests
import sys
from concurrent.futures import ThreadPoolExecutor

sys.path.append("src")
from util.async_timer import async_timed


def get_status_code(url: str) -> int:
    response = requests.get(url)
    return response.status_code


@async_timed()
async def main():
    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor() as pool:
        urls = ["https://www.example.com" for _ in range(1000)]
        tasks = [
            loop.run_in_executor(pool, functools.partial(get_status_code, url))
            for url in urls
        ]
        results = await asyncio.gather(*tasks)
        print(results)


asyncio.run(main())
