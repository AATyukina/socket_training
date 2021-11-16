import socket
from urls import URLS


def parse_request(request):
    parsed = request.split(' ')
    method = parsed[0]
    url = parsed[1]
    return method, url


def generate_headers(method, url):
    if not method == 'GET':
        return "HTTP/1.1 405 Method not allowed\n\n", 405

    if url not in URLS:
        return "HTTP/1.1 404 Not found\n\n", 404

    return "HTTP/1.1 200 OK\n\n", 200


def generate_content(code, url):
    if code == 404:
        return "<h1>404</h1><p>Not Found</p>"
    if code == 405:
        return "<h1>405</h1><p>Method not allowed</p>"
    return f"<h1>{URLS[url]()}</h1>"


def generate_response(request):
    method, url = parse_request(request)
    headers, code = generate_headers(method, url)
    body = generate_content(code, url)

    return (headers + body).encode()


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
        print(address, "\n")

        try:
            response = generate_response(request.decode('utf-8'))
            client_socket.sendall(response)
        except IndexError:
            pass
        finally:
            client_socket.close()


if __name__ == "__main__":
    run()
