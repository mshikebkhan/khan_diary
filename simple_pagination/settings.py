from django.conf import settings


FIRST_LABEL = getattr(
    settings, 'SIMPLE_PAGINATION_FIRST_LABEL', 'First')
PREVIOUS_LABEL = getattr(
    settings, 'SIMPLE_PAGINATION_PREVIOUS_LABEL', '')
PER_PAGE = getattr(settings, 'SIMPLE_PAGINATION_PER_PAGE', 10)
PAGE_LABEL = getattr(settings, 'SIMPLE_PAGINATION_PAGE_LABEL', 'page')
NEXT_LABEL = getattr(
    settings, 'SIMPLE_PAGINATION_NEXT_LABEL', '')
LAST_LABEL = getattr(
    settings, 'SIMPLE_PAGINATION_LAST_LABEL', 'Last')