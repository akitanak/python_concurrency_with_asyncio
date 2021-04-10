import asyncio
import sys
from concurrent.futures.process import ProcessPoolExecutor
from typing import List, Dict
from utils import get_pool

sys.path.append("src")
from util.async_timer import async_timed

product_query = """
    SELECT
        p.product_id,
        p.product_name,
        p.brand_id,
        s.sku_id,
        pc.product_color_name,
        ps.product_size_name
    FROM product as p
    JOIN sku as s on s.product_id = p.product_id
    JOIN product_color as pc on pc.product_color_id = s.product_color_id
    JOIN product_size as ps on ps.product_size_id = s.product_size_id
    WHERE p.product_id = 100"""


async def query_product(pool):
    async with pool.acquire() as connection:
        return await connection.fetchrow(product_query)


@async_timed()
async def query_product_concurrently(pool, query_num):
    queries = [query_product(pool) for _ in range(query_num)]
    return await asyncio.gather(*queries)


def run_in_new_loop(num_queries: int) -> List[Dict]:
    async def run_queries():
        async with get_pool() as pool:
            return await query_product_concurrently(pool, num_queries)

    results = [dict(result) for result in asyncio.run(run_queries())]
    return results


@async_timed()
async def main():
    loop = asyncio.get_running_loop()
    pool = ProcessPoolExecutor()
    tasks = []
    for _ in range(5):
        tasks.append(loop.run_in_executor(pool, run_in_new_loop, 10000))

    all_results: List[List[Dict]] = await asyncio.gather(*tasks)
    total_queries = sum([len(result) for result in all_results])
    print(f"Retrieved {total_queries} products the product database.")


if __name__ == "__main__":
    asyncio.run(main())
