from abc import ABC, abstractmethod
from functools import cached_property

from urls import URLS


class BaseResponseGenerator(ABC):
    STATUS_SNIPPETS = {
        404: "404 Not found",
        405: "405 Method not allowed",
        200: "200 OK"
    }

    def __call__(self, *args, **kwargs):
        return self._generate_response()

    @abstractmethod
    def _generate_response(self):
        pass

    @cached_property
    def _body(self) -> str:
        if self.code == 404:
            return "<h1>404</h1><p>Not Found</p>"
        if self.code == 405:
            return "<h1>405</h1><p>Method not allowed</p>"
        return f"<h1>{URLS[self.url]()}</h1>"

    @abstractmethod
    @cached_property
    def method(self):
        pass

    @abstractmethod
    @cached_property
    def url(self):
        pass

    @abstractmethod
    @cached_property
    def headers(self):
        pass

    @cached_property
    def code(self) -> int:
        if not self.method == 'GET':
            return 405
        if self.url not in URLS:
            return 404
        return 200

    @cached_property
    def status(self) -> str:
        return self.STATUS_SNIPPETS.get(self.code, "500 Server Error")


class SocketResponseGenerator(BaseResponseGenerator):
    def __init__(self, request):
        self.request: list = request.split(' ')

    def _generate_response(self) -> bytes:
        return (self.headers + self._body).encode()

    @cached_property
    def method(self) -> str:
        return self.request[0]

    @cached_property
    def url(self) -> str:
        return self.request[1]

    @cached_property
    def headers(self) -> str:
        return f"HTTP/1.1 {self.status}\n\n"


class WSGIResponseGenerator(BaseResponseGenerator):
    def __init__(self, environ):
        self.environ: dict = environ

    def _generate_response(self) -> list:
        return [self._body.encode()]

    @cached_property
    def method(self) -> str:
        return self.environ.get("REQUEST_METHOD")

    @cached_property
    def url(self) -> str:
        return self.environ.get("PATH_INFO")

    @cached_property
    def headers(self) -> list:
        return [
            ('Content-Type', 'text/html'),
        ]
