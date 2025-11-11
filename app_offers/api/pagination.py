from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    """
    Standard pagination class for API results.

    Defines default page size and maximum page size for paginated responses.
    """
    page_size = 6
    max_page_size = 100