from django.core.paginator import Paginator

from core.constants import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE


class StandardPaginator(Paginator):
    """Paginator base para listados del CRM."""

    def __init__(self, object_list, per_page=DEFAULT_PAGE_SIZE, **kwargs):
        super().__init__(object_list, per_page, **kwargs)


def get_per_page_from_request(request, default=DEFAULT_PAGE_SIZE, max_size=MAX_PAGE_SIZE):
    raw_value = request.GET.get("per_page")

    if not raw_value:
        return default

    try:
        value = int(raw_value)
    except (TypeError, ValueError):
        return default

    return max(1, min(value, max_size))