import asyncio
import sys
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
async def query_product_synchronously(pool, query_num):
    return [await query_product(pool) for _ in range(query_num)]


@async_timed()
async def query_product_concurrently(pool, query_num):
    queries = [query_product(pool) for _ in range(query_num)]
    return await asyncio.gather(*queries)


async def main():
    async with get_pool() as pool:
        await query_product_synchronously(pool, 10000)
        await query_product_concurrently(pool, 10000)


asyncio.run(main())
