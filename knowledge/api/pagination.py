from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination

from knowledge.api.constants import (
    DEFAULT_PAGINATION_LIMIT,
    MAX_PAGINATION_LIMIT,
    PAGE_SIZE,
)


class KnowledgeListPagination(LimitOffsetPagination):
    max_limit = MAX_PAGINATION_LIMIT
    default_limit = DEFAULT_PAGINATION_LIMIT


class KnowledgeListPageNumberPagination(PageNumberPagination):
    page_size = PAGE_SIZE
