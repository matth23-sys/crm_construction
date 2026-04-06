import logging
from time import perf_counter

from core.constants import ACTIVITY_LOGGER_NAME, SAFE_HTTP_METHODS

logger = logging.getLogger(ACTIVITY_LOGGER_NAME)


class ActivityLoggingMiddleware:
    """
    Registra actividad básica de requests mutantes.
    Más adelante AuditLog podrá consumir o complementar esto.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        started_at = perf_counter()
        response = None

        try:
            response = self.get_response(request)
            return response
        finally:
            if request.method not in SAFE_HTTP_METHODS:
                duration_ms = round((perf_counter() - started_at) * 1000, 2)
                user = getattr(request, "user", None)
                user_repr = user.pk if getattr(user, "is_authenticated", False) else "anonymous"

                logger.info(
                    "method=%s path=%s status=%s user=%s duration_ms=%s",
                    request.method,
                    request.path,
                    getattr(response, "status_code", 500),
                    user_repr,
                    duration_ms,
                    extra={"request_id": getattr(request, "request_id", "-")},
                )