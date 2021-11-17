from wsgiref.simple_server import make_server
from response_processor import WSGIResponseGenerator


def application(environ, start_response):
    response_process = WSGIResponseGenerator(environ)
    start_response(response_process.status, response_process.headers)
    return response_process()


if __name__ == '__main__':
    server = make_server('localhost', 7000, app=application)
    server.serve_forever()
