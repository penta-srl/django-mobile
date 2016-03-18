from django_mobile import get_flavour, _set_request_header
from django.utils.cache import patch_vary_headers


class FetchFromCacheFlavourMiddleware(object):
    def process_request(self, request):
        _set_request_header(request, get_flavour(request))

class UpdateCacheFlavourMiddleware(object):
    def process_response(self, request, response):
        patch_vary_headers(response, ['X-Flavour'])
        return response
