import asyncio
import logging
import socket
import signal
from asyncio import AbstractEventLoop
from typing import List


async def echo(connection: socket.socket, loop: AbstractEventLoop) -> None:
    try:
        while data := await loop.sock_recv(connection, 1024):
            print("Got a data!")
            if data == b"boom\r\n":
                raise Exception("Unexpected network error.")
            await loop.sock_sendall(connection, data)
    except Exception as ex:
        logging.exception(ex)
    finally:
        connection.close()


async def connection_listener(server_socket: socket.socket, loop: AbstractEventLoop):
    while True:
        connection, address = await loop.sock_accept(server_socket)
        connection.setblocking(False)
        print(f"Got a connection from {address}")
        yield asyncio.create_task(echo(connection, loop))


class GracefulExit(SystemExit):
    pass


def shutdown():
    raise GracefulExit()


async def close_echo_tasks(echo_tasks: List[asyncio.Task]):
    waiters = [asyncio.wait_for(task, 2) for task in echo_tasks]
    print(f"waiters {len(waiters)}")
    for task in waiters:
        try:
            await task
        except asyncio.exceptions.TimeoutError:
            pass


echo_tasks = []


async def listen_for_connections(server_socket: socket.socket, loop: AbstractEventLoop):
    async for echo_task in connection_listener(server_socket, loop):
        echo_tasks.append(echo_task)


async def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ("localhost", 8000)
    server_socket.setblocking(False)
    server_socket.bind(server_address)
    server_socket.listen()

    for signame in {"SIGINT", "SIGTERM"}:
        loop.add_signal_handler(getattr(signal, signame), shutdown)
    await listen_for_connections(server_socket, loop)


loop = asyncio.new_event_loop()

try:
    loop.run_until_complete(main())
except GracefulExit:
    loop.run_until_complete(close_echo_tasks(echo_tasks))
finally:
    loop.close()
