import asyncio
import logging
import asyncpg
from utils import get_connection


async def main():
    connection = await get_connection()

    try:
        async with connection.transaction():
            insert_brand = "INSERT INTO brand VALUES(9999, 'big_brand')"
            await connection.execute(insert_brand)
            await connection.execute(insert_brand)
    except Exception:
        logging.exception("Erro while running transaction")
    finally:
        query = """SELECT brand_name FROM brand WHERE brand_name LIKE 'brand%'"""
        brands = await connection.fetch(query)
        print(brands)

        await connection.close()


asyncio.run(main())
