from django.conf import settings


# version annotation
class BuildVersionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response['X-Build-Version'] = settings.BUILD_VERSION
        return response
