import asyncio
import os
from typing import List
import asyncpg
from asyncpg import Record


POSTGRES_USER = os.environ["POSTGRES_USER"]
POSTGRES_PASSWORD = os.environ["POSTGRES_PASSWORD"]


async def main():

    connection = await asyncpg.connect(
        host="0.0.0.0",
        port=5432,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        database="products",
    )

    try:
        await connection.execute("INSERT INTO brand VALUES(DEFAULT, 'Levis')")
        await connection.execute("INSERT INTO brand VALUES(DEFAULT, 'Seven')")

        brand_query = "SELECT brand_id, brand_name FROM brand"
        results: List[Record] = await connection.fetch(brand_query)

        for brand in results:
            print(f"id: {brand['brand_id']}, name: {brand['brand_name']}")
    finally:
        await connection.close()


asyncio.run(main())
