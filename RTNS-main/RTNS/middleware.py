# middleware.py
from partials.views import HeaderView

class HeaderMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        header_data = HeaderView(request)
        request.header = header_data  # Attach header_data to the request object
        
        response = self.get_response(request)
        
        return response