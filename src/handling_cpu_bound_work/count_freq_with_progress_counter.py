import asyncio
import functools
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import Value
from typing import Dict, Iterator, List

from count_freq_of_word_start_with_a import partition, merge_frequencies


map_progress: Value


def init(progress: Value):
    global map_progress
    map_progress = progress


def map_frequencies(chunk: List[str]) -> Dict[str, int]:
    counter: Dict[str, int] = {}
    for line in chunk:
        word, _, _, count = line.split("\t")
        if counter.get(word):
            counter[word] = counter[word] + int(count)
        else:
            counter[word] = int(count)

    with map_progress.get_lock():
        map_progress.value += 1

    return counter


async def progress_reporter(total_partitions: int):
    while map_progress.value < total_partitions:
        print(f"Finished {map_progress.value}/{total_partitions} map operations")
        await asyncio.sleep(1)


async def reduce(loop, pool, counters, chunk_size) -> Dict[str, int]:
    chunks: List[List[Dict]] = list(partition(counters, chunk_size))
    reducers = []
    while len(chunks[0]) > 1:
        for chunk in chunks:
            reducer = functools.partial(functools.reduce, merge_frequencies, chunk)
            reducers.append(loop.run_in_executor(pool, reducer))

        reducer_chunks = await asyncio.gather(*reducers)
        chunks = list(partition(reducer_chunks, chunk_size))
        reducers.clear()
    return chunks[0][0]


async def main(partition_size: int):
    global map_progress

    with open("data/google_books/googlebooks-eng-all-1gram-20120701-a") as f:
        contents = f.readlines()
        loop = asyncio.get_event_loop()
        tasks = []
        map_progress = Value("i", 0)

        with ProcessPoolExecutor(initializer=init, initargs=(map_progress,)) as pool:

            total_partitions = len(contents) // partition_size
            reporter = asyncio.create_task(progress_reporter(total_partitions))

            for chunk in partition(contents, partition_size):
                tasks.append(
                    loop.run_in_executor(
                        pool, functools.partial(map_frequencies, chunk)
                    )
                )

            counters = await asyncio.gather(*tasks)

            await reporter
            final_result = functools.reduce(merge_frequencies, counters)

            print(f"Aardvark has appeared {final_result['Aardvark']} times.")


if __name__ == "__main__":
    asyncio.run(main(partition_size=60000))
