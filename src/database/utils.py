import os
from contextlib import asynccontextmanager
import asyncpg
from asyncpg.connection import Connection


POSTGRES_USER = os.environ["POSTGRES_USER"]
POSTGRES_PASSWORD = os.environ["POSTGRES_PASSWORD"]


async def get_connection() -> Connection:

    connection: Connection = await asyncpg.connect(
        host="0.0.0.0",
        port=5432,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        database="products",
    )

    return connection


@asynccontextmanager
async def get_pool(min_size: int = 6, max_size: int = 6):
    async with asyncpg.create_pool(
        host="0.0.0.0",
        port=5432,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        database="products",
        min_size=min_size,
        max_size=max_size,
    ) as pool:
        yield pool
