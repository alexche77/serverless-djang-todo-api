"""Mixins to extend api views"""


class SerializerMixin:
    serializer_class = None

    def get_serializer(self, *args, **kwargs):
        if self.serializer_class:
            return self.serializer_class(*args, **kwargs)
        else:
            return None


class ResponseGenericViewMixin:

    def finalize_response(self, request, response, *args, **kwargs):
        if response.status_code >= 200 and response.status_code < 300:
            if isinstance(response.data, dict) and 'data' not in response.data:
                response.data = {'data': response.data}
        return super().finalize_response(request, response, *args, **kwargs)
