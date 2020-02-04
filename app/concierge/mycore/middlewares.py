from django.utils.deprecation import MiddlewareMixin
from time import perf_counter


class TimeitMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.start_time = perf_counter()

    def process_response(self, request, response):
        print('Operation took {time:.3f} ms'.format(
            time=(perf_counter() - request.start_time)*1000))
        return response
