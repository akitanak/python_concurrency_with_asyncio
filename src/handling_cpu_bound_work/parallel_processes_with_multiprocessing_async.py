import asyncio
import time
from asyncio.events import AbstractEventLoop
from concurrent.futures import ProcessPoolExecutor
from functools import partial
from typing import List


def count(count_to: int) -> int:
    start = time.time()
    counter = 0
    while counter < count_to:
        counter += 1
    end = time.time()
    print(f"Finish counting to {count_to} in {end - start}")
    return counter


async def main():
    with ProcessPoolExecutor() as process_pool:
        loop: AbstractEventLoop = asyncio.get_event_loop()
        numbers = [
            200000000,
            100000000,
            100000000,
        ]
        calls: List[partial[int]] = [partial(count, num) for num in numbers]
        call_coros = []

        for call in calls:
            call_coros.append(loop.run_in_executor(process_pool, call))

        for result in asyncio.as_completed(call_coros):
            print(await result)


if __name__ == "__main__":
    start_time = time.time()

    asyncio.run(main())

    end_time = time.time()
    print(f"Completed in {end_time - start_time}")
