import selectors
import socket
from selectors import SelectorKey
from typing import List, Tuple


def main():
    selector = selectors.DefaultSelector()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    address = ("localhost", 8000)
    server_socket.setblocking(False)
    server_socket.bind(address)
    server_socket.listen()

    selector.register(server_socket, selectors.EVENT_READ)

    while True:
        events: List[Tuple[SelectorKey, int]] = selector.select(timeout=1)

        if not events:
            print("No events, waiting a bit more!")

        for event, _ in events:
            event_socket = event.fileobj

            if event_socket == server_socket:
                conn, client_address = server_socket.accept()
                conn.setblocking(False)
                print(f"I got a connection from {client_address}.")
                selector.register(conn, selectors.EVENT_READ)
            else:
                data = event_socket.recv(1024)
                print(f"I got data: {data}.")
                event_socket.send(data)


if __name__ == "__main__":
    main()
