from wsgiref.simple_server import make_server

from main import generate_content, URLS


def generate_code(method: str, url: str):
    if not method == 'GET':
        return 405

    if url not in URLS:
        return 404

    return 200


def generate_status(code: int):
    status_snippets = {
        404: "404 Not found",
        405: "405 Method not allowed",
        200: "200 OK"
    }
    return status_snippets.get(code, "500 Server Error")


def application(environ, start_response):
    method = environ.get("REQUEST_METHOD")
    url = environ.get("PATH_INFO")

    headers = [
        ('Content-Type', 'text/html'),
    ]
    code = generate_code(method, url)
    status = generate_status(code)
    body = generate_content(code, url)

    start_response(status, headers)

    return [body.encode()]


server = make_server('localhost', 7000, app=application)
server.serve_forever()


# todo refactor code
