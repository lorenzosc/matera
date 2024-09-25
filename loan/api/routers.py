from rest_framework.routers import DefaultRouter
from rest_framework.reverse import reverse

class CustomRouter(DefaultRouter):
    def get_api_root_view(self, api_urls=None):
        original_root_view = super().get_api_root_view(api_urls)

        def api_root(request, *args, **kwargs):
            response = original_root_view(request, *args, **kwargs)

            response.data.update({
                'token_obtain_pair': reverse('token_obtain_pair',
                                             request=request,
                                             format=kwargs.get('format', None)),
                'token_refresh': reverse(
                    'token_refresh',
                    request=request,
                    format=kwargs.get('format', None)),
            })
            return response

        return api_root
