import asyncio
import asyncpg
from utils import get_connection


async def take(generator, to_take: int):
    item_count = 0
    async for item in generator:
        yield item
        item_count += 1
        if item_count > to_take - 1:
            return


async def main():
    connection = await get_connection()

    query = "SELECT product_id, product_name FROM product"
    try:
        async with connection.transaction():
            product_generator = connection.cursor(query)

            async for product in take(product_generator, 5):
                print(product)

            print("Got the first five generators!")

    finally:
        await connection.close()


asyncio.run(main())
