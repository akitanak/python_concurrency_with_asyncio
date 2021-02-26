import asyncio
import signal
import sys
from asyncio import AbstractEventLoop
from typing import Set

sys.path.append("src")
from util.delay_functions import delay


def cancel_tasks():
    print("Got a SIGINT!")
    tasks: Set[asyncio.Task] = asyncio.all_tasks()
    print(f"Cancelling {len(tasks)} task(s).")
    [task.cancel() for task in tasks]


async def await_all_tasks():
    tasks = asyncio.all_tasks()
    print(f"await {len(tasks)} task(s).")
    [await task for task in tasks]


async def main():
    loop: AbstractEventLoop = asyncio.get_event_loop()

    # loop.add_signal_handler(signal.SIGINT, cancel_tasks)
    loop.add_signal_handler(
        signal.SIGINT, lambda: asyncio.create_task(await_all_tasks())
    )
    await delay(10)


asyncio.run(main())
