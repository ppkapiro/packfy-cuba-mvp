import uuid
from typing import Callable

from django.http import HttpRequest, HttpResponse
from django.utils.deprecation import MiddlewareMixin


class RequestIDMiddleware(MiddlewareMixin):
    header_name = "HTTP_X_REQUEST_ID"
    response_header = "X-Request-ID"

    def process_request(self, request: HttpRequest):
        incoming = request.META.get(self.header_name)
        request.request_id = incoming or uuid.uuid4().hex  # type: ignore[attr-defined]

    def process_response(self, request: HttpRequest, response: HttpResponse):
        rid = getattr(request, "request_id", None)
        if rid:
            response["X-Request-ID"] = rid
        return response
