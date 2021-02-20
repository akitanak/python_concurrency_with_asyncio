import socket


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    address = ("localhost", 8000)
    server_socket.bind(address)
    server_socket.listen()

    try:
        conn, client_address = server_socket.accept()
        print(f"I got a connection from {client_address}.")

        buffer = conn.recv(2)
        print(f"I got data: {buffer}.")

        while buffer[-2:] != b"\r\n":
            data = conn.recv(2)
            print(f"I got data: {data}")
            buffer = buffer + data

        print(f"All data is {buffer}.")
        conn.sendall(buffer)
    finally:
        server_socket.close()


if __name__ == "__main__":
    main()
