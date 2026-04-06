import logging
import uuid

from django.utils.deprecation import MiddlewareMixin

REQUEST_ID_CONTEXT = "request_id"


class RequestIDMiddleware(MiddlewareMixin):
    header_name = "HTTP_X_REQUEST_ID"
    response_header_name = "X-Request-ID"

    def process_request(self, request):
        request_id = request.META.get(self.header_name) or str(uuid.uuid4())
        request.request_id = request_id

    def process_response(self, request, response):
        request_id = getattr(request, "request_id", None)
        if request_id:
            response[self.response_header_name] = request_id
        return response


class RequestIDLogFilter(logging.Filter):
    def filter(self, record):
        if not hasattr(record, REQUEST_ID_CONTEXT):
            record.request_id = "-"
        return True