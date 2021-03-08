import asyncio
from utils import get_connection


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


async def main():
    conn = await get_connection()

    queries = [conn.execute(product_query), conn.execute(product_query)]

    results = await asyncio.gather(*queries)


asyncio.run(main())
