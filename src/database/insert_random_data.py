import asyncio
from pathlib import Path
from typing import List, Tuple, Union
from random import randint, sample
from utils import get_connection


def load_common_words() -> List[str]:
    path = Path("./data/database/common_words.txt")
    with open(path, "r") as common_words:
        return common_words.readlines()


def generate_brand_names(
    words: List[str],
) -> List[Tuple[Union[str,]]]:
    return [(words[index],) for index in sample(range(100), 100)]


def gen_products(
    common_words: List[str],
    brand_id_start: int,
    brand_id_end: int,
    products_to_create: int,
) -> List[Tuple[str, int]]:
    products = []
    for _ in range(products_to_create):
        description = [common_words[index] for index in sample(range(1000), 10)]
        brand_id = randint(brand_id_start, brand_id_end)
        products.append((" ".join(description), brand_id))

    return products


def gen_sku(
    product_id_start: int, product_id_end: int, skus_to_create: int
) -> List[Tuple[int, int, int]]:
    skus = []
    for _ in range(skus_to_create):
        product_id = randint(product_id_start, product_id_end)
        size_int = randint(1, 3)
        color_int = randint(1, 2)
        skus.append((product_id, size_int, color_int))

    return skus


async def insert_brands(common_words, connection) -> int:
    brands = generate_brand_names(common_words)
    insert_brands = "INSERT INTO brand VALUES(DEFAULT, $1)"
    return await connection.executemany(insert_brands, brands)


async def insert_products(common_words, connection) -> int:
    products = gen_products(common_words, 11, 110, 1000)
    insert_products = "INSERT INTO product VALUES(DEFAULT, $1, $2)"
    return await connection.executemany(insert_products, products)


async def insert_skus(connection) -> int:
    skus = gen_sku(1, 1000, 100000)
    insert_sku = "INSERT INTO sku VALUES(DEFAULT, $1, $2, $3)"
    return await connection.executemany(insert_sku, skus)


async def main():
    common_words = load_common_words()
    connection = await get_connection()

    try:
        await insert_brands(common_words, connection)
        await insert_products(common_words, connection)
        await insert_skus(connection)

    finally:
        await connection.close()


asyncio.run(main())
