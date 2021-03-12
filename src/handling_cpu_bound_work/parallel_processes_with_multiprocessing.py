import time
from multiprocessing import Pool


def count(count_to: int) -> int:
    start = time.time()
    counter = 0
    while counter < count_to:
        counter += 1
    end = time.time()
    print(f"Finish counting to {count_to} in {end - start}")
    return counter


if __name__ == "__main__":
    start_time = time.time()

    with Pool() as process_pool:
        counter_1 = process_pool.apply(count, args=(100000000,))
        counter_2 = process_pool.apply(count, args=(200000000,))

    print(counter_1)
    print(counter_2)
    end_time = time.time()
    print(f"Completed in {end_time - start_time}")
