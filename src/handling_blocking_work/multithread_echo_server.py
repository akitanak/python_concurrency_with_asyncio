from threading import Thread
from socket import socket, AF_INET, SOCK_STREAM, SHUT_RDWR


class ClientEchoThread(Thread):
    def __init__(self, client):
        super().__init__()
        self.client = client

    def run(self):
        try:
            while True:
                data = self.client.recv(2048)
                if data == bytes(0):
                    raise BrokenPipeError("Connection closed.")

                print(f"Received {data}, sending.")
                self.client.sendall(data)

        except OSError as e:
            print(f"Thread interrupted by {e} exception, shutting down...")

    def close(self):
        if self.is_alive():
            self.client.sendall(
                bytes(
                    "Shutting down...",
                    encoding="utf-8",
                )
            )
            self.client.shutdown(SHUT_RDWR)


def echo(client: socket):
    while True:
        data = client.recv(2048)
        print(f"Received {data}, sending!")
        client.sendall(data)


with socket(AF_INET, SOCK_STREAM) as server:
    server.bind(("0.0.0.0", 8000))
    server.listen()
    connection_threads = []
    try:
        while True:
            connection, _ = server.accept()
            thread = ClientEchoThread(connection)
            connection_threads.append(thread)
            thread.start()
    except KeyboardInterrupt:
        print("Shutting down...")
        [thread.close() for thread in connection_threads]
