import asyncio
import concurrent.futures
import functools
import time
from typing import Dict, Iterator, List


def partition(data: List[str], chunk_size: int) -> Iterator[List[str]]:
    for i in range(0, len(data), chunk_size):
        yield data[i : i + chunk_size]


def map_frequencies(chunk: List[str]) -> Dict[str, int]:
    counter: Dict[str, int] = {}
    for line in chunk:
        word, _, _, count = line.split("\t")
        if counter.get(word):
            counter[word] = counter[word] + int(count)
        else:
            counter[word] = int(count)
    return counter


def merge_frequencies(first: Dict[str, int], second: Dict[str, int]) -> Dict[str, int]:
    merged = first
    for key in second:
        if key in merged:
            merged[key] = merged[key] + second[key]
        else:
            merged[key] = second[key]
    return merged


async def main(partition_size: int):
    with open("data/google_books/googlebooks-eng-all-1gram-20120701-a") as f:
        contents = f.readlines()
        loop = asyncio.get_event_loop()
        tasks = []
        start = time.time()
        with concurrent.futures.ProcessPoolExecutor() as pool:
            for chunk in partition(contents, partition_size):
                tasks.append(
                    loop.run_in_executor(
                        pool, functools.partial(map_frequencies, chunk)
                    )
                )

            intermediate_results = await asyncio.gather(*tasks)
            final_result = functools.reduce(merge_frequencies, intermediate_results)

            print(f"Aardvark has appeared {final_result['Aardvark']} times.")

            end = time.time()
            print(f"Map reduce took: {(end - start):.4f} seconds.")


if __name__ == "__main__":
    asyncio.run(main(partition_size=60000))
