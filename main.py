import socket

# https://www.youtube.com/watch?v=4haMUvUxUJI&t=1194s
def generate_response(request):
    pass


def run():
    # AF_INET - address family - standard ip4 protocol
    # SOCK_STREAM - tcp
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # set options. SOL_SOCKET - our socket, SO_REUSEADDR - reuse address, 1 - True
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # connect server_socket with address
    server_socket.bind(('localhost', 5000))
    # listen to the port
    server_socket.listen()

    while True:
        client_socket, address = server_socket.accept()
        request = client_socket.recv(1024)
        # request = b'GET / HTTP/1.1\r\nHost: localhost:5000\r\nConnection: keep-alive\r\nCache-Control:
        # address = ('127.0.0.1', 65499)
        print(request)
        print()
        print(address)

        response = generate_response(request.decode('utf-8'))

        client_socket.sendall(b"hello world")
        client_socket.close()


if __name__ == "__main__":
    run()
