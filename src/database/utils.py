import os
import asyncpg
from asyncpg.connection import Connection


async def get_connection() -> Connection:
    POSTGRES_USER = os.environ["POSTGRES_USER"]
    POSTGRES_PASSWORD = os.environ["POSTGRES_PASSWORD"]

    connection = await asyncpg.connect(
        host="0.0.0.0",
        port=5432,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        database="products",
    )

    return connection
